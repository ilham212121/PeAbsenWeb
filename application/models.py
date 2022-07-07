from flask_login import UserMixin
from application import db
class data(UserMixin, db.Model):
    nip=db.Column(db.String(100), primary_key=True) # primary keys are required by SQLAlchemy
    nama = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    no_rumah = db.Column(db.String(1000))
    kontak = db.Column(db.String(1000))