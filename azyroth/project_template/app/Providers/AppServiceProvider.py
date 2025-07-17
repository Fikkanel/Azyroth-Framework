class AppServiceProvider:
    """
    Service provider utama aplikasi.
    Di sini Anda bisa mendaftarkan binding ke service container atau menjalankan logika bootstrap lainnya.
    """

    def __init__(self, app):
        self.app = app

    def register(self):
        """Mendaftarkan service-container bindings."""
        # Contoh:
        # from app.Services.MyService import MyService
        # self.app.container.singleton('my_service', MyService)
        print("AppServiceProvider registered.")

    def boot(self):
        """Bootstrap service aplikasi."""
        # Logika yang dijalankan setelah semua provider ter-register
        print("AppServiceProvider booted.")