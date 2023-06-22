from flask import Flask, Blueprint, render_template, request, redirect
from database.database import Database
from database.elastic import Elastic


app_page = Blueprint('app', __name__, template_folder='templates/layouts')
docs_db = Database(db_name="docs_db", user="postgres",
                   password="`1qazxsw2", host="localhost", port="5432")
es = Elastic('http://localhost:9200', 'my_index')


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.register_blueprint(app_page)
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(404, page_not_found)
    docs_db.create_table()
    if not len(docs_db.get_all_table_data()):
        docs_db.insert_data()
        print(len(docs_db.get_all_table_data()))
        for row in docs_db.get_all_table_data():
            es.add_index(id_ind=str(row[0]), data={'text': str(row[2])})
    return app


# @app_page.route('/')
# def home():
#     return render_template('app.html', data=[])


@app_page.route('/', methods=['GET', 'POST'])
def find():
    if not request.args.get("search"):
        return render_template('app.html', data=[])
    if request.method == 'GET':
        res = es.find_document(request.args.get('search'))
        doc_id = [i['_id'] for i in res['hits']['hits']]
        data = [docs_db.get_dock_by_id(i) for i in doc_id if int(i) <= 1500]
        data.sort(key=lambda x: x[0][3])
        return render_template('app.html', data=data)
    elif request.method == 'POST':
        docs_db.delete_by_id(request.args.get("search"))
        es.delete(request.args.get("search"))
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
