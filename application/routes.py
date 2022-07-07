from email import message
from application import app,db,mysql,data,users,dbmongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request

@app.route('/')
def index():
    return " hello this is flask framework "
@app.route('/hello')
def hello_world():
    ip_addr = request.remote_addr
    return '<h1> Your IP address is:' + ip_addr
@app.route('/apisqlite',methods=['POST'])
def apisqlite():
    nip = request.form['nip']
    password = request.form['password']
    datadb = data.query.filter_by(nip=nip).first() 
    if not datadb:
        return 'NIP tidak ditemukan'
    elif not check_password_hash(datadb.password, password):
        return "password salah"
    return "login berhasil"

@app.route('/apimysql',methods=['POST'])
def apimysql():
    data = mysql.connection.cursor()
    email = request.form['email']
    nama = request.form['nama']
    password = request.form['password']
    no_rumah = request.form['no_rumah']
    kontak = request.form['kontak']
    data.execute("SELECT email FROM data WHERE email= %s " , (email,))
    datayangada = data.fetchall()
    if str(datayangada) == '()':
        data.execute("INSERT INTO data (nama,email,password,no_rumah,kontak) values (%s,%s,%s,%s,%s)",(nama,email,password,no_rumah,kontak))
        mysql.connection.commit()
        return "Data Telah Disimpan"
    else:
        return "maaf email sudah ada"
@app.route('/apimongo',methods=['POST'])
def apimongo():
    email = request.form['email']
    nama = request.form['nama']
    password = request.form['password']
    no_rumah = request.form['no_rumah']
    kontak = request.form['kontak']    
    email = users.find_one({"email": email})
    if email:
        return 'This email is already exist.'
    new_data = {
            'nama':nama,
            'email': email,
            'password': password,
            'no_rumah': no_rumah,
            'kontak': kontak,
        }
    users.insert_one(new_data)
    return ''+new_data['nama'] + ' user has been added. success'
    
