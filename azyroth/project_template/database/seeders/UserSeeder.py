from app.Models.User import User
from flask import g

class UserSeeder:
    def run(self):
        """Menjalankan database seeder untuk user."""
        session = g.db_session

        # Hanya jalankan jika tabel user masih kosong
        if session.query(User).count() == 0:
            # Buat user admin contoh
            admin_user = User(
                name='Admin',
                email='admin@example.com',
                password='password' # Ingat untuk hash password di aplikasi nyata
            )
            session.add(admin_user)
            session.commit()
            print("Admin user has been created.")
        else:
            print("Users table is not empty, skipping seeder.")
