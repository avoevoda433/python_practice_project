from http import HTTPStatus
import elasticsearch
import psycopg2.errors
from flask import Flask, Blueprint, render_template, request
from flask_restx import Api, fields, Resource, abort
from database.database import Database
from database.elastic import Elastic
import config_data


blueprint = Blueprint('app', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='1.0', title='Docs find API')
ns = api.namespace('docs', description='Docs operations')
api.add_namespace(ns)
docs_db = Database(db_name=config_data.db_name, user=config_data.db_user,
                   password=config_data.db_password, host=config_data.db_host, port=config_data.db_port)
es = Elastic(f'http://{config_data.elastic_port}:{config_data.elastic_port}', config_data.elastic_index)


docs_model = api.model('Docs',
                       {'id': fields.String,
                        'rubrics': fields.String,
                        'text': fields.String,
                        'created_date': fields.String})

docs_parser = api.parser()
docs_parser.add_argument('id', type=str, location='form')
docs_parser.add_argument('rubrics', type=str, location='form')
docs_parser.add_argument('text', type=str, location='form')
docs_parser.add_argument('created_date', type=str, location='form')


@ns.route('/')
class DocsApi(Resource):
    @api.response(HTTPStatus.OK.value, "Get the docs list")
    @api.marshal_list_with(docs_model)
    def get(self):
        try:
            docs = docs_db.get_all_table_data()
            answer = [{
                'id': doc[0],
                'rubrics': doc[1],
                'text': doc[2],
                'created_date': doc[3]
            } for doc in docs]
            return answer
        except psycopg2.errors.UndefinedTable:
            return abort(HTTPStatus.BAD_REQUEST.value, 'Table not found')


@ns.route('/<int:doc_id>')
class DocApi(Resource):
    @api.response(HTTPStatus.OK.value, "Get the doc list")
    @api.response(HTTPStatus.BAD_REQUEST.value, "Doc not found")
    @api.marshal_with(docs_model)
    def get(self, doc_id: int):
        try:
            doc = docs_db.get_dock_by_id(str(doc_id))[0]
            answer = [{
                'id': doc[0],
                'rubrics': doc[1],
                'text': doc[2],
                'created_date': doc[3]
            }]
            return answer
        except IndexError:
            return abort(HTTPStatus.BAD_REQUEST.value, 'Doc not found')

    @api.response(HTTPStatus.OK.value, "Delete the doc")
    @api.response(HTTPStatus.BAD_REQUEST.value, "Doc not delete")
    @api.marshal_with(docs_model)
    def delete(self, doc_id: int):
        try:
            docs_db.delete_by_id(str(doc_id))
            es.delete(str(doc_id))
            return abort(HTTPStatus.OK.value, 'Delete the doc')
        except elasticsearch.NotFoundError:
            return abort(HTTPStatus.BAD_REQUEST.value, 'Doc not delete')


@ns.route('/search')
class SearchDocsApi(Resource):
    @api.response(HTTPStatus.OK.value, "Get the search doc list")
    @api.response(HTTPStatus.BAD_REQUEST.value, "Docs not found")
    @api.marshal_with(docs_model)
    def get(self):
        try:
            json_data = request.get_json()
            search_response = json_data['response']
            res = es.find_document(search_response)
            doc_id = [i['_id'] for i in res['hits']['hits']]
            docs = [docs_db.get_dock_by_id(i) for i in doc_id if int(i) <= 1500]
            docs.sort(key=lambda x: x[0][3])
            answer = [{
                'id': doc[0][0],
                'rubrics': doc[0][1],
                'text': doc[0][2],
                'created_date': doc[0][3]
            } for doc in docs]
            return answer
        except elasticsearch.ApiError:
            return abort(HTTPStatus.BAD_REQUEST.value, 'Docs not found')


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.register_blueprint(blueprint)
    docs_db.create_table()
    if not len(docs_db.get_all_table_data()):
        docs_db.insert_data()
        for row in docs_db.get_all_table_data():
            es.add_index(id_ind=str(row[0]), data={'text': str(row[2])})
    return app


if __name__ == '__main__':
    create_app().run()
