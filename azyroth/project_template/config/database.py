import os

CONFIG = {
    'default': os.getenv('DB_CONNECTION', 'mysql'),
    'connections': {
        'mysql': {
            'driver': 'mysql',
            'host': os.getenv('DB_HOST', '127.0.0.1'),
            'port': os.getenv('DB_PORT', '3306'),
            'database': os.getenv('DB_DATABASE', 'azyroth'),
            'username': os.getenv('DB_USERNAME', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
        }
    },
    'migrations': 'migrations'
}