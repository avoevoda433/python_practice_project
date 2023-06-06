from flask import Flask, Blueprint, render_template


app_page = Blueprint('app', __name__, template_folder='templates/layouts')


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.register_blueprint(app_page)

    return app


@app_page.route('/')
def home():
    return render_template('app.html')


if __name__ == '__main__':
    create_app().run()
