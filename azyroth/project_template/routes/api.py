from flask import jsonify

def register_routes(app):
    """Mendaftarkan rute API."""
    
    @app.route('/api/user', methods=['GET'])
    def get_user():
        # Logika untuk mengambil data user API
        return jsonify({'user': 'John Doe', 'email': 'john@example.com'})