from app.backend import db
import datetime

class Ideas(db.Model):
    __tablename__ = 'ideas'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    tech = db.Column(db.String(200))
    viewer = db.Column(db.String(200))
    time = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, data = {}):
        self.text = data.get("text","")
        self.tech = data.get("tech","")
        self.viewer = data.get("viewer", "")
        self.time = data.get("time","")
        

        