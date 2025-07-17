from functools import wraps
from flask import request, abort, session

class VerifyCsrfToken:
    """Middleware untuk proteksi CSRF."""

    def handle(self, next_middleware):
        @wraps(next_middleware)
        def decorated_function(*args, **kwargs):
            if request.method in ['POST', 'PUT', 'DELETE']:
                token = request.form.get('_token') or request.headers.get('X-CSRF-TOKEN')
                if not token or token != session.get('csrf_token'):
                    abort(419, "CSRF token mismatch.")
            return next_middleware(*args, **kwargs)
        return decorated_function