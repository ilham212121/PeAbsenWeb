import os

from flask_login import current_user
from application import app,mysql,allowed_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import jsonify, redirect, render_template, request, url_for

@app.route('/') 
def index():
    return render_template('index.html')
@app.route('/login')
def login():
      if current_user.is_authenticated:
          return redirect(url_for('dashboard'))
      return render_template('login.html')
@app.route('/dashboard') 
def dashboard():
    
    return render_template('admin/index.html')
@app.route('/laporan_absen') 
def laporan_absen():
    data = mysql.connection.cursor()
    data.execute("SELECT * FROM dataabsen")
    dataabsen = data.fetchall()
    return render_template('admin/lapran_absen.html',dataabsen=dataabsen)
@app.route('/laporan_pulang') 
def laporan_pulang():
    return render_template('admin/laporan_pulang.html')
@app.route('/hello')
def hello_world():
    ip_addr = request.remote_addr
    return '<h1> Your IP address is:' + ip_addr
@app.route('/api/login/admin',methods=['POST'])
def api_login_admin():
    data = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    data.execute("SELECT * FROM data WHERE nip = %s" , (nip,))
    datayangada = data.fetchall()
    if str(datayangada) == '()':
        data.close()
        return "maaf nip tida ada"
    elif not check_password_hash(datayangada[0][3],password):
        data.close()
        return "maaf password salah"
    else:
        data.close()
        return "login berhasil"
@app.route('/api/login/hrd',methods=['POST'])
def api_login_hrd():
    data = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    data.execute("SELECT * FROM data WHERE nip = %s" , (nip,))
    datayangada = data.fetchall()
    if str(datayangada) == '()':
        data.close()
        return "maaf nip tida ada"
    elif not check_password_hash(datayangada[0][3],password):
        data.close()
        return "maaf password salah"
    else:
        data.close()
        return "login berhasil"
@app.route('/api/login/k_ruang',methods=['POST'])
def api_login_k_ruang():
    data = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    data.execute("SELECT * FROM data WHERE nip = %s" , (nip,))
    datayangada = data.fetchall()
    if str(datayangada) == '()':
        data.close()
        return "maaf nip tida ada"
    elif not check_password_hash(datayangada[0][3],password):
        data.close()
        return "maaf password salah"
    else:
        data.close()
        return "login berhasil"

@app.route('/apilogin',methods=['POST'])
def apilogin():
    data = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    data.execute("SELECT * FROM data WHERE nip = %s" , (nip,))
    datayangada = data.fetchall()
    if str(datayangada) == '()':
        data.close()
        return "maaf nip tida ada"
    elif not check_password_hash(datayangada[0][3],password):
        data.close()
        return "maaf password salah"
    else:
        data.close()
        return "login berhasil"

@app.route('/apifoto',methods=['POST'])
def apifoto():
    data = mysql.connection.cursor()
    if 'image' not in request.files:
        data.close()
        return "tidak ada form image"
    file = request.files['image']
    if file.filename == '':
        data.close()
        return "tidak ada file image yang dipilih"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        data.execute("INSERT INTO dataabsen(foto) VALUES (%s)",(filename,))
        if mysql.connection.commit():
            data.close()
            print("oke")
        return "gambar telah terupload"
    else:
        data.close()
        return "bukan file image"
    
