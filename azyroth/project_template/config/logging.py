import os

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'storage', 'logs')

CONFIG = {
    'default': 'file',
    'channels': {
        'file': {
            'driver': 'single',
            'path': os.path.join(LOGS_DIR, 'azyroth.log'),
            'level': 'DEBUG',
        }
    }
}