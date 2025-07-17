import os

# Konfigurasi untuk layanan pihak ketiga
CONFIG = {
    'mailgun': {
        'domain': os.getenv('MAILGUN_DOMAIN'),
        'secret': os.getenv('MAILGUN_SECRET'),
    },
    'stripe': {
        'key': os.getenv('STRIPE_KEY'),
        'secret': os.getenv('STRIPE_SECRET'),
    }
}