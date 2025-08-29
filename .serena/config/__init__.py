# Serena Configuration Module
import yaml
from pathlib import Path

def load_config():
    """Load advanced configuration"""
    config_path = Path(__file__).parent / "advanced_settings.yml"
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}

CONFIG = load_config()
