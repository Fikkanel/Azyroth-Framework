from flask import render_template

class WebController:
    def home(self):
        return render_template('home.html', title='Welcome to Azyroth!')