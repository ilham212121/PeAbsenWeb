import os,pymongo
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mysqldb import MySQL 
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *
from pybigquery.api import ApiClient
app = Flask(__name__)
db= SQLAlchemy()
mysql = MySQL()
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
mongo = os.getenv('mongodb://localhost:27017')
client = pymongo.MongoClient(mongo)
dbmongo = client['data'] # Mongo collection
nama = dbmongo['nama'] # Mongo document
users = dbmongo['email'] # Mongo document
password = dbmongo['password'] # Mongo document
no_rumah = dbmongo['no_rumah'] # Mongo document
kontak = dbmongo['kontak'] # Mongo document
UPLOAD_FOLDER = 'application/static/upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'bukan rahasia'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Pe_Absen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']  = ''
app.config['MYSQL_DB'] = 'pe_absen'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config.update(dict(
SECRET_KEY="powerful secretkey",
WTF_CSRF_SECRET_KEY="wis tak omongi ora rahasia"
    ))
db.init_app(app)
mysql.init_app(app)
from application.models import data

from application import routes