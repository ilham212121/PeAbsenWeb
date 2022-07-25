import os
import re
from time import time
from urllib.request import DataHandler
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

def isNowTanggal(startTgl, endTgl, nowTgl):
    if startTgl < endTgl:
        if nowTgl < startTgl:
            return "tgl"
        if nowTgl > endTgl:
            return "kamu terlambat"
        if nowTgl >= startTgl and nowTgl <= endTgl:
            return "kamu absen tepat waktu"
        return 
    else: 
        return nowTgl >= startTgl or nowTgl <= endTgl
def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        if nowTime < startTime:
            wait=startTime-nowTime
            return "kamu absen terlalu cepat silahkan tunggu "+wait+" lagi"
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
            if 'loggedin' in session:
            # User is loggedin show them the home page
                if not session['role'] in role_names:
                    print('The user does not have this role.')
                    return redirect(url_for('index'))
                else:
                    print('The user is in this role.')
                    return original_route(*args, **kwargs)
            else:
                return redirect(url_for('index'))
        return decorated_route
    return decorator
@app.route('/') 
def index():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        role_names=['admin','HRD','karu']
        if not session['role'] in role_names:
            print('The user does not have this role.')
            return redirect(url_for('index'))
        else:
            print('The user is in this role.')
            return render_template('dashboard/index.html', username=session['username'])
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
@app.route('/dashboard') 
def dashboard():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        role_names=['admin','HRD','karu']
        if not session['role'] in role_names:
            print('The user does not have this role.')
            return redirect(url_for('index'))
        else:
            print('The user is in this role.')
            return render_template('dashboard/index.html', username=session['username'])
    else:
        return redirect(url_for('index'))
@app.route('/data_admin') 
@roles_required('admin')
def data_admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin")
    admin = cur.fetchall()
    return render_template('dashboard/data_admin.html',admin=admin)
@app.route('/data_hrd')
@roles_required('admin','HRD')
def data_hrd():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hrd")
    hrd = cur.fetchall()
    return render_template('dashboard/data_hrd.html',hrd=hrd)
@app.route('/data_karu') 
@roles_required('admin','HRD','karu')
def data_karu():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM karu")
    karu = cur.fetchall()
    return render_template('dashboard/data_karu.html',karu=karu)
@app.route('/data_karyawan') 
@roles_required('admin','HRD','karu')
def data_karyawan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM karyawan")
    karyawan = cur.fetchall()
    return render_template('dashboard/data_karyawan.html',karyawan=karyawan)
@app.route('/laporan_absen') 
@roles_required('admin','HRD','karu')
def laporan_absen():
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT `id`, dataabsen.nip, karyawan.nama,shift.ruangan,shift.shift,`latitude`, `longitude`, `foto`, `tanggal`, `waktu`, `status`'
        ' FROM dataabsen INNER JOIN shift on dataabsen.nip = shift.nip INNER JOIN karyawan ON dataabsen.nip = karyawan.nip '
        ' GROUP by tanggal desc, waktu desc')
    dataabsen = cur.fetchall()
    return render_template('dashboard/laporan_absen.html',dataabsen=dataabsen)
@app.route('/laporan_pulang') 
@roles_required('admin','HRD','karu')
def laporan_pulang():
    return render_template('dashboard/laporan_pulang.html')
@app.route('/api/login',methods=['POST'])
def apilogindashboard():
    cur = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    cur.execute("SELECT * FROM login WHERE nip = %s" , (nip,))
    datalogin = cur.fetchall()
    if str(datalogin) == '()':
        cur.close()
        return "maaf nip tida ada"
    elif not check_password_hash(datalogin[0][1],password):
        cur.close()
        return "maaf password salah"
    else:
        if datalogin[0][2]=='admin':
            cur.execute("SELECT login.nip,login.role, admin.nama,admin.email,admin.alamat,admin.no_hp FROM login INNER JOIN admin ON login.nip = admin.nip WHERE login.nip = %s" , (nip,))
            datalogin= cur.fetchall()
        elif datalogin[0][2]=='HRD':
            cur.execute("SELECT login.nip,login.role, hrd.nama,hrd.email,hrd.alamat,hrd.no_hp FROM login INNER JOIN hrd ON login.nip = hrd.nip WHERE login.nip = %s" , (nip,))
            datalogin= cur.fetchall()
        elif datalogin[0][2]=='karu':
            cur.execute("SELECT login.nip,login.role, karu.nama,karu.email,karu.alamat,karu.no_hp FROM login INNER JOIN karu ON login.nip = karu.nip WHERE login.nip = %s " , (nip,))
            datalogin= cur.fetchall()
        else:
            return "maaf nip tida ada"
        session['loggedin'] = True
        session['id'] = datalogin[0][0]
        session['role'] = datalogin[0][1]
        session['username'] = datalogin[0][2]
        cur.close()
        return redirect(url_for('dashboard'))
