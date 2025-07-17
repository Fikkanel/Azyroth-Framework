import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    """Membuat dan mengkonfigurasi instance aplikasi."""

    # Tentukan root path proyek secara eksplisit
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(
        'app',
        template_folder=os.path.join(project_root, 'resources', 'views'),
        static_folder=os.path.join(project_root, 'public')
    )
    
    # Muat .env dari root proyek aplikasi
    load_dotenv(os.path.join(project_root, '.env'))

    # Muat Konfigurasi dari folder config/
    from config import app as app_config, database as db_config
    app.config.update(app_config.CONFIG)
    app.config['DATABASE_CONFIG'] = db_config.CONFIG
    app.secret_key = app.config.get('KEY')

    # Impor dan jalankan Service Provider
    from app.Providers.AppServiceProvider import AppServiceProvider
    from app.Providers.DatabaseServiceProvider import DatabaseServiceProvider

    providers = [AppServiceProvider(app), DatabaseServiceProvider(app)]
    for provider in providers:
        if hasattr(provider, 'register'): provider.register()
    for provider in providers:
        if hasattr(provider, 'boot'): provider.boot()
            
    # Registrasi Rute
    from routes.web import register_routes
    register_routes(app)

    return app
