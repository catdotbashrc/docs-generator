"""
Configuration Extraction Contract Tests (RED Phase)

These tests define the contract that all configuration extractors must fulfill.
Initially, these tests FAIL, driving the implementation.
"""

from dataclasses import dataclass
from typing import Dict, List

import pytest

from ..base import BaseConfigExtractorTest, ExtractorTestCase


class TestPythonConfigExtractionContract(BaseConfigExtractorTest):
    """Contract tests for Python configuration extraction"""
    
    def get_extractor(self):
        """Return Python configuration extractor"""
        from ddd.config_extractors import ConfigurationExtractor
        return ConfigurationExtractor()
    
    def get_test_cases(self) -> List[ExtractorTestCase]:
        """Define expected extraction behavior for Python configs"""
        return [
            ExtractorTestCase(
                name="django_settings",
                input_code="""
# Django settings.py
DEBUG = True
SECRET_KEY = 'django-insecure-key-123'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'postgres',
        'PASSWORD': 'secret123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CACHE_TTL = 3600
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
""",
                expected_configs=[
                    {'name': 'DEBUG', 'value': 'True', 'type': 'boolean'},
                    {'name': 'SECRET_KEY', 'value': 'django-insecure-key-123', 'type': 'string', 'is_sensitive': True},
                    {'name': 'ALLOWED_HOSTS', 'type': 'list'},
                    {'name': 'DATABASES', 'type': 'dict', 'is_sensitive': True},
                    {'name': 'CACHE_TTL', 'value': '3600', 'type': 'integer'},
                    {'name': 'MAX_UPLOAD_SIZE', 'type': 'integer'},
                ],
                language="python",
                description="Extract Django settings configurations"
            ),
            ExtractorTestCase(
                name="flask_config",
                input_code="""
# Flask config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
""",
                expected_configs=[
                    {'name': 'SECRET_KEY', 'source': 'environment', 'is_sensitive': True},
                    {'name': 'SQLALCHEMY_DATABASE_URI', 'source': 'environment', 'is_sensitive': True},
                    {'name': 'SQLALCHEMY_TRACK_MODIFICATIONS', 'value': 'False', 'type': 'boolean'},
                    {'name': 'MAIL_SERVER', 'value': 'smtp.gmail.com', 'type': 'string'},
                    {'name': 'MAIL_PORT', 'value': '587', 'type': 'integer'},
                    {'name': 'MAIL_USE_TLS', 'value': 'True', 'type': 'boolean'},
                    {'name': 'MAIL_USERNAME', 'source': 'environment', 'is_sensitive': True},
                    {'name': 'MAIL_PASSWORD', 'source': 'environment', 'is_sensitive': True},
                ],
                language="python",
                description="Extract Flask configuration with environment variables"
            ),
            ExtractorTestCase(
                name="fastapi_settings",
                input_code="""
# FastAPI settings with Pydantic
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My API"
    admin_email: str = "admin@example.com"
    database_url: str
    redis_url: str = "redis://localhost"
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600
    
    class Config:
        env_file = ".env"
""",
                expected_configs=[
                    {'name': 'app_name', 'default': 'My API', 'type': 'string'},
                    {'name': 'admin_email', 'default': 'admin@example.com', 'type': 'string'},
                    {'name': 'database_url', 'required': True, 'type': 'string', 'is_sensitive': True},
                    {'name': 'redis_url', 'default': 'redis://localhost', 'type': 'string'},
                    {'name': 'jwt_secret', 'required': True, 'type': 'string', 'is_sensitive': True},
                    {'name': 'jwt_algorithm', 'default': 'HS256', 'type': 'string'},
                    {'name': 'jwt_expiration', 'default': '3600', 'type': 'integer'},
                ],
                language="python",
                description="Extract Pydantic-based FastAPI settings"
            ),
        ]
    
    def get_non_config_samples(self) -> List[str]:
        """Code that should NOT be detected as configuration"""
        return [
            # Regular function with constants
            """
def calculate_tax(amount):
    TAX_RATE = 0.08  # This is a calculation constant, not config
    return amount * TAX_RATE
""",
            # Class with non-config attributes
            """
class User:
    def __init__(self, name):
        self.name = name
        self.created_at = datetime.now()
        self.is_active = True  # Instance attribute, not config
""",
            # Test fixtures
            """
@pytest.fixture
def test_user():
    return {
        'username': 'testuser',
        'password': 'testpass123'  # Test data, not config
    }
""",
        ]
    
    def get_sensitive_test_cases(self) -> List[ExtractorTestCase]:
        """Test cases with sensitive configuration data"""
        return [
            ExtractorTestCase(
                name="api_keys",
                input_code="""
API_KEY = 'sk-1234567890abcdef'
AWS_ACCESS_KEY_ID = 'AKIAIOSFODNN7EXAMPLE'
AWS_SECRET_ACCESS_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
STRIPE_SECRET_KEY = 'sk_test_1234567890'
GITHUB_TOKEN = 'ghp_1234567890abcdef'
""",
                expected_configs=[
                    {'name': 'API_KEY', 'is_sensitive': True},
                    {'name': 'AWS_ACCESS_KEY_ID', 'is_sensitive': True},
                    {'name': 'AWS_SECRET_ACCESS_KEY', 'is_sensitive': True},
                    {'name': 'STRIPE_SECRET_KEY', 'is_sensitive': True},
                    {'name': 'GITHUB_TOKEN', 'is_sensitive': True},
                ],
                language="python",
                description="Detect API keys and secrets"
            ),
        ]


