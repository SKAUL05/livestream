import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder="", static_url_path="")
app.config.from_object(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)


class Ideas(db.Model):
    __tablename__ = "ideas"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    tech = db.Column(db.String(200))
    viewer = db.Column(db.String(200))
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    upVote = db.Column(db.Integer, default=0)

    def __init__(self, data={}):
        self.text = data.get("text", "")
        self.tech = data.get("tech", "")
        self.viewer = data.get("viewer", "")

    def retr_dict(self, obj=None):
        return_dict = {}
        if obj:
            return_dict["text"] = obj.text
            return_dict["tech"] = obj.tech
            return_dict["viewer"] = obj.viewer
            return_dict["time"] = obj.time
            return_dict["upVote"] = obj.upVote
        return return_dict
