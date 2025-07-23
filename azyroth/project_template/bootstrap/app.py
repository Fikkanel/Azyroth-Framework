import os
import importlib
import inspect
from flask import Flask, Blueprint
from dotenv import load_dotenv

# Impor AdminController generik dari paket framework Azyroth
from azyroth.AdminController import AdminController

def register_admin_routes(app):
    """Mendeteksi dan mendaftarkan semua rute Admin Resource secara dinamis."""
    resources_path = os.path.join(app.root_path, 'app', 'Admin', 'Resources')
    if not os.path.exists(resources_path):
        return

    admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

    for filename in os.listdir(resources_path):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = f"app.Admin.Resources.{filename[:-3]}"
            mod = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(mod, inspect.isclass):
                if name.endswith('Resource'):
                    resource_class = obj
                    resource_name = resource_class.model.__tablename__
                    controller = AdminController(resource_class)
                    
                    endpoint = f"{resource_name}"
                    admin_bp.add_url_rule(f"/{resource_name}", endpoint=f"{endpoint}.index", view_func=controller.index, methods=['GET'])
                    admin_bp.add_url_rule(f"/{resource_name}/create", endpoint=f"{endpoint}.create", view_func=controller.create, methods=['GET'])
                    admin_bp.add_url_rule(f"/{resource_name}/create", endpoint=f"{endpoint}.store", view_func=controller.store, methods=['POST'])
                    admin_bp.add_url_rule(f"/{resource_name}/<int:id>/edit", endpoint=f"{endpoint}.edit", view_func=controller.edit, methods=['GET'])
                    admin_bp.add_url_rule(f"/{resource_name}/<int:id>/edit", endpoint=f"{endpoint}.update", view_func=controller.update, methods=['POST'])
                    admin_bp.add_url_rule(f"/{resource_name}/<int:id>/delete", endpoint=f"{endpoint}.destroy", view_func=controller.destroy, methods=['POST'])
    
    app.register_blueprint(admin_bp)

def create_app():
    """Membuat dan mengkonfigurasi instance aplikasi."""
    app = Flask('app')
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app.template_folder=os.path.join(project_root, 'resources', 'views')
    
    load_dotenv(os.path.join(project_root, '.env'))

    from config import app as app_config, database as db_config
    app.config.update(app.config)
    app.config['DATABASE_CONFIG'] = db_config.CONFIG
    app.secret_key = app.config.get('KEY')

    from app.Providers.AppServiceProvider import AppServiceProvider
    from app.Providers.DatabaseServiceProvider import DatabaseServiceProvider

    providers = [AppServiceProvider(app), DatabaseServiceProvider(app)]
    for provider in providers:
        if hasattr(provider, 'register'): provider.register()
    for provider in providers:
        if hasattr(provider, 'boot'): provider.boot()
            
    from routes.web import register_routes
    register_routes(app)

    # Daftarkan rute admin
    register_admin_routes(app)

    return app
