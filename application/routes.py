import os
from time import time
from flask_login import current_user
from sqlalchemy import case
from application import app,mysql,allowed_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import jsonify, redirect, render_template, request, url_for
import time
import datetime
from datetime import datetime
def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        if nowTime < startTime:
            return "kamu absen terlalu cepat"
        if nowTime > endTime:
            return "kamu terlambat"
        if nowTime >= startTime and nowTime <= endTime:
            return "kamu absen tepat waktu"
        return 
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime
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
    return render_template('admin/laporan_absen.html',dataabsen=dataabsen)
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

@app.route('/api/login/karyawan',methods=['POST'])
def apilogin():
    data = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    data.execute("SELECT * FROM karyawan WHERE nip = %s" , (nip,))
    datayangada = data.fetchall()
    if str(datayangada) == '()':
        data.close()
        print("maaf nip tidak ada")
        return jsonify({"msg":"maaf nip tidak ada"})
    elif not check_password_hash(datayangada[0][2],password):
        data.close()
        print("maaf password salah")
        return jsonify({"msg":"maaf password salah"})
    else:
        data.close()
        return jsonify({"data":datayangada,"msg":"login berhasil"})

@app.route('/apiabsen',methods=['POST'])
def apiabsen():
    data = mysql.connection.cursor()
    if 'image' not in request.files:
        data.close()
        return "tidak ada form image"
    file = request.files['image']
    nip=request.form['nip']
    nama=request.form['nama']
    ruangan= request.form['ruangan']
    lokasi=request.form['lokasi']
    lokasi="POINT("+lokasi+")"
    
    if file.filename == '':
        data.close()
        return "tidak ada file image yang dipilih"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        data.execute("SELECT shift from karyawan where nip= %s",(nip,))
        shift = data.fetchall()
        a=time.localtime()
        hr=a.tm_hour
        mn=a.tm_min
        if hr>=12:
            hr= hr-12
            w='PM'
        else:
            w='AM'
        timeNow = '{}:{}{}'.format(hr,mn,w)
        timeNow = datetime.strptime(timeNow, "%I:%M%p")
        if shift[0][0]=="pagi":
            timeStart = '06:30AM'
            timeEnd = '07:10AM'
            timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
            timeStart = datetime.strptime(timeStart, "%I:%M%p")
            status=isNowInTimePeriod(timeStart, timeEnd, timeNow)
            
        elif shift[0][0]=="siang":
            timeStart = '01:30PM'
            timeEnd = '02:10PM'
            timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
            timeStart = datetime.strptime(timeStart, "%I:%M%p")
            status=isNowInTimePeriod(timeStart, timeEnd, timeNow)
            
        elif shift[0][0]=="middle":
            timeStart = '09:30AM'
            timeEnd = '10:10AM'
            timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
            timeStart = datetime.strptime(timeStart, "%I:%M%p")
            status=isNowInTimePeriod(timeStart, timeEnd, timeNow)

        elif shift[0][0]=="malam":
            timeStart = '09:30PM'
            timeEnd = '10:10PM'
            timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
            timeStart = datetime.strptime(timeStart, "%I:%M%p")
            status=isNowInTimePeriod(timeStart, timeEnd, timeNow)
            
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        if status=='kamu absen terlalu cepat':
            data.close()
            return status
        if status=="kamu terlambat":
            statusdb="telat"
            data.execute("INSERT INTO dataabsen(nip,nama,ruangan,lokasi,waktu,foto,status) VALUES (%s,%s,%s,ST_GeomFromText(%s),%s,%s,%s)",(nip,nama,ruangan,lokasi,timeNow,filename,statusdb))
            if mysql.connection.commit():
                data.close()
            return status
        if status=="kamu absen tepat waktu":
            statusdb="tepat waktu"
            data.execute("INSERT INTO dataabsen(nip,nama,ruangan,lokasi,waktu,foto,status) VALUES (%s,%s,%s,ST_GeomFromText(%s),%s,%s,%s)",(nip,nama,ruangan,lokasi,timeNow,filename,statusdb))
            if mysql.connection.commit():
                data.close()
            return status
    else:
        data.close()
        return "foto yang anda kirim invalid"

@app.route('/cetak_laporan') 
def cetak_laporan():
    return render_template('index.html')
@app.route('/cetak_data') 
def cetak_data():
    return render_template('index.html')
@app.route('/data_karyawan') 
def data_karyawan():
    return render_template('index.html')
@app.route('/data_ka_ruang') 
def data_ka_ruang():
    return render_template('index.html')
@app.route('/data_hrd') 
def data_hrd():
    return render_template('index.html')
@app.route('/data_admin') 
def data_admin():
    return render_template('index.html')

    
