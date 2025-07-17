from flask import current_app, g
from app.Models.User import User

class UserSeeder:
    def run(self):
        """Jalankan database seeder."""
        session = g.db_session
        
        # Contoh data
        user = User(
            name='Admin User',
            email='admin@azyroth.com',
            password='password' # Ingat untuk hash password di aplikasi nyata
        )
        
        session.add(user)
        session.commit()
        
        print("UserSeeder selesai dijalankan.")

# Untuk menjalankan seeder ini, Anda perlu membuat perintah CLI khusus.