import os
import string
from flask import Flask, jsonify, render_template, url_for
from flask_login import LoginManager
from flask_mysqldb import MySQL 
app = Flask(__name__)
mysql = MySQL()
FOLDER_ABSEN = 'application/static/assets/absen/'
FOLDER_PULANG = 'application/static/assets/pulang/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):     
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app.config['FOLDER_ABSEN'] = FOLDER_ABSEN
app.config['FOLDER_PULANG'] = FOLDER_PULANG
app.config['SECRET_KEY'] = 'bukan rahasia'
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']  = ''
app.config['MYSQL_DB'] = 'e_attandance'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config.update(dict(
SECRET_KEY="powerful secretkey",
WTF_CSRF_SECRET_KEY="wis tak omongi ora rahasia"
    ))
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = u"selamat datang"
login_manager.login_message_category = "info"
@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        data = mysql.connection.cursor()
        data.execute("SELECT * FROM admin")
        datalogin = data.fetchall()
        return datalogin.query.get(int(user_id))
from application.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
# bluprint for api in android users
from application.mobile import mobile as mobile_blueprint
app.register_blueprint(name="mobile",blueprint=mobile_blueprint)
# blueprint for non-auth parts of app
# blueprint for api in web users (CRUD)
from application.web import web as web_blueprint
app.register_blueprint(name="web",blueprint=web_blueprint)
@app.errorhandler(404)
def errorhandler(e):
    return render_template('404.html')
@app.errorhandler(401)
def errorhandler(e):
    return render_template('401.html')
@app.errorhandler(400)
def errorhandler(e):
    return jsonify({"msg":"server error"})
@app.errorhandler(500)
def errorhandler(e):
    return jsonify({"msg":"server error"})
login_manager.init_app(app)
mysql.init_app(app)
