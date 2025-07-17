# Impor perintah kustom Anda di sini
# from app.Console.Commands.YourCustomCommand import YourCustomCommand

class Inspire:
    """Menampilkan kutipan inspirasional."""
    def handle(self):
        print("Simplicity is the ultimate sophistication. - Leonardo da Vinci")

# Daftarkan semua perintah CLI aplikasi Anda di sini
commands = {
    'inspire': Inspire
}