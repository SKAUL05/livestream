import argparse
import json
import os
from datetime import datetime, timedelta
from flask import Flask, g, jsonify, render_template, request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .models import Ideas
import time

app = Flask(__name__, static_folder="", static_url_path="")
app.config.from_object(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)


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





@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()


def retr_dict(obj=None):
    return_dict = {}
    if obj:
        return_dict["id"] = obj.id
        return_dict["text"] = obj.text
        return_dict["tech"] = obj.tech
        return_dict["viewer"] = obj.viewer
        return_dict["count"] = obj.upVote
        if obj.time:
            readable = obj.time + timedelta(hours=5) + timedelta(minutes=30)
            return_dict["time"] = readable.strftime("%d-%B-%Y, %I:%M:%S %p")
        else:
            retr_dict["time"] = "None"
    return return_dict


@app.route("/livestream", methods=["GET"])
def get_todos():
    print("In Here......")
    try:
        selection = Ideas.query.order_by(Ideas.id).all()
        print("Objects %s ", selection)
        return_list = []
        for obj in selection:
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
    print(entry_data["text"])
    idea = Ideas(entry_data)
    db.session.add(idea)
    db.session.commit()
    print("Here......")
    return jsonify(id=idea.id)


@app.route("/upvote", methods=["POST"])
def add_upvote():
    
    u_data = request.json
    obj = Ideas.query.filter_by(id=u_data["id"]).first()
    print(obj.upVote)
    print(type(obj.upVote))
    if obj.upVote is not None:
        obj.upVote += 1
    else:
        obj.upVote = 1

    db.session.commit()
    return jsonify(count=obj.upVote)


@app.route("/")
def show_todos():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 8080)))
