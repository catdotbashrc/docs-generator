#!/usr/bin/env python3
"""
Test suite for the metrics collection system.

Following TDD principles: Write failing tests first, then make them pass.
"""

import json
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add hook lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / '.claude' / 'hooks' / 'lib'))

from metrics_collector import (
    MetricsCollector, 
    MetricEvent, 
    MetricType,
    MetricsContext,
    get_metrics_collector
)


class TestMetricsCollector(unittest.TestCase):
    """Test the MetricsCollector class functionality."""
    
    def setUp(self):
        """Create a temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.collector = MetricsCollector(db_path=Path(self.temp_db.name))
        
    def tearDown(self):
        """Clean up temporary database."""
        self.temp_db.close()
        Path(self.temp_db.name).unlink(missing_ok=True)
        
    def test_initialization_creates_database(self):
        """Test that initialization creates the database with proper schema."""
        # Verify database exists
        self.assertTrue(Path(self.temp_db.name).exists())
        
        # Verify schema
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.assertIn('metrics', tables)
            
            # Check indices
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
            indices = [row[0] for row in cursor.fetchall()]
            self.assertIn('idx_timestamp', indices)
            self.assertIn('idx_metric_type', indices)
            
    def test_log_metric_stores_event(self):
        """Test that logging a metric stores it in the database."""
        # Log a metric
        self.collector.log_metric(
            MetricType.MEMORY_LOAD,
            'TestHook',
            {'memory_name': 'TEST_MEMORY', 'tokens': 1000},
            duration_ms=50.5
        )
        
        # Verify it was stored
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.execute("SELECT * FROM metrics")
            rows = cursor.fetchall()
            
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row[2], 'memory_load')  # metric_type
        self.assertEqual(row[3], 'TestHook')  # hook_name
        self.assertAlmostEqual(row[6], 50.5)  # duration_ms
        
    def test_memory_access_counter(self):
        """Test that memory access events are counted in cache."""
        # Log multiple accesses
        for i in range(3):
            self.collector.log_metric(
                MetricType.MEMORY_ACCESS,
                'TestHook',
                {'memory_name': 'PROJECT_MANIFEST'}
            )
            
        self.assertEqual(
            self.collector.cache['memory_access_count']['PROJECT_MANIFEST'], 
            3
        )
        
    def test_cache_hit_rate_calculation(self):
        """Test cache hit rate calculation."""
        # Log cache events
        for _ in range(7):
            self.collector.log_cache_event('TestHook', 'MEMORY1', is_hit=True)
        for _ in range(3):
            self.collector.log_cache_event('TestHook', 'MEMORY2', is_hit=False)
            
        # Get summary
        summary = self.collector.get_metrics_summary(hours=1)
        
        self.assertAlmostEqual(summary['cache_hit_rate'], 70.0)
        
    def test_token_usage_tracking(self):
        """Test that token usage is properly tracked."""
        # Log token usage
        self.collector.log_memory_load(
            'TestHook',
            ['MEMORY1', 'MEMORY2'],
            5000,
            100.0
        )
        
        self.assertEqual(self.collector.cache['total_tokens_used'], 5000)
        
    def test_error_logging(self):
        """Test that errors are properly logged."""
        self.collector.log_error(
            'TestHook',
            'ValueError',
            'Test error message',
            {'context': 'test'}
        )
        
        # Verify error was stored
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.execute(
                "SELECT * FROM metrics WHERE metric_type = 'error'"
            )
            rows = cursor.fetchall()
            
        self.assertEqual(len(rows), 1)
        event_data = json.loads(rows[0][4])
        self.assertEqual(event_data['error_type'], 'ValueError')
        
    def test_metrics_context_manager(self):
        """Test the MetricsContext context manager for timing."""
        with MetricsContext(self.collector, 'TestHook', 'test_operation'):
            pass  # Simulate some work
            
        # Check that performance metric was logged
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.execute(
                "SELECT * FROM metrics WHERE metric_type = 'performance'"
            )
            rows = cursor.fetchall()
            
        self.assertEqual(len(rows), 1)
        self.assertIsNotNone(rows[0][6])  # duration_ms should be set
        
    def test_freshness_check_logging(self):
        """Test logging of freshness check events."""
        self.collector.log_freshness_check(
            'TestHook',
            'CURRENT_SPRINT',
            is_fresh=False,
            staleness_seconds=3600,
            auto_refreshed=True
        )
        
        # Verify both freshness check and auto-refresh were logged
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.execute("SELECT metric_type FROM metrics")
            types = [row[0] for row in cursor.fetchall()]
            
        self.assertIn('freshness_check', types)
        self.assertIn('auto_refresh', types)
        
    def test_optimization_recommendations(self):
        """Test that optimization recommendations are generated correctly."""
        # Simulate low cache hit rate
        for _ in range(3):
            self.collector.log_cache_event('TestHook', 'MEM1', is_hit=True)
        for _ in range(7):
            self.collector.log_cache_event('TestHook', 'MEM2', is_hit=False)
            
        recommendations = self.collector.get_optimization_recommendations()
        
        # Should recommend improving cache
        cache_recs = [r for r in recommendations if r['category'] == 'cache']
        self.assertTrue(len(cache_recs) > 0)
        self.assertEqual(cache_recs[0]['priority'], 'high')
        
    def test_metrics_export_json(self):
        """Test exporting metrics to JSON format."""
        # Log some metrics
        self.collector.log_metric(
            MetricType.MEMORY_LOAD,
            'TestHook',
            {'test': 'data'}
        )
        
        # Export to JSON
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            export_path = Path(f.name)
            
        try:
            self.collector.export_metrics(export_path, format='json', hours=1)
            
            # Verify JSON content
            with open(export_path) as f:
                data = json.load(f)
                
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['metric_type'], 'memory_load')
            
        finally:
            export_path.unlink(missing_ok=True)
            
    def test_cleanup_old_metrics(self):
        """Test cleanup of old metrics."""
        # Insert an old metric directly
        old_time = datetime.now() - timedelta(days=40)
        with sqlite3.connect(self.temp_db.name) as conn:
            conn.execute(
                "INSERT INTO metrics (timestamp, metric_type, hook_name, event_data) VALUES (?, ?, ?, ?)",
                (old_time.isoformat(), 'test', 'TestHook', '{}')
            )
            
        # Also log a recent metric
        self.collector.log_metric(MetricType.MEMORY_LOAD, 'TestHook', {})
        
        # Clean up metrics older than 30 days
        deleted = self.collector.cleanup_old_metrics(days=30)
        
        self.assertEqual(deleted, 1)
        
        # Verify only recent metric remains
        with sqlite3.connect(self.temp_db.name) as conn:
            count = conn.execute("SELECT COUNT(*) FROM metrics").fetchone()[0]
            
        self.assertEqual(count, 1)
        
    def test_singleton_pattern(self):
        """Test that get_metrics_collector returns singleton instance."""
        collector1 = get_metrics_collector()
        collector2 = get_metrics_collector()
        
        self.assertIs(collector1, collector2)


class TestHookIntegrationWithMetrics(unittest.TestCase):
    """Test hook integration with metrics system."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.collector = MetricsCollector(db_path=Path(self.temp_db.name))
        
    def tearDown(self):
        """Clean up."""
        self.temp_db.close()
        Path(self.temp_db.name).unlink(missing_ok=True)
        
    @patch('metrics_collector.get_metrics_collector')
    def test_hook_logs_metrics_on_success(self, mock_get_collector):
        """Test that hooks log metrics on successful execution."""
        mock_get_collector.return_value = self.collector
        
        # Simulate hook execution
        with MetricsContext(self.collector, 'TestHook', 'load_memories'):
            # Simulate loading memories
            self.collector.log_memory_load(
                'TestHook',
                ['MEMORY1', 'MEMORY2'],
                3000,
                50.0
            )
            
        # Verify metrics were logged
        summary = self.collector.get_metrics_summary(hours=1)
        
        self.assertGreater(summary['total_events'], 0)
        self.assertIn('memory_load', summary['events_by_type'])
        
    @patch('metrics_collector.get_metrics_collector')
    def test_hook_logs_errors_on_failure(self, mock_get_collector):
        """Test that hooks log errors on failure."""
        mock_get_collector.return_value = self.collector
        
        # Simulate hook failure
        try:
            with MetricsContext(self.collector, 'TestHook', 'failing_operation'):
                raise ValueError("Test error")
        except ValueError:
            pass  # Expected
            
        # Verify error was logged
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.execute(
                "SELECT * FROM metrics WHERE metric_type = 'error'"
            )
            rows = cursor.fetchall()
            
        self.assertEqual(len(rows), 1)
        event_data = json.loads(rows[0][4])
        self.assertEqual(event_data['error_type'], 'ValueError')


