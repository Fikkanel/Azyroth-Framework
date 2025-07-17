from app.Http.Controllers.WebController import WebController

def register_routes(app):
    controller = WebController()
    app.add_url_rule('/', 'home', view_func=controller.home)