import os
from time import time
from flask_login import current_user
from sqlalchemy import case
from application import app,mysql,allowed_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import jsonify, make_response, redirect, render_template, request, session, url_for
import time
import datetime
from datetime import datetime
from functools import wraps
from flask_login import login_user, logout_user, login_required,current_user

def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        if nowTime < startTime:
            return "kamu absen terlalu cepat"
        if nowTime > endTime:
            return "kamu terlambat"
        if nowTime >= startTime and nowTime <= endTime:
            return "kamu absen tepat waktu"
        return 
    else: 
        return nowTime >= startTime or nowTime <= endTime
def isNowpulang(startTime, endTime, nowTime):
    if startTime < endTime:
        if nowTime < startTime:
            return "kamu pulang terlalu cepat"
        if nowTime > endTime:
            return "kamu pulang terlalu lambat dari jadwal apakah kamu lembur?"
        if nowTime >= startTime and nowTime <= endTime:
            return "kamu pulang sesuai jadwal shift"
        return 
    else: 
        return nowTime >= startTime or nowTime <= endTime
def roles_required(*role_names):
    def decorator(original_route):
        @wraps(original_route)
        def decorated_route(*args, **kwargs):
            if not session['loggedin'] == True:
                print('The user is not authenticated.')
                return redirect(url_for('index'))
            
            print(session['role'])
            print(role_names)
            if not session['role'] in role_names:
                print('The user does not have this role.')
                return redirect(url_for('index'))
            else:
                print('The user is in this role. ')
                return original_route(*args, **kwargs)
        return decorated_route
    return decorator
@app.route('/') 
def index():
    if session==None:
        return render_template('index.html')
    else:
        return render_template('index.html')
   
@app.errorhandler(404)
def errorhandler(e):
    return render_template('404.html')
@app.errorhandler(401)
def errorhandler(e):
    return render_template('401.html')
@app.errorhandler(500)
def errorhandler(e):
    return render_template('500.html')
def handle_error(error):
    if error.status_code == 404:
        return make_response(jsonify({ "error": { "code": 404, "message": "Not found" } }), 404)
    else:
        return make_response(jsonify({ "error": { "code": 500, "message": "Internal server error" } }), 500)
@app.route('/dashboard') 
@roles_required('admin','HRD','k_ruang') 
def dashboard():
    return render_template('dashboard/index.html')
@app.route('/data_admin') 
def data_admin():
    data = mysql.connection.cursor()
    data.execute("SELECT * FROM admin")
    admin = data.fetchall()
    return render_template('dashboard/data_admin.html',admin=admin)
@app.route('/data_hrd') 
def data_hrd():
    data = mysql.connection.cursor()
    data.execute("SELECT * FROM hrd")
    hrd = data.fetchall()
    return render_template('dashboard/data_hrd.html',hrd=hrd)
@app.route('/data_ka_ruang') 
def data_ka_ruang():
    data = mysql.connection.cursor()
    data.execute("SELECT * FROM ka_ruang")
    ka_ruang = data.fetchall()
    return render_template('dashboard/data_ka_ruang.html',ka_ruang=ka_ruang)
@app.route('/data_karyawan') 
def data_karyawan():
    data = mysql.connection.cursor()
    data.execute("SELECT * FROM karyawan")
    karyawan = data.fetchall()
    return render_template('dashboard/data_karyawan.html',karyawan=karyawan)
@app.route('/laporan_absen') 
def laporan_absen():
    data = mysql.connection.cursor()
    data.execute(
        'SELECT dataabsen.nip, karyawan.nama, karyawan.ruangan, karyawan.shift, dataabsen.lokasi,dataabsen.foto, dataabsen.tanggal,dataabsen.waktu, dataabsen.status'
        ' FROM dataabsen INNER JOIN karyawan ON dataabsen.nip = karyawan.nip'
        ' GROUP by tanggal desc, waktu desc')
    dataabsen = data.fetchall()
    return render_template('dashboard/laporan_absen.html',dataabsen=dataabsen)
@app.route('/laporan_pulang') 
def laporan_pulang():
    return render_template('dashboard/laporan_pulang.html')
@app.route('/hello')
def hello_world():
    ip_addr = request.remote_addr
    return '<h1> Your IP address is:' + ip_addr
