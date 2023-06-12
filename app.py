from flask import Flask, Blueprint, render_template
from database.database import Database


app_page = Blueprint('app', __name__, template_folder='templates/layouts')


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.register_blueprint(app_page)
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(404, page_not_found)

    # docs_db = Database('docs_db')
    # docs_db.create_table('documents', (('Title', 'text'), ('Data', 'text')))
    # docs_db.drop_table('documents')
    # docs_db.show_tables()
    # docs_db.insert_data('documents', ('Test_title_1', 'Some_information_about_document_1'))
    # docs_db.get_all_table_data('documents')

    return app


@app_page.route('/')
def home():
    return render_template('app.html')


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
