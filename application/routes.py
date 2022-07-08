import os
from application import app,mysql,allowed_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import jsonify, request

@app.route('/')
def index():
    return " hello this is flask framework "
@app.route('/hello')
def hello_world():
    ip_addr = request.remote_addr
    return '<h1> Your IP address is:' + ip_addr

@app.route('/apilogin',methods=['POST'])
def apilogin():
    data = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    data.execute("SELECT nip FROM data WHERE nip = %s" , (nip,))
    datayangada = data.fetchall()
    if str(datayangada) == '()':
        return "maaf nip tida ada"
    else:
        data.execute("SELECT nip FROM data WHERE nip = %s and password = %s " , (nip,password,))
        datapswd = data.fetchall()
        if str(datapswd) == '()':
            return "maaf password salah"
        else:
            return "login berhasil"

@app.route('/apifoto',methods=['POST'])
def apifoto():
    data = mysql.connection.cursor()
    if 'image' not in request.files:
        return "tidak ada form image"
    file = request.files['image']
    if file.filename == '':
        return "tidak ada file image yang dipilih"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        data.execute("INSERT INTO dataabsen(foto) VALUES (%s)",(filename,))
        if mysql.connection.commit():
            print("oke")
        return "gambar telah terupload"
    else:
        return "bukan file image"
    