class TestMetricsAnalysis(unittest.TestCase):
    """Test metrics analysis and reporting functionality."""
    
    def setUp(self):
        """Set up test environment with sample data."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.collector = MetricsCollector(db_path=Path(self.temp_db.name))
        self._populate_sample_data()
        
    def tearDown(self):
        """Clean up."""
        self.temp_db.close()
        Path(self.temp_db.name).unlink(missing_ok=True)
        
    def _populate_sample_data(self):
        """Populate database with sample metrics data."""
        # Memory loads
        for memory in ['PROJECT_MANIFEST', 'CURRENT_SPRINT', 'JAVA_PATTERNS']:
            for _ in range(5):
                self.collector.log_memory_load(
                    'SessionStart',
                    [memory],
                    2000,
                    45.0
                )
                
        # Cache events
        for _ in range(70):
            self.collector.log_cache_event('PreToolUse', 'MEM1', is_hit=True)
        for _ in range(30):
            self.collector.log_cache_event('PreToolUse', 'MEM2', is_hit=False)
            
        # Tool usage
        for tool in ['Write', 'Read', 'Grep']:
            self.collector.log_tool_usage(
                'PreToolUse',
                tool,
                ['PROJECT_MANIFEST'],
                120.0
            )
            
    def test_summary_generation(self):
        """Test that summary generation provides accurate statistics."""
        summary = self.collector.get_metrics_summary(hours=24)
        
        self.assertGreater(summary['total_events'], 0)
        self.assertAlmostEqual(summary['cache_hit_rate'], 70.0, places=1)
        self.assertIn('memory_load', summary['events_by_type'])
        self.assertIn('cache_hit', summary['events_by_type'])
        
    def test_most_accessed_memories(self):
        """Test identification of most accessed memories."""
        # Log additional accesses
        for _ in range(10):
            self.collector.log_metric(
                MetricType.MEMORY_ACCESS,
                'TestHook',
                {'memory_name': 'PROJECT_MANIFEST'}
            )
            
        summary = self.collector.get_metrics_summary(hours=24)
        
        most_accessed = summary['most_accessed_memories']
        self.assertTrue(len(most_accessed) > 0)
        self.assertEqual(most_accessed[0]['memory'], 'PROJECT_MANIFEST')


if __name__ == '__main__':
    unittest.main()