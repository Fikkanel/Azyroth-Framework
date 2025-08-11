from app.Models.User import User

class UserSeeder:
    def run(self, session):
        """Menjalankan database seeder untuk user."""
        if session.query(User).count() == 0:
            admin_user = User(
                name='Admin',
                email='admin@example.com',
                password='password' # Ingat untuk hash password di aplikasi nyata
            )
            session.add(admin_user)
            session.commit()
            print("Admin user has been created.")
        else:
            print("Users table is not empty, skipping UserSeeder.")
