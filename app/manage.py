import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import Ideas

app = Flask(__name__, static_folder="", static_url_path="")
app.config.from_object(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)
app.config.from_object(__name__)
MIGRATION_DIR = os.path.join("app", "migrations")
migrate = Migrate(app, db, dirctory=MIGRATION_DIR)
manager = Manager(app)

manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()