class TestJavaScriptConfigExtractionContract(BaseConfigExtractorTest):
    """Contract tests for JavaScript/Node.js configuration extraction"""
    
    def get_extractor(self):
        """Return JavaScript configuration extractor"""
        from ddd.config_extractors import ConfigurationExtractor
        return ConfigurationExtractor()
    
    def get_test_cases(self) -> List[ExtractorTestCase]:
        """Define expected extraction behavior for JavaScript configs"""
        return [
            ExtractorTestCase(
                name="nodejs_env_config",
                input_code="""
// config.js
module.exports = {
    port: process.env.PORT || 3000,
    database: {
        host: process.env.DB_HOST || 'localhost',
        port: process.env.DB_PORT || 5432,
        name: process.env.DB_NAME || 'myapp',
        user: process.env.DB_USER || 'postgres',
        password: process.env.DB_PASSWORD
    },
    jwt: {
        secret: process.env.JWT_SECRET,
        expiresIn: '24h'
    },
    redis: {
        url: process.env.REDIS_URL || 'redis://localhost:6379'
    }
};
""",
                expected_configs=[
                    {'name': 'port', 'source': 'environment', 'default': '3000'},
                    {'name': 'database.host', 'source': 'environment', 'default': 'localhost'},
                    {'name': 'database.port', 'source': 'environment', 'default': '5432'},
                    {'name': 'database.name', 'source': 'environment', 'default': 'myapp'},
                    {'name': 'database.user', 'source': 'environment', 'default': 'postgres'},
                    {'name': 'database.password', 'source': 'environment', 'is_sensitive': True},
                    {'name': 'jwt.secret', 'source': 'environment', 'is_sensitive': True},
                    {'name': 'jwt.expiresIn', 'value': '24h'},
                    {'name': 'redis.url', 'source': 'environment', 'default': 'redis://localhost:6379'},
                ],
                language="javascript",
                description="Extract Node.js configuration with environment variables"
            ),
            ExtractorTestCase(
                name="dotenv_usage",
                input_code="""
// app.js
require('dotenv').config();

const config = {
    APP_NAME: process.env.APP_NAME,
    APP_ENV: process.env.NODE_ENV || 'development',
    API_URL: process.env.API_URL,
    API_KEY: process.env.API_KEY,
    ENABLE_LOGGING: process.env.ENABLE_LOGGING === 'true',
    MAX_CONNECTIONS: parseInt(process.env.MAX_CONNECTIONS || '100'),
};
""",
                expected_configs=[
                    {'name': 'APP_NAME', 'source': 'environment'},
                    {'name': 'APP_ENV', 'source': 'environment', 'default': 'development'},
                    {'name': 'API_URL', 'source': 'environment'},
                    {'name': 'API_KEY', 'source': 'environment', 'is_sensitive': True},
                    {'name': 'ENABLE_LOGGING', 'source': 'environment', 'type': 'boolean'},
                    {'name': 'MAX_CONNECTIONS', 'source': 'environment', 'default': '100', 'type': 'integer'},
                ],
                language="javascript",
                description="Extract dotenv-based configuration"
            ),
        ]
    
    def get_non_config_samples(self) -> List[str]:
        """Code that should NOT be detected as configuration"""
        return [
            # Regular constants in functions
            """
function calculateDiscount(price) {
    const DISCOUNT_RATE = 0.1;  // Calculation constant
    return price * DISCOUNT_RATE;
}
""",
            # React component props
            """
const Button = ({ label = 'Click me', disabled = false }) => {
    return <button disabled={disabled}>{label}</button>;
};
""",
            # Test data
            """
describe('User tests', () => {
    const testUser = {
        email: 'test@example.com',
        password: 'testpass123'
    };
});
""",
        ]
    
    def get_sensitive_test_cases(self) -> List[ExtractorTestCase]:
        """Test cases with sensitive configuration data"""
        return [
            ExtractorTestCase(
                name="api_credentials",
                input_code="""
const config = {
    STRIPE_KEY: 'sk_live_1234567890',
    AWS_ACCESS_KEY: 'AKIAIOSFODNN7EXAMPLE',
    AWS_SECRET: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    DB_PASSWORD: process.env.DB_PASSWORD,
    PRIVATE_KEY: fs.readFileSync('./private.key'),
    SESSION_SECRET: 'keyboard cat'
};
""",
                expected_configs=[
                    {'name': 'STRIPE_KEY', 'is_sensitive': True},
                    {'name': 'AWS_ACCESS_KEY', 'is_sensitive': True},
                    {'name': 'AWS_SECRET', 'is_sensitive': True},
                    {'name': 'DB_PASSWORD', 'is_sensitive': True},
                    {'name': 'PRIVATE_KEY', 'is_sensitive': True},
                    {'name': 'SESSION_SECRET', 'is_sensitive': True},
                ],
                language="javascript",
                description="Detect various types of sensitive credentials"
            ),
        ]