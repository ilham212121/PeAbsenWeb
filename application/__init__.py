import os
from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL 
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
from application import routes