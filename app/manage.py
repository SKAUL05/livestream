import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.backend import app,db

app.config.from_object(__name__)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
