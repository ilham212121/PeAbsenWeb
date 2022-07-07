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
mysql = MySQL()
UPLOAD_FOLDER = 'application/static/upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'bukan rahasia'
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']  = ''
app.config['MYSQL_DB'] = 'pe_absen'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config.update(dict(
SECRET_KEY="powerful secretkey",
WTF_CSRF_SECRET_KEY="wis tak omongi ora rahasia"
    ))
mysql.init_app(app)
from application.models import data

from application import routes