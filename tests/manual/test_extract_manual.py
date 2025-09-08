from ddd.config_extractors import ConfigurationExtractor
from pathlib import Path
import tempfile

test_code = """
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
"""

extractor = ConfigurationExtractor()

# Create temp directory with test file
with tempfile.TemporaryDirectory() as tmpdir:
    test_file = Path(tmpdir) / "settings.py"
    test_file.write_text(test_code)
    
    # Extract configs
    result = extractor.extract_configs(tmpdir)
    
    print(f"Found {len(result)} configs:")
    for config in result:
        print(f"  - {config.name}: {config.type} (sensitive: {config.is_sensitive})")
