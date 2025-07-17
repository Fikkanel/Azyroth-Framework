import os
import sys

# Menambahkan root direktori proyek ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bootstrap.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=app.config.get('DEBUG', False)
    )