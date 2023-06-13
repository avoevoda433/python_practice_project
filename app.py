from flask import Flask, Blueprint, render_template
import psycopg2
import csv


app_page = Blueprint('app', __name__, template_folder='templates/layouts')

conn = psycopg2.connect(database="docs_db", user="postgres",
                        password="`1qazxsw2", host="localhost", port="5432")

cur = conn.cursor()
cur.execute(
    '''CREATE TABLE IF NOT EXISTS documents (id serial \
    PRIMARY KEY, rubrics varchar(100), text text, created_date timestamp);''')

with open('posts.csv', newline='', encoding='utf-8') as File:
    file = list(csv.reader(File))[1:]
    for row in file:
        row[0] = row[0].replace("\'", '\"')
        row[1] = row[1].replace("\'", '\"')
        row[2] = row[2].replace("\'", '\"')
        cur.execute(
            f"INSERT INTO documents (rubrics, text, created_date) VALUES ('{row[2]}', '{row[0]}', '{row[1]}');")

conn.commit()
cur.close()
conn.close()


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
    conn = psycopg2.connect(database="docs_db", user="postgres",
                            password="`1qazxsw2", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM documents''')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('app.html', data=data)


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
