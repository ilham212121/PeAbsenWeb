import os
from time import time
import time
import datetime
from application import app,mysql,allowed_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, make_response, redirect,request, url_for
from datetime import datetime
from PIL import Image 
from flask_cors import CORS
from flask_restful import Resource, Api
mobile = Blueprint('auth', __name__)
api = Api(app)
CORS(app)
def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        if nowTime < startTime:
            wait=startTime-nowTime
            print(str(wait))
            return "kamu absen terlalu cepat silahkan tunggu "+str(wait)+" lagi"
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
class apiabsen(Resource):
    def post(self):
        cur = mysql.connection.cursor()
        if 'image' not in request.files:
            return jsonify({"msg":"tidak ada form image"})
        file = request.files['image']
        nip=request.form['nip']
        latitude=request.form['latitude']
        longitude= request.form['longitude']
        if file.filename == '':
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
                renamefile= secure_filename(str(tanggal)+"-"+str(nip)+".jpg")
                timeNow = datetime.strptime(timeNow, "%H:%M:%S")
                if str(tuker_dinas)=='()':
                    timeEnd = datetime.strptime(str(jadwal[0][1]), "%H:%M:%S")
                    a=datetime.strptime("00:30:00","%H:%M:%S")
                    b= timeEnd-a
                    timeStart = datetime.strptime(str(b), "%H:%M:%S")
                    status=isNowInTimePeriod(timeStart,timeEnd,timeNow)
                else:
                    timeEnd = datetime.strptime(str(tuker_dinas[0][1]), "%H:%M:%S")
                    a=datetime.strptime("00:30:00","%H:%M:%S")
                    b= timeEnd-a
                    timeStart = datetime.strptime(str(b),"%H:%M:%S")
                    status=isNowInTimePeriod(timeStart,timeEnd,timeNow)
                file.save(os.path.join(app.config['FOLDER_ABSEN'], str(renamefile)))
                img = Image.open(os.path.join(app.config['FOLDER_PULANG'],renamefile))
                resizedimg = img.resize((300,300),Image.ANTIALIAS==True)
                resizedimg.save(os.path.join(app.config['FOLDER_PULANG'],renamefile),optimize=True,quality=95)
                if status=='kamu absen terlalu cepat':
                    return jsonify({"msg":status})
                if status=="kamu terlambat":
                    statusdb="telat"
                    cur.execute("INSERT INTO dataabsen(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                    if mysql.connection.commit():
                        return jsonify({"msg":status})
                if status=="kamu absen tepat waktu":
                    statusdb="tepat waktu"
                    cur.execute("INSERT INTO dataabsen(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                    if mysql.connection.commit():
                        return jsonify({"msg":status,"waktu":timeNow,"tanggal":tanggal})
            else:
                return jsonify({"msg":"maaf kamu sudah absen"})
        else:
            return jsonify({"foto yang anda kirim invalid"})
class apipulang(Resource):
    def post(self):
        cur = mysql.connection.cursor()
        if 'image' not in request.files:
            return jsonify({"msg":"tidak ada form image"})
        file = request.files['image']
        nip=request.form['nip']
        latitude=request.form['latitude']
        longitude= request.form['longitude']
        if file.filename == '':
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
                renamefile= secure_filename(str(tanggal)+"-"+str(nip)+"-"+str(a.tm_hour)+'-'+str(a.tm_min)+'-'+str(a.tm_sec)+".jpg")
                timeNow = datetime.strptime(timeNow, "%H:%M:%S")
                if str(tuker_dinas)=='()':
                    if str(jadwal)=='()':
                        return jsonify({"msg":"maaf jadwal belum ada"})
                    else:
                        timeEnd = datetime.strptime(str(jadwal[0][1]), "%H:%M:%S")
                        a=datetime.strptime("00:30:00", "%H:%M:%S")
                        b= timeEnd-a
                        timeStart = datetime.strptime(str(b), "%H:%M:%S")
                        status=isNowInTimePeriod(timeStart,timeEnd , timeNow)
                else:
                    if str(jadwal)=='()':
                        return jsonify({"msg":"maaf jadwal belum ada"})
                    else:
                        timeEnd = datetime.strptime(str(tuker_dinas[0][1]), "%H:%M:%S")
                        a=datetime.strptime("00:30:00", "%H:%M:%S")
                        b= timeEnd-a
                        timeStart = datetime.strptime(str(b), "%H:%M:%S")
                        status=isNowInTimePeriod(timeStart,timeEnd , timeNow)
                file.save(os.path.join(app.config['FOLDER_PULANG'],renamefile))
                img = Image.open(os.path.join(app.config['FOLDER_PULANG'],renamefile))
                resizedimg = img.resize((300,300),Image.ANTIALIAS==True)
                resizedimg.save(os.path.join(app.config['FOLDER_PULANG'],renamefile),optimize=True,quality=95)
                if status=='kamu pulang terlalu cepat':
                    statusdb="terlalu cepat"
                    cur.execute("INSERT INTO datapulang(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,filename,statusdb))
                    if mysql.connection.commit():
                        return jsonify({"msg":status})
                elif status=="kamu pulang terlalu lambat dari jawdwal apakah kamu lembur?":
                    statusdb="lembur?"
                    cur.execute("INSERT INTO datapulang(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,filename,statusdb))
                    if mysql.connection.commit():
                        return jsonify({"msg":status})
                elif status=="kamu pulang sesuai jadwal shift":
                    statusdb="tepat waktu"
                    cur.execute("INSERT INTO datapulang(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,filename,statusdb))
                    if mysql.connection.commit():
                        return jsonify({"msg":status})
            else:
                 return jsonify({"msg":"maaf anda sudah absen pulang"})
        else:
            return jsonify({"msg":"foto yang anda kirim invalid"})

class history_absen(Resource):
    def get(self,nip):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM dataabsen WHERE nip = %s GROUP BY tanggal DESC',(nip,))
        datahistory= cur.fetchall()
        respon=[]
        for i in range(len(datahistory)):
            dictlogs={}
            dictlogs.update({"tanggal":str(datahistory[int(i)][5]),"waktu":str(datahistory[int(i)][6]),"status":str(datahistory[int(i)][7])})   
            respon.append(dictlogs)
        return make_response(jsonify([{"data":respon,"msg":'get history sukses'}]))

class history_absenold(Resource):
    def get(self):
        return make_response(redirect(url_for(history_absen)))

class history_pulangold(Resource):
    def get(self):
        return make_response(redirect(url_for(history_pulang)))

class history_pulang(Resource):
    def get(self,nip):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM datapulang WHERE nip = %s GROUP BY tanggal DESC',(nip,))
        datahistory= cur.fetchall()
        respon=[]
        for i in range(len(datahistory)):
            dictlogs={}
            dictlogs.update({"tanggal":str(datahistory[int(i)][5]),"waktu":str(datahistory[int(i)][6]),"status":str(datahistory[int(i)][7])})   
            respon.append(dictlogs)
        return jsonify([{"data":respon,"msg":'get history sukses'}])

class update_profile(Resource):
    def put(self):
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
            return jsonify({"data":[{"nip":new_data[0][0],"nama":new_data[0][1],"posisi":new_data[0][2],"gender":new_data[0][3],"ttl":str(new_data[0][4]),"email":new_data[0][5],"no_hp":new_data[0][6],"alamat":new_data[0][7]}],"msg":"data berhasil diupdate"})
        else:
            cur.execute("SELECT * FROM login WHERE NIP = %s",(nip,))
            data = cur.fetchall()
            if not check_password_hash(data[0][1],old_pswd):
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
                    return jsonify({"data":[{"nip":new_data[0][0],"nama":new_data[0][1],"posisi":new_data[0][2],"gender":new_data[0][3],"ttl":new_data[0][4],"email":new_data[0][5],"no_hp":new_data[0][6],"alamat":new_data[0][7]}],"msg":"data berhasil diupdate"})

api.add_resource(history_absenold, '/api/karyawan/history/absen', methods=['GET'])
api.add_resource(history_pulangold, '/api/karyawan/history/pulang', methods=['GET'])
api.add_resource(apiabsen, '/api/v1/events/absen', methods=['POST'])
api.add_resource(apipulang, '/api/v1/events/pulang', methods=['POST'])
api.add_resource(history_absen, '/api/v1/karyawan/history/absen/<nip>', methods=['GET'])
api.add_resource(history_pulang, '/api/v1/karyawan/history/pulang/<nip>', methods=['GET'])
api.add_resource(update_profile, '/api/v1/karyawan/update_profile', methods=['PUT'])