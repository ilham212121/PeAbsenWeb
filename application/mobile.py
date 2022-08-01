import os
from time import time
from application import app,mysql,allowed_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify,request
import time
import datetime
from datetime import datetime
from PIL import Image 

mobile = Blueprint('auth', __name__)
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
@mobile.route('/apiabsen',methods=['POST'])
def apiabsen():
    cur = mysql.connection.cursor()
    if 'image' not in request.files:
        cur.close()
        return jsonify({"msg":"tidak ada form image"})
    file = request.files['image'],nip=request.form['nip']
    latitude=request.form['latitude'],longitude= request.form['longitude']
    if file.filename == '':
        cur.close()
        return jsonify({"msg":"tidak ada file image yang dipilih"})
    if file and allowed_file(file.filename):
        a=time.localtime()
        tanggal=""+str(a.tm_year)+"-"+str(a.tm_mon)+"-"+str(a.tm_mday)+""
        timeNow = str(a.tm_hour)+':'+str(a.tm_min)+':'+str(a.tm_sec)
        cur.execute("SELECT * from dataabsen where nip = %s and tanggal = %s ",(nip,tanggal))
        cek = cur.fetchall()
        if str(cek) == '()':
            cur.execute("SELECT jadwal.shift,shift.berangkat from jadwal INNER JOIN shift ON shift.shift = jadwal.shift where jadwal.nip = %s AND jadwal.bulan = %s",(nip,str(a.tm_mon)))
            jadwal = cur.fetchall()
            cur.execute("SELECT tukar_dinas.shift,shift.berangkat from tukar_dinas INNER JOIN shift ON tukar_dinas.shift = shift.shift where nip = %s AND tanggal = %s",(nip,tanggal))
            tuker_dinas = cur.fetchall()
            renamefile= secure_filename(str(nip)+str(tanggal)+str(timeNow)+".jpg")
            timeNow = datetime.strptime(timeNow, "%H:%M:%S")
            if str(tuker_dinas)=='()':
                timeEnd = datetime.strptime(str(jadwal[0][1]), "%H:%M:%S")
                a=datetime.strptime("00:30:00", "%H:%M:%S")
                b= timeEnd-a
                timeStart = datetime.strptime(str(b), "%H:%M:%S")
                status=isNowInTimePeriod(timeStart,timeEnd , timeNow)
            else:
                timeEnd = datetime.strptime(str(tuker_dinas[0][1]), "%H:%M:%S")
                a=datetime.strptime("00:30:00", "%H:%M:%S")
                b= timeEnd-a
                timeStart = datetime.strptime(str(b), "%H:%M:%S")
                status=isNowInTimePeriod(timeStart,timeEnd , timeNow)
            file.save(os.path.join(app.config['FOLDER_ABSEN'], renamefile))
            img = Image.open(os.path.join(app.config['FOLDER_ABSEN'],a))
            resizedimg = img.resize((300,300),Image.ANTIALIAS==True)
            resizedimg.save(os.path.join(app.config['FOLDER_ABSEN'],a),optimize=True,quality=95)
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
@mobile.route('/apipulang',methods=['POST'])
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
        tanggal=""+str(a.tm_year)+"-"+str(a.tm_mon)+"-"+str(a.tm_mday)+""
        timeNow = str(a.tm_hour)+':'+str(a.tm_min)+':'+str(a.tm_sec)
        cur.execute("SELECT * from datapulang where nip = %s and tanggal = %s ",(nip,tanggal))
        cek = cur.fetchall()
        if str(cek) == '()':
            cur.execute("SELECT jadwal.shift,shift.pulang from jadwal INNER JOIN shift ON shift.shift = jadwal.shift where jadwal.nip = %s AND jadwal.bulan = %s",(nip,str(a.tm_mon)))
            jadwal = cur.fetchall()
            cur.execute("SELECT tukar_dinas.shift,shift.pulang from tukar_dinas INNER JOIN shift ON tukar_dinas.shift = shift.shift where nip = %s AND tanggal = %s",(nip,tanggal))
            tuker_dinas = cur.fetchall()
            renamefile= secure_filename(str(nip)+str(tanggal)+str(timeNow)+".jpg")
            timeNow = datetime.strptime(timeNow, "%H:%M:%S")
            if str(tuker_dinas)=='()':
                timeEnd = datetime.strptime(str(jadwal[0][1]), "%H:%M:%S")
                a=datetime.strptime("00:30:00", "%H:%M:%S")
                b= timeEnd-a
                timeStart = datetime.strptime(str(b), "%H:%M:%S")
                status=isNowInTimePeriod(timeStart,timeEnd , timeNow)
            else:
                timeEnd = datetime.strptime(str(tuker_dinas[0][1]), "%H:%M:%S")
                a=datetime.strptime("00:30:00", "%H:%M:%S")
                b= timeEnd-a
                timeStart = datetime.strptime(str(b), "%H:%M:%S")
                status=isNowInTimePeriod(timeStart,timeEnd , timeNow)
            file.save(os.path.join(app.config['FOLDER_PULANG'], renamefile))
            img = Image.open(os.path.join(app.config['FOLDER_PULANG'],renamefile))
            resizedimg = img.resize((300,300),Image.ANTIALIAS==True)
            resizedimg.save(os.path.join(app.config['FOLDER_PULANG'],renamefile),optimize=True,quality=95)
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
@mobile.route('/api/karyawan/history/absen', methods=['POST'])
def history_absen():
    cur = mysql.connection.cursor()
    nip = request.form['nip']
    cur.execute('SELECT * FROM dataabsen WHERE nip = %s GROUP BY tanggal DESC',(nip,))
    datahistory= cur.fetchall()
    respon=[]
    for i in enumerate(datahistory):
        dictlogs={}
        dictlogs.update({"tanggal":str(datahistory[int(i)][5]),"waktu":str(datahistory[int(i)][6]),"status":str(datahistory[int(i)][7])})   
        respon.append(dictlogs)
    return jsonify({"data":respon,"msg":'get history sukses'})
@mobile.route('/api/karyawan/history/pulang', methods=['POST'])
def history_pulang():
    cur = mysql.connection.cursor()
    nip = request.form['nip']
    cur.execute('SELECT * FROM datapulang WHERE nip = %s GROUP BY tanggal DESC',(nip,))
    datahistory= cur.fetchall()
    respon=[]
    for i in enumerate(datahistory):
        dictlogs={}
        dictlogs.update({"tanggal":str(datahistory[int(i)][5]),"waktu":str(datahistory[int(i)][6]),"status":str(datahistory[int(i)][7])})   
        respon.append(dictlogs)
    return jsonify({"data":respon,"msg":'get history sukses'})

@mobile.route('/api/karyawan/update_profile', methods=['POST']) 
def update_profile():
    cur = mysql.connection.cursor()
    nip = request.form['nip'],old_pswd = request.form['old_pswd'],new_pswd = request.form['new_pswd']
    email = request.form['email'],no_hp = request.form['no_hp'],alamat = request.form['alamat']
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
