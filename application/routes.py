from application import app,mysql,data
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request

@app.route('/')
def index():
    return " hello this is flask framework "
@app.route('/hello')
def hello_world():
    ip_addr = request.remote_addr
    return '<h1> Your IP address is:' + ip_addr

@app.route('/apimysql',methods=['POST'])
def apimysql():
    data = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    data.execute("SELECT nip FROM data WHERE nip = %s" , (nip,))
    datayangada = data.fetchall()
    if str(datayangada) == '()':
        return "maaf nip tida ada"
    else:
        data.execute("SELECT nip FROM data WHERE email = %s and password = %s " , (nip,password,))
        datapswd = data.fetchall()
        if str(datapswd) == '()':
            return "maaf password salah"
        else:
            return "login berhasil"
    
