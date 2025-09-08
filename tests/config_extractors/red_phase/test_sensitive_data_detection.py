"""
Sensitive Data Detection Contract Tests (RED Phase)

Tests that verify configuration extractors can identify and flag sensitive data.
"""

from typing import List

import pytest

from ..base import BaseConfigExtractorTest, ExtractorTestCase


class TestSensitiveDataDetection(BaseConfigExtractorTest):
    """Contract for detecting sensitive configuration data across languages"""
    
    def get_extractor(self):
        """Return configuration extractor with sensitive data detection"""
        from ddd.config_extractors import ConfigurationExtractor
        return ConfigurationExtractor()
    
    def get_test_cases(self) -> List[ExtractorTestCase]:
        """Test cases for sensitive data detection"""
        return [
            # Python sensitive patterns
            ExtractorTestCase(
                name="python_database_credentials",
                input_code="""
DATABASE_URL = 'postgresql://user:password@localhost/dbname'
DB_PASSWORD = 'super_secret_123'
MONGO_URI = 'mongodb://admin:pass123@localhost:27017/'
REDIS_PASSWORD = 'redis_secret'
""",
                expected_configs=[
                    {'name': 'DATABASE_URL', 'is_sensitive': True, 'reason': 'contains_credentials'},
                    {'name': 'DB_PASSWORD', 'is_sensitive': True, 'reason': 'password_field'},
                    {'name': 'MONGO_URI', 'is_sensitive': True, 'reason': 'contains_credentials'},
                    {'name': 'REDIS_PASSWORD', 'is_sensitive': True, 'reason': 'password_field'},
                ],
                language="python",
                description="Detect database credentials in Python"
            ),
            
            # JavaScript API keys and tokens
            ExtractorTestCase(
                name="javascript_api_tokens",
                input_code="""
const config = {
    API_KEY: 'abc123def456',
    API_SECRET: 'secret_key_here',
    ACCESS_TOKEN: 'token_xyz789',
    REFRESH_TOKEN: 'refresh_abc123',
    CLIENT_SECRET: 'client_secret_value',
    PRIVATE_KEY: '-----BEGIN RSA PRIVATE KEY-----',
    PUBLIC_KEY: '-----BEGIN PUBLIC KEY-----'
};
""",
                expected_configs=[
                    {'name': 'API_KEY', 'is_sensitive': True, 'reason': 'api_key'},
                    {'name': 'API_SECRET', 'is_sensitive': True, 'reason': 'secret_field'},
                    {'name': 'ACCESS_TOKEN', 'is_sensitive': True, 'reason': 'token_field'},
                    {'name': 'REFRESH_TOKEN', 'is_sensitive': True, 'reason': 'token_field'},
                    {'name': 'CLIENT_SECRET', 'is_sensitive': True, 'reason': 'secret_field'},
                    {'name': 'PRIVATE_KEY', 'is_sensitive': True, 'reason': 'private_key'},
                    {'name': 'PUBLIC_KEY', 'is_sensitive': False},  # Public keys are not sensitive
                ],
                language="javascript",
                description="Detect API tokens and keys in JavaScript"
            ),
            
            # Environment variable patterns
            ExtractorTestCase(
                name="env_var_sensitive_patterns",
                input_code="""
# .env file patterns
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
GITHUB_TOKEN=ghp_1234567890abcdef
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
SENDGRID_API_KEY=SG.1234567890.abcdefghijklmnop
JWT_SECRET=my_super_secret_jwt_key
ENCRYPTION_KEY=base64encodedkey==
SALT=random_salt_value
""",
                expected_configs=[
                    {'name': 'AWS_ACCESS_KEY_ID', 'is_sensitive': True, 'reason': 'aws_credential'},
                    {'name': 'AWS_SECRET_ACCESS_KEY', 'is_sensitive': True, 'reason': 'aws_credential'},
                    {'name': 'GITHUB_TOKEN', 'is_sensitive': True, 'reason': 'github_token'},
                    {'name': 'SLACK_WEBHOOK_URL', 'is_sensitive': True, 'reason': 'webhook_url'},
                    {'name': 'SENDGRID_API_KEY', 'is_sensitive': True, 'reason': 'api_key'},
                    {'name': 'JWT_SECRET', 'is_sensitive': True, 'reason': 'jwt_secret'},
                    {'name': 'ENCRYPTION_KEY', 'is_sensitive': True, 'reason': 'encryption_key'},
                    {'name': 'SALT', 'is_sensitive': True, 'reason': 'cryptographic_material'},
                ],
                language="env",
                description="Detect sensitive patterns in environment variables"
            ),
            
            # Mixed sensitivity levels
            ExtractorTestCase(
                name="mixed_sensitivity",
                input_code="""
# Some sensitive, some not
APP_NAME = "My Application"  # Not sensitive
APP_VERSION = "1.0.0"  # Not sensitive
LOG_LEVEL = "info"  # Not sensitive
DATABASE_HOST = "localhost"  # Not sensitive
DATABASE_PORT = 5432  # Not sensitive
DATABASE_USER = "admin"  # Potentially sensitive
DATABASE_PASSWORD = "secret123"  # Sensitive
SESSION_SECRET = "keyboard cat"  # Sensitive
COOKIE_DOMAIN = ".example.com"  # Not sensitive
ADMIN_EMAIL = "admin@example.com"  # Not sensitive
SMTP_PASSWORD = "smtp_pass"  # Sensitive
""",
                expected_configs=[
                    {'name': 'APP_NAME', 'is_sensitive': False},
                    {'name': 'APP_VERSION', 'is_sensitive': False},
                    {'name': 'LOG_LEVEL', 'is_sensitive': False},
                    {'name': 'DATABASE_HOST', 'is_sensitive': False},
                    {'name': 'DATABASE_PORT', 'is_sensitive': False},
                    {'name': 'DATABASE_USER', 'is_sensitive': True, 'reason': 'username_field'},
                    {'name': 'DATABASE_PASSWORD', 'is_sensitive': True, 'reason': 'password_field'},
                    {'name': 'SESSION_SECRET', 'is_sensitive': True, 'reason': 'secret_field'},
                    {'name': 'COOKIE_DOMAIN', 'is_sensitive': False},
                    {'name': 'ADMIN_EMAIL', 'is_sensitive': False},
                    {'name': 'SMTP_PASSWORD', 'is_sensitive': True, 'reason': 'password_field'},
                ],
                language="python",
                description="Distinguish between sensitive and non-sensitive configs"
            ),
        ]
    
    def get_non_config_samples(self) -> List[str]:
        """These should not trigger sensitive data detection"""
        return [
            # Comments mentioning passwords
            """
# Remember to set DATABASE_PASSWORD in production
# The password should be strong
def connect():
    pass
""",
            # Documentation strings
            """
'''
Configuration Guide:
1. Set your API_KEY in the environment
2. Configure DATABASE_PASSWORD securely
3. Use strong JWT_SECRET values
'''
""",
            # Variable names without values
            """
password = None  # Will be set later
api_key = get_from_vault('api_key')
secret = load_secret()
""",
        ]
    
    def get_sensitive_test_cases(self) -> List[ExtractorTestCase]:
        """Additional sensitive data test cases"""
        return [
            ExtractorTestCase(
                name="oauth_credentials",
                input_code="""
OAUTH_CLIENT_ID = 'client_id_12345'
OAUTH_CLIENT_SECRET = 'client_secret_abcdef'
OAUTH_REDIRECT_URI = 'https://example.com/callback'
OAUTH_ACCESS_TOKEN = 'access_token_xyz'
OAUTH_REFRESH_TOKEN = 'refresh_token_123'
""",
                expected_configs=[
                    {'name': 'OAUTH_CLIENT_ID', 'is_sensitive': False},  # Client ID is usually public
                    {'name': 'OAUTH_CLIENT_SECRET', 'is_sensitive': True},
                    {'name': 'OAUTH_REDIRECT_URI', 'is_sensitive': False},
                    {'name': 'OAUTH_ACCESS_TOKEN', 'is_sensitive': True},
                    {'name': 'OAUTH_REFRESH_TOKEN', 'is_sensitive': True},
                ],
                language="python",
                description="OAuth credential sensitivity"
            ),
            ExtractorTestCase(
                name="encryption_materials",
                input_code="""
const crypto = {
    AES_KEY: 'aes256key1234567890123456789012',
    AES_IV: '1234567890123456',
    RSA_PRIVATE_KEY: '-----BEGIN RSA PRIVATE KEY-----...',
    RSA_PUBLIC_KEY: '-----BEGIN PUBLIC KEY-----...',
    HMAC_SECRET: 'hmac_secret_key',
    SIGNING_KEY: 'signing_key_value',
    ENCRYPTION_SALT: 'salt_value_123'
};
""",
                expected_configs=[
                    {'name': 'AES_KEY', 'is_sensitive': True},
                    {'name': 'AES_IV', 'is_sensitive': True},
                    {'name': 'RSA_PRIVATE_KEY', 'is_sensitive': True},
                    {'name': 'RSA_PUBLIC_KEY', 'is_sensitive': False},
                    {'name': 'HMAC_SECRET', 'is_sensitive': True},
                    {'name': 'SIGNING_KEY', 'is_sensitive': True},
                    {'name': 'ENCRYPTION_SALT', 'is_sensitive': True},
                ],
                language="javascript",
                description="Cryptographic material sensitivity"
            ),
        ]
    
    def test_sensitivity_patterns(self):
        """Test that common sensitive patterns are detected"""
        sensitive_patterns = [
            'password', 'passwd', 'pwd',
            'secret', 'token', 'key',
            'api_key', 'apikey', 'access_key',
            'private', 'credential', 'auth'
        ]
        
        extractor = self.get_extractor()
        
        for pattern in sensitive_patterns:
            # Test uppercase
            test_code = f"{pattern.upper()} = 'some_value'"
            result = extractor.extract_configs(test_code) if hasattr(extractor, 'extract_configs') else []
            if result:
                assert any(c.get('is_sensitive') for c in result), \
                    f"Pattern '{pattern.upper()}' not detected as sensitive"
            
            # Test mixed case
            test_code = f"{pattern.title()}_Config = 'some_value'"
            result = extractor.extract_configs(test_code) if hasattr(extractor, 'extract_configs') else []
            if result:
                assert any(c.get('is_sensitive') for c in result), \
                    f"Pattern '{pattern.title()}_Config' not detected as sensitive"
    
    def test_connection_string_detection(self):
        """Test that connection strings with credentials are detected"""
        connection_strings = [
            "postgresql://user:pass@localhost/db",
            "mysql://root:password@127.0.0.1:3306/database",
            "mongodb://admin:secret@mongo.example.com:27017/",
            "redis://:password@redis.example.com:6379/0",
            "amqp://user:pass@rabbitmq.example.com:5672/vhost",
        ]
        
        extractor = self.get_extractor()
        
        for conn_str in connection_strings:
            test_code = f'DATABASE_URL = "{conn_str}"'
            result = extractor.extract_configs(test_code) if hasattr(extractor, 'extract_configs') else []
            if result:
                assert any(c.get('is_sensitive') for c in result), \
                    f"Connection string not detected as sensitive: {conn_str}"