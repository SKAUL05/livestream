import argparse
import json
import os
from datetime import datetime
from flask import Flask, g, jsonify, render_template, request, abort

import rethinkdb as rdb
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

r = rdb.RethinkDB()

# Connection details

# We will use these settings later in the code to connect to the
# RethinkDB server.
RDB_HOST = os.environ.get("RDB_HOST", "localhost")
RDB_PORT = os.environ.get("RDB_PORT", 28015)
PROJECT_DB = os.environ.get("PROJECT_DB","livestream")
DB_USER = os.environ.get("PROJECT_USER","")
DB_PASSWORD = os.environ.get("PROJECT_PASSWORD","")

# Setting up the app database


def dbSetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT, db=PROJECT_DB ,user =DB_USER, password = DB_PASSWORD )
    try:
        r.db_create(PROJECT_DB).run(connection)
        r.db(PROJECT_DB).table_create("ideas").run(connection)
        print("Database setup completed. Now run the app without --setup.")
    except RqlRuntimeError:
        print("App database already exists. Run the app without --setup.")
    finally:
        connection.close()


app = Flask(__name__, static_folder='', static_url_path='')
app.config.from_object(__name__)


# Managing connections

# The pattern we're using for managing database connections is to have **a connection per request**.
# We're using Flask's `@app.before_request` and `@app.teardown_request` for
# [opening a database connection](http://www.rethinkdb.com/api/python/connect/) and
# [closing it](http://www.rethinkdb.com/api/python/close/) respectively.
@app.before_request
def before_request():
    try:
        print("Requesting.....")
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=PROJECT_DB ,user =DB_USER, password = DB_PASSWORD )
        print(g.rdb_conn)
    except RqlDriverError as e:
        print("Errorr..........")
        print(e)
        print("No database connection could be established.")


@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


@app.route("/livestream", methods=["GET"])
def get_todos():
    selection = list(r.table("ideas").run(g.rdb_conn))
    print(selection)
    for obj in selection:
        if obj.get("time"):
            obj["time"] = obj["time"].strftime("%d-%B-%Y, %I:%M:%S %p")
    print(selection)
    return json.dumps(selection)


@app.route("/livestream", methods=["POST"])
def new_todo():
    entry_data = request.json
    entry_data["time"] = r.expr(datetime.now(r.make_timezone("+05:30")))
    inserted = r.table("ideas").insert(request.json).run(g.rdb_conn)
    return jsonify(id=inserted["generated_keys"][0])


@app.route("/")
def show_todos():
    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Flask todo app")
    parser.add_argument("--setup", dest="run_setup", action="store_true")

    args = parser.parse_args()
    if args.run_setup:
        dbSetup()
    else:
        app.run(debug=True)


# ### Best practices ###
#
# #### Managing connections: a connection per request ####
#
# The RethinkDB server doesn't use a thread-per-connnection approach
# so opening connections per request will not slow down your database.
#
# #### Fetching multiple rows: batched iterators ####
#
# When fetching multiple rows from a table, RethinkDB returns a
# batched iterator initially containing a subset of the complete
# result. Once the end of the current batch is reached, a new batch is
# automatically retrieved from the server. From a coding point of view
# this is transparent:
#
#     for result in r.table('todos').run(g.rdb_conn):
#         print result
#
#
# #### `replace` vs `update` ####
#
# Both `replace` and `update` operations can be used to modify one or
# multiple rows. Their behavior is different:
#
# *   `replace` will completely replace the existing rows with new values
# *   `update` will merge existing rows with the new values


#
# Licensed under the MIT license: <http://opensource.org/licenses/mit-license.php>
#
# Copyright (c) 2012 RethinkDB
#