@app.route('/api/login/karyawan',methods=['POST'])
def apilogin():
    cur = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    cur.execute("SELECT * FROM login WHERE role='karyawan'and nip = %s" , (nip,))
    datalogin= cur.fetchall()
    if str(datalogin) == '()':
        cur.close()
        print("maaf nip tidak ada")
        return jsonify({"msg":"maaf nip tidak ada"})
    elif not check_password_hash(datalogin[0][1],password):
        cur.close()
        print("maaf password salah")
        return jsonify({"msg":"maaf password salah"})
    else:
        cur.execute("SELECT * FROM karyawan WHERE nip = %s" , (nip,))
        datalogin = cur.fetchall()
        cur.close()
        return jsonify({"data":[{"nip":datalogin[0][0],"nama":datalogin[0][1],"posisi":datalogin[0][2],"gender":datalogin[0][3],"ttl":str(datalogin[0][4]),"email":datalogin[0][5],"no_hp":datalogin[0][6],"alamat":datalogin[0][7]}],"msg":"login berhasil"})
@app.route('/logout')
@roles_required('admin','HRD','karu')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('role', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('index'))
@app.route('/apiabsen',methods=['POST'])
def apiabsen():
    cur = mysql.connection.cursor()
    if 'image' not in request.files:
        cur.close()
        return jsonify({"msg":"tidak ada form image"})
    file = request.files['image']
    nip=request.form['nip']
    latitude=request.form['latitude']
    longitude= request.form['longitude']
    if file.filename == '':
        cur.close()
        return jsonify({"msg":"tidak ada file image yang dipilih"})
    if file and allowed_file(file.filename):
        print(file.filename)
        a=time.localtime()
        hr=a.tm_hour
        mn=a.tm_min
        sc=a.tm_sec
        thn=a.tm_year
        bln=a.tm_mon
        hari=a.tm_mday
        tanggal=""+str(thn)+"-"+str(bln)+"-"+str(hari)+""
        print(tanggal)
        timeNow = str(hr)+':'+str(mn)+':'+str(sc)
        cur.execute("SELECT * from dataabsen where nip = %s and tanggal = %s ",(nip,tanggal))
        cek = cur.fetchall()
        if str(cek) == '()':
            cur.execute("SELECT jadwal.shift,shift.berangkat from jadwal INNER JOIN shift ON shift.shift = jadwal.shift where jadwal.nip = %s AND jadwal.bulan = %s",(nip,str(bln)))
            shift = cur.fetchall()
            print(shift)
            cur.execute("SELECT jadwal_khusus.shift,shift.berangkat from jadwal_khusus INNER JOIN shift ON jadwal_khusus.shift = shift.shift where nip = %s AND tanggal = %s",(nip,tanggal))
            tglkhusus = cur.fetchall()
            renamefile= secure_filename(str(nip)+str(tanggal)+str(timeNow)+".jpg")
            timeNow = datetime.strptime(timeNow, "%H:%M:%S")
            if str(tglkhusus)=='()':
                print(shift)
                print(shift[0][1])
                timeEnd = datetime.strptime(str(shift[0][1]), "%H:%M:%S")
                print(timeEnd)
                a=datetime.strptime("00:30:00", "%H:%M:%S")
                b= timeEnd-a
                print(b)
                timeStart = datetime.strptime(str(b), "%H:%M:%S")
                print(timeStart)
                status=isNowInTimePeriod(timeStart,timeEnd , timeNow)
            else:
                print(tglkhusus)
                print(tglkhusus[0][1])
                timeEnd = datetime.strptime(str(tglkhusus[0][1]), "%H:%M:%S")
                print(timeEnd)
                a=datetime.strptime("00:30:00", "%H:%M:%S")
                b= timeEnd-a
                print(b)
                timeStart = datetime.strptime(str(b), "%H:%M:%S")
                print(timeStart)
                status=isNowInTimePeriod(timeStart,timeEnd , timeNow)
            file.save(os.path.join(app.config['FOLDER_ABSEN'], renamefile))
            if status=='kamu absen terlalu cepat':
                cur.close()
                return jsonify({"msg":status})
            if status=="kamu terlambat":
                statusdb="telat"
                cur.execute("INSERT INTO dataabsen(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                if mysql.connection.commit():
                    cur.close()
                return jsonify({"msg":status})
            if status=="kamu absen tepat waktu":
                statusdb="tepat waktu"
                cur.execute("INSERT INTO dataabsen(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                if mysql.connection.commit():
                    cur.close()
                return jsonify({"msg":status,"waktu":timeNow,"tanggal":tanggal})
        else:
            return jsonify({"msg":"maaf kamu sudah absen"})
    else:
        cur.close()
        return "foto yang anda kirim invalid"
@app.route('/apipulang',methods=['POST'])
def apipulang():
    cur = mysql.connection.cursor()
    if 'image' not in request.files:
        cur.close()
        return jsonify({"msg":"tidak ada form image"})
    file = request.files['image']
    nip=request.form['nip']
    latitude=request.form['latitude']
    longitude= request.form['longitude']
    
    if file.filename == '':
        cur.close()
        return jsonify({"msg":"tidak ada file image yang dipilih"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        a=time.localtime()
        hr=a.tm_hour
        mn=a.tm_min
        sc=a.tm_sec
        thn=a.tm_year
        bln=a.tm_mon
        hari=a.tm_mday
        tanggal=""+str(thn)+"-"+str(bln)+"-"+str(hari)+""
        print(tanggal)
        timeNow = str(hr)+':'+str(mn)+':'+str(sc)
        cur.execute("SELECT * from datapulang where nip = %s and tanggal = %s ",(nip,tanggal))
        cek = cur.fetchall()
        if str(cek) == '()':
            cur.execute("SELECT jadwal.shift,shift.berangkat from jadwal INNER JOIN shift ON shift.shift = jadwal.shift where jadwal.nip = %s AND jadwal.bulan = %s",(nip,str(bln)))
            shift = cur.fetchall()
            print(shift)
            cur.execute("SELECT jadwal_khusus.shift,shift.berangkat from jadwal_khusus INNER JOIN shift ON jadwal_khusus.shift = shift.shift where nip = %s AND tanggal = %s",(nip,tanggal))
            tglkhusus = cur.fetchall()
            renamefile= secure_filename(str(nip)+str(tanggal)+str(timeNow)+".jpg")
            timeNow = datetime.strptime(timeNow, "%H:%M:%S")
            if str(tglkhusus)=='()':
                timeEnd = datetime.strptime(str(shift[0][1]), "%H:%M:%S")
                a=datetime.strptime("00:30:00", "%H:%M:%S")
                b= timeEnd-a
                timeStart = datetime.strptime(str(b), "%H:%M:%S")
                status=isNowInTimePeriod(timeStart,timeEnd , timeNow)
            else:
                timeEnd = datetime.strptime(str(tglkhusus[0][1]), "%H:%M:%S")
                a=datetime.strptime("00:30:00", "%H:%M:%S")
                b= timeEnd-a
                timeStart = datetime.strptime(str(b), "%H:%M:%S")
                status=isNowInTimePeriod(timeStart,timeEnd , timeNow)
            file.save(os.path.join(app.config['FOLDER_PULANG'], renamefile))
            if status=='kamu pulang terlalu cepat':
                statusdb="terlalu cepat"
                cur.execute("INSERT INTO datapulang(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,filename,statusdb))
                if mysql.connection.commit():
                    cur.close()
                return jsonify({"msg":status})
            elif status=="kamu pulang terlalu lambat dari jawdwal apakah kamu lembur?":
                statusdb="lembur?"
                cur.execute("INSERT INTO datapulang(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,filename,statusdb))
                if mysql.connection.commit():
                    cur.close()
                return jsonify({"msg":status})
            elif status=="kamu pulang sesuai jadwal shift":
                statusdb="tepat waktu"
                cur.execute("INSERT INTO datapulang(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,filename,statusdb))
                if mysql.connection.commit():
                    cur.close()
                return jsonify({"msg":status})
        else:
             return jsonify({"msg":"maaf anda sudah absen pulang"})
    else:
        cur.close()
        return jsonify({"msg":"foto yang anda kirim invalid"})
@app.route('/api/karyawan/history/absen', methods=['POST'])
def history_absen():
    cur = mysql.connection.cursor()
    nip = request.form['nip']
    cur.execute('SELECT * FROM dataabsen WHERE nip = %s GROUP BY tanggal DESC',(nip,))
    datahistory= cur.fetchall()
    respon=[]
    for i,j in enumerate(datahistory):
        dictlogs={}
        dictlogs.update({"tanggal":str(datahistory[int(i)][5]),"waktu":str(datahistory[int(i)][6]),"status":str(datahistory[int(i)][7])})
        
        respon.append(dictlogs)
    return jsonify({"data":respon,"msg":'get history sukses'})
@app.route('/api/karyawan/history/pulang', methods=['POST'])
def history_pulang():
    cur = mysql.connection.cursor()
    nip = request.form['nip']
    cur.execute('SELECT * FROM datapulang WHERE nip = %s GROUP BY tanggal DESC',(nip,))
    datahistory= cur.fetchall()
    respon=[]
    for i,j in enumerate(datahistory):
        dictlogs={}
        dictlogs.update({"tanggal":str(datahistory[int(i)][5]),"waktu":str(datahistory[int(i)][6]),"status":str(datahistory[int(i)][7])})
        
        respon.append(dictlogs)
    return jsonify({"data":respon,"msg":'get history sukses'})
@app.route('/cetak_laporan') 
@roles_required('admin','HRD','karu')
def cetak_laporan():
    return render_template('dashboard/charts.html')
@app.route('/cetak_data') 
@roles_required('admin','HRD','karu')
def cetak_data():
    return render_template('dashboard/tables.html')
@app.route('/api/karyawan/update_profile', methods=['POST']) 
def update_profile():
    cur = mysql.connection.cursor()
    nip = request.form['nip']
    old_pswd = request.form['old_pswd']
    new_pswd = request.form['new_pswd']
    email = request.form['email']
    no_hp = request.form['no_hp']
    alamat = request.form['alamat']
    if old_pswd == '':
        cur.execute("SELECT * FROM karyawan WHERE nip = %s" , (nip,))
        new_data = cur.fetchall()
        cur.execute("UPDATE karyawan SET email=%s , no_hp=%s , alamat=%s WHERE nip = %s",(email,no_hp,alamat,nip,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"data":[{"nip":new_data[0][0],"nama":new_data[0][1],"posisi":new_data[0][2],"gender":new_data[0][3],"ttl":str(new_data[0][4]),"email":new_data[0][5],"no_hp":new_data[0][6],"alamat":new_data[0][7]}],"msg":"data berhasil diupdate"})
    else:
        cur.execute("SELECT * FROM login WHERE NIP = %s",(nip,))
        data = cur.fetchall()
        if not check_password_hash(data[0][1],old_pswd):
            cur.close()
            return jsonify({"msg":"password lama salah"})
        else: 
            if new_pswd == '':
                return jsonify({"msg":"Password Baru Tidak Boleh kosong"})
            else:
                new_pswd = generate_password_hash(new_pswd)
                cur.execute("UPDATE login SET pswd = %s WHERE nip = %s",(new_pswd, nip))
                cur.execute("UPDATE karyawan SET email = %s , no_hp = %s , alamat = %s WHERE nip = %s",(email,no_hp,alamat,nip,))
                cur.execute("SELECT * FROM karyawan WHERE NIP = %s",(nip,))
                new_data = cur.fetchall()
                mysql.connection.commit()
                cur.close()
                return jsonify({"data":[{"nip":new_data[0][0],"nama":new_data[0][1],"posisi":new_data[0][2],"gender":new_data[0][3],"ttl":new_data[0][4],"email":new_data[0][5],"no_hp":new_data[0][6],"alamat":new_data[0][7]}],"msg":"data berhasil diupdate"})
                
    