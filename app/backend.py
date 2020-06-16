import argparse
import json
import os
import datetime
from flask import Flask, g, jsonify, render_template, request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .models import Ideas
import time

app = Flask(__name__, static_folder='', static_url_path='')
app.config.from_object(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)
db.create_all()
db.session.commit()




# Setting up the app database


# def dbSetup():
#     connection = r.connect(host=RDB_HOST, port=RDB_PORT, db=PROJECT_DB ,user =DB_USER, password = DB_PASSWORD )
#     try:
#         r.db_create(PROJECT_DB).run(connection)
#         r.db(PROJECT_DB).table_create("ideas").run(connection)
#         print("Database setup completed. Now run the app without --setup.")
#     except RqlRuntimeError:
#         print("App database already exists. Run the app without --setup.")
#     finally:
#         connection.close()




# Managing connections

# The pattern we're using for managing database connections is to have **a connection per request**.
# We're using Flask's `@app.before_request` and `@app.teardown_request` for
# [opening a database connection](http://www.rethinkdb.com/api/python/connect/) and
# [closing it](http://www.rethinkdb.com/api/python/close/) respectively.
# @app.before_request
# def before_request():
#     try:
#         print("Requesting.....")
#         g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=PROJECT_DB ,user =DB_USER, password = DB_PASSWORD )
#         print(g.rdb_conn)
#     except RqlDriverError as e:
#         print("Errorr..........")
#         print(e)
#         print("No database connection could be established.")


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()

def retr_dict(obj=None):
    return_dict = {}
    if obj:
        return_dict['text'] = obj.text
        return_dict['tech'] = obj.tech
        return_dict['viewer'] = obj.viewer
        return_dict['time'] = obj.time
    return return_dict

@app.route("/livestream", methods=["GET"])
def get_todos():
    print("In Here......")
    try:
        selection = Ideas.query.order_by(Ideas.id).all()
        print("Objects %s ",selection)
        return_list = []
        for obj in selection:
            if obj.time:
                obj.time = obj.time.strftime("%d-%B-%Y, %I:%M:%S %p")
            return_list.append(retr_dict(obj=obj))
        print(return_list)
        return json.dumps(return_list)
    except Exception as e:
        print(e)
        return json.dumps({})

@app.route("/livestream", methods=["POST"])
def new_todo():
    print("Todo......")
    entry_data = request.json
    print(entry_data['text'])
    idea = Ideas(entry_data)
    db.session.add(idea)
    db.session.commit()
    print("Here......")
    return jsonify(id=idea.id)


@app.route("/")
def show_todos():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run the Flask todo app")
#     parser.add_argument("--setup", dest="run_setup", action="store_true")

#     args = parser.parse_args()
#     if args.run_setup:
#         dbSetup()
#     else:
#         app.run(debug=True)


