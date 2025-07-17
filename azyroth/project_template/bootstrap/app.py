import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    """Membuat dan mengkonfigurasi instance aplikasi."""

    # Tentukan root path proyek secara eksplisit
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(
        'app',  # <-- Ganti dengan nama statis, jangan gunakan __name__
        template_folder=os.path.join(project_root, 'resources', 'views'),
        static_folder=os.path.join(project_root, 'public')
    )
    
    # Muat .env dari root proyek aplikasi
    load_dotenv(os.path.join(project_root, '.env'))

    # Muat Konfigurasi
    from config import app as app_config
    app.config.update(app_config.CONFIG)
    app.secret_key = app.config.get('KEY')
    
    # Registrasi Rute
    from routes.web import register_routes as register_web_routes
    register_web_routes(app)

    return app