from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g

class DatabaseServiceProvider:
    def __init__(self, app):
        self.app = app
        self.config = app.config.get('DATABASE_CONFIG')

    def register(self):
        """Mendaftarkan koneksi database ke aplikasi."""
        if self.config and self.config['default'] == 'mysql':
            db_config = self.config['connections']['mysql']
            db_uri = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            
            engine = create_engine(db_uri)
            Session = sessionmaker(bind=engine)
            
            # Membuatnya dapat diakses di seluruh aplikasi
            self.app.db_engine = engine
            self.app.db_session = Session

            print("DatabaseServiceProvider registered.")

    def boot(self):
        """Konfigurasi koneksi database per request."""
        @self.app.before_request
        def before_request():
            # Membuat sesi DB baru untuk setiap request
            g.db_session = self.app.db_session()

        @self.app.teardown_request
        def teardown_request(exception=None):
            # Menutup sesi DB setelah request selesai
            db_session = g.pop('db_session', None)
            if db_session is not None:
                db_session.close()

        print("DatabaseServiceProvider booted.")