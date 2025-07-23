import os
import importlib
import inspect
from flask import Flask, Blueprint, render_template, session, redirect, url_for, request, flash
from dotenv import load_dotenv

# Impor dari framework dan aplikasi
try:
    from azyroth.AdminController import AdminController
    from app.Http.Middleware.AdminAuthMiddleware import admin_auth_middleware
except ImportError as e:
    # Fallback jika ada masalah impor, agar server tetap bisa jalan
    print(f"Peringatan Impor: {e}. Fitur admin mungkin tidak berfungsi.")
    AdminController = None
    admin_auth_middleware = None

def register_admin_routes(app, discovered_resources):
    """Mendaftarkan rute CRUD dinamis berdasarkan resource yang ditemukan."""
    if not discovered_resources or AdminController is None:
        return

    admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
    
    # Terapkan middleware ke semua rute di dalam blueprint ini
    if admin_auth_middleware:
        admin_bp.before_request(admin_auth_middleware)

    # Rute untuk dashboard
    @admin_bp.route('/')
    def dashboard():
        return render_template('admin/dashboard.html', page_title="Dashboard")

    # Rute dinamis untuk setiap resource
    for resource in discovered_resources:
        resource_class = resource['class']
        resource_name = resource['name']
        controller = AdminController(resource_class)
        
        endpoint = resource_name
        admin_bp.add_url_rule(f"/{resource_name}", endpoint=f"{endpoint}_index", view_func=controller.index, methods=['GET'])
        admin_bp.add_url_rule(f"/{resource_name}/create", endpoint=f"{endpoint}_create", view_func=controller.create, methods=['GET'])
        admin_bp.add_url_rule(f"/{resource_name}/create", endpoint=f"{endpoint}_store", view_func=controller.store, methods=['POST'])
        admin_bp.add_url_rule(f"/{resource_name}/<int:id>/edit", endpoint=f"{endpoint}_edit", view_func=controller.edit, methods=['GET'])
        admin_bp.add_url_rule(f"/{resource_name}/<int:id>/edit", endpoint=f"{endpoint}_update", view_func=controller.update, methods=['POST'])
        admin_bp.add_url_rule(f"/{resource_name}/<int:id>/delete", endpoint=f"{endpoint}_destroy", view_func=controller.destroy, methods=['POST'])
    
    app.register_blueprint(admin_bp)

def create_app():
    """Membuat dan mengkonfigurasi instance aplikasi."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask('app', template_folder=os.path.join(project_root, 'resources', 'views'))
    load_dotenv(os.path.join(project_root, '.env'))

    # Muat Konfigurasi
    from config import app as app_config, database as db_config
    app.config.update(app_config.CONFIG)
    app.config['DATABASE_CONFIG'] = db_config.CONFIG
    app.secret_key = app.config.get('KEY')

    # Jalankan Service Provider
    from app.Providers.AppServiceProvider import AppServiceProvider
    from app.Providers.DatabaseServiceProvider import DatabaseServiceProvider
    providers = [AppServiceProvider(app), DatabaseServiceProvider(app)]
    for provider in providers:
        if hasattr(provider, 'register'): provider.register()
    for provider in providers:
        if hasattr(provider, 'boot'): provider.boot()

    # Temukan semua file Resource
    discovered_resources = []
    resources_path = os.path.join(app.root_path, 'app', 'Admin', 'Resources')
    if os.path.exists(resources_path):
        for filename in os.listdir(resources_path):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = f"app.Admin.Resources.{filename[:-3]}"
                try:
                    mod = importlib.import_module(module_name)
                    for name, obj in inspect.getmembers(mod, inspect.isclass):
                        if name.endswith('Resource'):
                            discovered_resources.append({'name': obj.model.__tablename__, 'class': obj})
                except ImportError as e:
                    print(f"PERINGATAN: Gagal mengimpor resource '{module_name}'. Error: {e}")

    # Sediakan daftar resource ke semua template
    @app.context_processor
    def inject_admin_resources():
        return dict(admin_resources=discovered_resources)

    # Daftarkan Rute Web dan Admin
    from routes.web import register_routes
    register_routes(app)
    register_admin_routes(app, discovered_resources)

    # Daftarkan Rute Login/Logout Admin (di luar Blueprint agar tidak terlindungi middleware)
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            # GANTI DENGAN LOGIKA OTENTIKASI ANDA YANG SEBENARNYA
            if request.form.get('username') == 'admin' and request.form.get('password') == 'password':
                session['admin_logged_in'] = True
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Username atau password salah', 'danger')
        return render_template('admin/login.html') # Anda perlu membuat template ini

    @app.route('/admin/logout')
    def admin_logout():
        session.pop('admin_logged_in', None)
        return redirect(url_for('admin_login'))

    return app
