import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    """Membuat dan mengkonfigurasi instance aplikasi."""
    app = Flask('app')

    # --- BAGIAN YANG DIPERBAIKI & DITAMBAHKAN ---

    # Tentukan path dan muat file .env
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    load_dotenv(os.path.join(project_root, '.env'))

    # Muat Konfigurasi dari folder config/
    from config import app as app_config, database as db_config
    app.config.update(app_config.CONFIG)
    app.config['DATABASE_CONFIG'] = db_config.CONFIG # Konfigurasi DB
    app.secret_key = app.config.get('KEY')

    # Impor Service Provider
    from app.Providers.AppServiceProvider import AppServiceProvider
    from app.Providers.DatabaseServiceProvider import DatabaseServiceProvider

    # Daftarkan semua provider
    providers = [
        AppServiceProvider(app),
        DatabaseServiceProvider(app)
    ]

    # Jalankan method register() dari semua provider
    for provider in providers:
        if hasattr(provider, 'register'):
            provider.register()

    # Jalankan method boot() dari semua provider
    for provider in providers:
        if hasattr(provider, 'boot'):
            provider.boot()
            
    # --- AKHIR DARI BAGIAN PERBAIKAN ---

    # Registrasi Rute
    from routes.web import register_routes
    register_routes(app)

    return app