@app.route('/api/login',methods=['POST'])
def apilogindashboard():
    data = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    data.execute("SELECT * FROM login WHERE nip = %s" , (nip,))
    datalogin = data.fetchall()
    if str(datalogin) == '()':
        data.close()
        return "maaf nip tida ada"
    elif not check_password_hash(datalogin[0][1],password):
        data.close()
        return "maaf password salah"
    else:
        if datalogin[0][2]=='admin':
            data.execute("SELECT login.nip,login.role, admin.nama,admin.email,admin.alamat,admin.kontak FROM login INNER JOIN admin ON login.nip = admin.nip WHERE login.nip = %s" , (nip,))
            datalogin= data.fetchall()
        elif datalogin[0][2]=='HRD':
            data.execute("SELECT login.nip,login.role, hrd.nama,hrd.email,hrd.alamat,hrd.kontak FROM login INNER JOIN hrd ON login.nip = hrd.nip WHERE login.nip = %s" , (nip,))
            datalogin= data.fetchall()
        elif datalogin[0][2]=='k_ruang':
            data.execute("SELECT login.nip,login.role, kep_ruang.nama,kep_ruang.email,kep_ruang.alamat,kep_ruang.kontak FROM login INNER JOIN kep_ruang ON login.nip = kep_ruang.nip WHERE login.nip = %s " , (nip,))
            datalogin= data.fetchall()
        else:
            return "maaf nip tida ada"
        session['loggedin'] = True
        session['id'] = datalogin[0][0]
        session['role'] = datalogin[0][1]
        session['username'] = datalogin[0][2]
        data.close()
        return redirect(url_for('dashboard'))
