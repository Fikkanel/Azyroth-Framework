import os

CONFIG = {
    'NAME': os.getenv('APP_NAME', 'Azyroth'),
    'ENV': os.getenv('APP_ENV', 'production'),
    'DEBUG': os.getenv('APP_DEBUG', 'False').lower() in ('true', '1', 't'),
    'KEY': os.getenv('APP_KEY', 'some_default_secret_key'),
    'URL': os.getenv('APP_URL', 'http://localhost'),
}