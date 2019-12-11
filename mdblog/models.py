from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql.functions import current_timestamp

db = SQLAlchemy()

class Kalkulacka(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    creation_date = db.Column(db.DateTime, server_default=current_timestamp())