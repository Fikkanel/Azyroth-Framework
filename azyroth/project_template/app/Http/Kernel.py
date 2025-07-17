# Mendaftarkan middleware HTTP global dan grup middleware.
# Contoh ini masih sederhana dan belum mengimplementasikan grup.

from app.Http.Middleware.VerifyCsrfToken import VerifyCsrfToken

# Middleware yang akan dijalankan pada setiap request
global_middleware = [
    # Contoh:
    # VerifyCsrfToken,
]

# Grup middleware (misal: 'web', 'api')
middleware_groups = {
    'web': [
        VerifyCsrfToken,
    ],
    'api': [
        # Middleware untuk API, misal: ThrottleRequests
    ]
}