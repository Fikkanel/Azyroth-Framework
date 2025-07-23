from flask import session, redirect, url_for, flash

def admin_auth_middleware():
    """
    Middleware untuk memeriksa apakah admin sudah login.
    Dijalankan sebelum setiap request ke blueprint admin.
    """
    # Middleware ini diterapkan pada Blueprint, jadi kita tidak perlu
    # khawatir tentang halaman login/logout karena mereka berada di luar Blueprint.
    if 'admin_logged_in' not in session:
        flash('Anda harus login untuk mengakses halaman ini.', 'danger')
        return redirect(url_for('admin_login'))
