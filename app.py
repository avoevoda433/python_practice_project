from flask import Flask, Blueprint, render_template, request, redirect
from database.database import Database


app_page = Blueprint('app', __name__, template_folder='templates/layouts')
docs_db = Database(db_name="docs_db", user="postgres",
                   password="`1qazxsw2", host="localhost", port="5432")
docs_db.create_table()
docs_db.insert_data()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.register_blueprint(app_page)
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(404, page_not_found)
    return app


@app_page.route('/')
def home():
    return render_template('app.html', data=[])


@app_page.route('/find/', methods=['GET', 'POST'])
def find():
    if request.method == 'GET':
        return render_template('app.html', data=docs_db.get_dock_by_id(request.args.get("search")))
    elif request.method == 'POST':
        docs_db.delete_by_id(request.args.get("search"))
        return render_template('app.html', data=docs_db.get_dock_by_id(request.args.get("search")))


@app_page.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app_page.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405


@app_page.errorhandler(400)
def handle_bad_request(e):
    return  render_template('400.html'), 400


if __name__ == '__main__':
    create_app().run()