@app.route('/api/login/karyawan',methods=['POST'])
def apilogin():
    data = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    data.execute("SELECT * FROM login WHERE role='karyawan', nip = %s" , (nip,))
    datalogin= data.fetchall()
    if str(datalogin) == '()':
        data.close()
        print("maaf nip tidak ada")
        return jsonify({"msg":"maaf nip tidak ada"})
    elif not check_password_hash(datalogin[0][1],password):
        data.close()
        print("maaf password salah")
        return jsonify({"msg":"maaf password salah"})
    else:
        data.execute("SELECT * FROM karyawan WHERE nip = %s" , (nip,))
        datalogin = data.fetchall()
        data.close()
        return jsonify({"data":[{"nip":datalogin[0][0],"nama":datalogin[0][1],"posisi":datalogin[0][2],"gender":datalogin[0][3],"ttl":datalogin[0][4],"email":datalogin[0][5],"no_hp":datalogin[0][6],"alamat":datalogin[0][7]}],"msg":"login berhasil"})
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('role', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('index'))
@app.route('/apiabsen',methods=['POST'])
def apiabsen():
    data = mysql.connection.cursor()
    if 'image' not in request.files:
        data.close()
        return jsonify({"msg":"tidak ada form image"})
    file = request.files['image']
    nip=request.form['nip']
    latitude=request.form['latitude']
    longitude= request.form['longitude']
    
    if file.filename == '':
        data.close()
        return jsonify({"msg":"tidak ada file image yang dipilih"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(file.filename)
        data.execute("SELECT shift from shift where nip= %s",(nip,))
        shift = data.fetchall()
        a=time.localtime()
        hr=a.tm_hour
        mn=a.tm_min
        thn=a.tm_year
        bln=a.tm_mon
        hari=a.tm_mday
        tanggal=""+str(thn)+"-"+str(bln)+"-"+str(hari)+""
        print(tanggal)
        data.execute("SELECT * from dataabsen where nip= %s and tanggal = %s ",(nip,tanggal))
        cek = data.fetchall()
        if hr>=12:
            if hr==12:
                hr=12
            else:
                hr = hr-12
            w='PM'
        else:
            if hr==0:
                hr=12
            w='AM'
        if str(cek) == '()':
            timeNow = str(hr)+':'+str(mn)+str(w)+''
            renamefile= secure_filename(str(nip)+str(tanggal)+str(timeNow)+".jpg")
            print(renamefile)
            print(timeNow)
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
                
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], renamefile))
            print(renamefile)
            if status=='kamu absen terlalu cepat':
                data.close()
                return jsonify({"msg":status})
            if status=="kamu terlambat":
                statusdb="telat"
                data.execute("INSERT INTO dataabsen(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                if mysql.connection.commit():
                    data.close()
                return jsonify({"msg":status})
            if status=="kamu absen tepat waktu":
                statusdb="tepat waktu"
                data.execute("INSERT INTO dataabsen(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                if mysql.connection.commit():
                    data.close()
                return jsonify({"msg":status})
        else:
             return jsonify({"msg":"maaf kamu sudah absen"})
    else:
        data.close()
        return "foto yang anda kirim invalid"
@app.route('/apipulang',methods=['POST'])
def apipulang():
    data = mysql.connection.cursor()
    if 'image' not in request.files:
        data.close()
        return "tidak ada form image"
    file = request.files['image']
    nip=request.form['nip']
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
        det=a.tm_sec
        thn=a.tm_year
        bln=a.tm_mon
        hari=a.tm_mday

        tanggal=""+str(thn)+"-"+str(bln)+"-"+str(hari)+""
        print(tanggal)
        data.execute("SELECT * from datapulang where nip= %s and tanggal = %s ",(nip,tanggal))
        cek = data.fetchall()
        if hr>=12:
            if hr==12:
                hr=12
            else:
                hr = hr-12
            w='PM'
        else:
            if hr==0:
                hr=12
            w='AM'
        if str(cek) == '()':
            timeNow = str(hr)+':'+str(mn)+str(w)+''
            print(timeNow)
            timeNow = datetime.strptime(timeNow, "%I:%M%p")
            if shift[0][0]=="pagi":
                timeStart = '02:00PM'
                timeEnd = '02:18PM'
                timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
                timeStart = datetime.strptime(timeStart, "%I:%M%p")
                status=isNowpulang(timeStart, timeEnd, timeNow)
                
            elif shift[0][0]=="siang":
                timeStart = '09:00PM'
                timeEnd = '09:18PM'
                timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
                timeStart = datetime.strptime(timeStart, "%I:%M%p")
                status=isNowpulang(timeStart, timeEnd, timeNow)
                
            elif shift[0][0]=="middle":
                timeStart = '05:00PM'
                timeEnd = '05:18PM'
                timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
                timeStart = datetime.strptime(timeStart, "%I:%M%p")
                status=isNowpulang(timeStart, timeEnd, timeNow)
    
            elif shift[0][0]=="malam":
                timeStart = '07:00AM'
                timeEnd = '07:18AM'
                timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
                timeStart = datetime.strptime(timeStart, "%I:%M%p")
                status=isNowpulang(timeStart, timeEnd, timeNow)
                
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            timeNow = str(hr)+':'+str(mn)+str(det)+str(w)+''
            if status=='kamu pulang terlalu cepat':
                statusdb="terlalu cepat"
                data.execute("INSERT INTO datapulang(nip,lokasi,tanggal,waktu,foto,status) VALUES (%s,ST_GeomFromText(%s),%s,%s,%s,%s)",(nip,lokasi,tanggal,timeNow,filename,statusdb))
                if mysql.connection.commit():
                    data.close()
                return jsonify({"msg":status})
            if status=="kamu pulang terlalu lambat dari jawdwal apakah kamu lembur?":
                statusdb="lembur?"
                data.execute("INSERT INTO datapulang(nip,lokasi,tanggal,waktu,foto,status) VALUES (%s,ST_GeomFromText(%s),%s,%s,%s,%s)",(nip,lokasi,tanggal,timeNow,filename,statusdb))
                if mysql.connection.commit():
                    data.close()
                return jsonify({"msg":status})
            if status=="kamu pulang sesuai jadwal shift":
                statusdb="tepat waktu"
                data.execute("INSERT INTO datapulang(nip,lokasi,tanggal,waktu,foto,status) VALUES (%s,ST_GeomFromText(%s),%s,%s,%s,%s)",(nip,lokasi,tanggal,timeNow,filename,statusdb))
                if mysql.connection.commit():
                    data.close()
                return jsonify({"msg":status})
        else:
             return jsonify({"msg":"maaf anda sudah absen pulang"})
    else:
        data.close()
        return "foto yang anda kirim invalid"

@app.route('/cetak_laporan') 
def cetak_laporan():
    return render_template('dashboard/charts.html')
@app.route('/cetak_data') 
def cetak_data():
    return render_template('dashboard/tables.html')
    
