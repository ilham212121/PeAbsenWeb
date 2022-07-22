import os
import string
from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL 
app = Flask(__name__)
mysql = MySQL()
FOLDER_ABSEN = 'application/static/upload/absen/'
FOLDER_PULANG = 'application/static/upload/pulang/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):     
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app.config['FOLDER_ABSEN'] = FOLDER_ABSEN
app.config['FOLDER_PULANG'] = FOLDER_PULANG
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
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = u"selamat datang"
login_manager.login_message_category = "info"
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        data = mysql.connection.cursor()
        data.execute("SELECT * FROM admin")
        datalogin = data.fetchall()
        return datalogin.query.get(int(user_id))
mysql.init_app(app)
from application import routes