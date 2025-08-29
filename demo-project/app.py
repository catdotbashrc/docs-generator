"""
Sample application demonstrating configuration usage
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
DB_PASSWORD = os.environ['DB_PASSWORD']  # Critical - will fail if missing
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', 5432)

# API Keys and Secrets
API_KEY = os.environ.get('API_KEY')
JWT_SECRET = os.environ.get('JWT_SECRET')
STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Application settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', '10485760'))  # 10MB default
SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT', '3600'))

# Email configuration
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT', 587)
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

# Redis configuration
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
CACHE_TTL = int(os.environ.get('CACHE_TTL', '300'))

# Feature flags
ENABLE_NEW_FEATURE = os.getenv('ENABLE_NEW_FEATURE', 'false').lower() == 'true'
ENABLE_ANALYTICS = os.getenv('ENABLE_ANALYTICS', 'true').lower() == 'true'

class Config:
    """Application configuration"""
    
    def __init__(self):
        self.database_url = DATABASE_URL
        self.debug = DEBUG
        self.api_key = API_KEY
        
        # Validate required configs
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is required")
        
        if not JWT_SECRET:
            raise ValueError("JWT_SECRET is required for authentication")