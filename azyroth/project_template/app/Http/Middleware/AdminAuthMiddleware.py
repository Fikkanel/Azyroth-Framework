from functools import wraps
from flask import session, redirect, url_for, flash

def admin_auth_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Anda harus login untuk mengakses halaman ini.', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function
