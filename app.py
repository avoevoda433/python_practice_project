from flask import Flask, Blueprint, render_template
from database.database import Database


app_page = Blueprint('app', __name__, template_folder='templates/layouts')


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.register_blueprint(app_page)

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


if __name__ == '__main__':
    create_app().run()
