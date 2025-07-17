import os

# Konfigurasi spesifik aplikasi yang bisa di-override oleh file di direktori /config
# Ini lebih seperti 'config/app.php' di Laravel

APP_CONFIG = {
    'name': os.getenv('APP_NAME', 'Azyroth'),
    'env': os.getenv('APP_ENV', 'production'),
    'debug': os.getenv('APP_DEBUG', 'False').lower() in ('true', '1', 't'),
    'key': os.getenv('APP_KEY'),
    'url': os.getenv('APP_URL', 'http://localhost'),
}