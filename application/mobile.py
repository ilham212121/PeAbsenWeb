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
def isNowAbsen(startTime, endTime, nowTime):
    if startTime < endTime:
        if nowTime < startTime:
            wait=startTime-nowTime
            print(str(wait))
            return "kamu absen terlalu cepat \n silahkan tunggu "+str(wait)+" lagi"
        if nowTime > endTime:
            return "kamu terlambat"
        if nowTime >= startTime and nowTime <= endTime:
            return "kamu absen tepat waktu"
        return 
    else: 
        return nowTime >= startTime or nowTime <= endTime
def isNowPulang(startTime, endTime, nowTime):
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
            print(cek)
            if str(cek) == '()':
                cur.execute("SELECT jadwal.shift,shift.berangkat from jadwal INNER JOIN shift ON shift.nama = jadwal.shift where jadwal.nip = %s AND jadwal.bulan = %s AND jadwal.tanggal = %s",(nip,str(a.tm_mon),tanggal))
                jadwal = cur.fetchall()
                renamefile= secure_filename(str(tanggal)+"-"+str(nip)+".jpg")
                timeNow = datetime.strptime(timeNow, "%H:%M:%S")
                print(jadwal)
                if str(jadwal)=='()':
                    print("maaf jadwal belum ada")
                    return jsonify({"msg":"maaf jadwal belum ada"})
                else:
                    timeEnd = datetime.strptime(str(jadwal[0][1]), "%H:%M:%S")
                    a=datetime.strptime("00:30:00","%H:%M:%S")
                    b= timeEnd-a
                    timeStart = datetime.strptime(str(b), "%H:%M:%S")
                    print(timeStart)
                    print(timeEnd)
                    print(timeNow)
                    status=isNowAbsen(timeStart,timeEnd,timeNow)
                file.save(os.path.join(app.config['FOLDER_ABSEN'], str(renamefile)))
                img = Image.open(os.path.join(app.config['FOLDER_ABSEN'],renamefile))
                resizedimg = img.resize((300,300),Image.ANTIALIAS==True)
                resizedimg.save(os.path.join(app.config['FOLDER_ABSEN'],renamefile),optimize=True,quality=95)
                print(status)
                print(tanggal)
                timeNow = str(timeNow).replace("1900-01-01 ","")
                print(timeNow)
                if status=='kamu absen terlalu cepat':
                    return jsonify({"msg":status})
                if status=="kamu terlambat":
                    statusdb="telat"
                    cur.execute("INSERT INTO dataabsen(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                    mysql.connection.commit()
                    return jsonify({"msg":status})
                if status=="kamu absen tepat waktu":
                    statusdb="tepat waktu"
                    cur.execute("INSERT INTO dataabsen(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                    mysql.connection.commit()
                    return jsonify({"msg":status,"waktu":str(timeNow),"tanggal":str(tanggal)})
                return jsonify({"msg":status})
            else:
                return jsonify({"msg":"maaf kamu sudah absen"})
        else:
            return jsonify({"foto yang anda kirim invalid"})
class apipulang(Resource):
    def post(self):
        cur = mysql.connection.cursor()
        if 'image' not in request.files:
            print("tidak ada form image")
            return jsonify({"msg":"tidak ada form image"})
        file = request.files['image']
        nip=request.form['nip']
        print(nip)
        latitude=request.form['latitude']
        print(latitude)
        longitude= request.form['longitude']
        if file.filename == '':
            print("tidak ada file image yang dipilih")
            return jsonify({"msg":"tidak ada file image yang dipilih"})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            a=time.localtime()
            tanggal=""+str(a.tm_year)+"-"+str(a.tm_mon)+"-"+str(a.tm_mday)+""
            timeNow = str(a.tm_hour)+':'+str(a.tm_min)+':'+str(a.tm_sec)
            cur.execute("SELECT * from datapulang where nip = %s and tanggal = %s ",(nip,tanggal))
            cek = cur.fetchall()
            if str(cek) == '()':
                cur.execute("SELECT jadwal.shift,shift.pulang from jadwal INNER JOIN shift ON shift.nama = jadwal.shift where jadwal.nip = %s AND jadwal.bulan = %s",(nip,str(a.tm_mon)))
                jadwal = cur.fetchall()
                renamefile= secure_filename(str(tanggal)+"-"+str(nip)+"-"+str(a.tm_hour)+'-'+str(a.tm_min)+'-'+str(a.tm_sec)+".jpg")
                timeNow = datetime.strptime(timeNow, "%H:%M:%S")
                if str(jadwal)=='()':
                    print("maaf jadwal belum ada")
                    return jsonify({"msg":"maaf jadwal belum ada"})
                else:
                    timeEnd = datetime.strptime(str(jadwal[0][1]), "%H:%M:%S")
                    a=datetime.strptime("00:30:00", "%H:%M:%S")
                    b= timeEnd-a
                    timeStart = datetime.strptime(str(b), "%H:%M:%S")
                    status=isNowPulang(timeStart,timeEnd , timeNow)
                file.save(os.path.join(app.config['FOLDER_PULANG'],renamefile))
                img = Image.open(os.path.join(app.config['FOLDER_PULANG'],renamefile))
                resizedimg = img.resize((300,300),Image.ANTIALIAS==True)
                resizedimg.save(os.path.join(app.config['FOLDER_PULANG'],renamefile),optimize=True,quality=95)
                if status=='kamu pulang terlalu cepat':
                    print("terlalu cepat")
                    statusdb="terlalu cepat"
                    cur.execute("INSERT INTO datapulang(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                    if mysql.connection.commit():
                        return jsonify({"msg":status})
                elif status=="kamu pulang terlalu lambat dari jadwal apakah kamu lembur?":
                    print("lembur?")
                    statusdb="lembur?"
                    cur.execute("INSERT INTO datapulang(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,renamefile,statusdb))
                    if mysql.connection.commit():
                        return jsonify({"msg":status})
                elif status=="kamu pulang sesuai jadwal shift":
                    print("tepat waktu")
                    statusdb="tepat waktu"
                    cur.execute("INSERT INTO datapulang(nip,latitude,longitude,tanggal,waktu,foto,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nip,latitude,longitude,tanggal,timeNow,filename,statusdb))
                    if mysql.connection.commit():
                        return jsonify({"msg":status})
                return jsonify({"msg":status})
            else:
                print("maaf anda sudah absen pulang")
                return jsonify({"msg":"maaf anda sudah absen pulang"})
        else:
            print("foto yang anda kirim invalid")
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
class search_history_absen(Resource):
    def get(self,nip,tanggal,status):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM dataabsen WHERE nip = %s and tanggal = %s and status = %s GROUP BY tanggal DESC',(nip,tanggal,status))
        datahistory= cur.fetchall()
        respon=[]
        for i in range(len(datahistory)):
            dictlogs={}
            dictlogs.update({"tanggal":str(datahistory[int(i)][5]),"waktu":str(datahistory[int(i)][6]),"status":str(datahistory[int(i)][7])})   
            respon.append(dictlogs)
        return make_response(jsonify([{"data":respon,"msg":'get history sukses'}]))
class history_absenold(Resource):
    def post(self):
        nip = request.form['nip']
        return redirect("/api/v1/karyawan/history/absen/"+nip)

class history_pulangold(Resource):
    def post(self):
        nip = request.form['nip']
        return redirect("/api/v1/karyawan/history/pulang/"+nip)

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

class profile(Resource):
    def get(self,token):
        cur = mysql.connection.cursor()
        print(token)
        cur.execute("SELECT nip FROM login WHERE token = %s ",(token,))
        nip=cur.fetchone()
        cur.execute("SELECT nip,nama,posisi,gender,ttl,email,no_hp,alamat FROM karyawan WHERE nip = %s ",(nip,))
        dataprofile= cur.fetchone()
        print(dataprofile)
        return jsonify({"data":{"nip":dataprofile[0],"nama":dataprofile[1],"posisi":dataprofile[2],"gender":dataprofile[3],"ttl":str(dataprofile[4]),"email":dataprofile[5],"no_hp":dataprofile[6],"alamat":dataprofile[7]},"msg":'get profile sukses'})

class update_profile(Resource):
    def put(self):
        cur = mysql.connection.cursor()
        nip = request.form['nip']
        print(nip)
        old_pswd = request.form['old_pswd'] 
        print(old_pswd)
        new_pswd = request.form['new_pswd']
        print(new_pswd)
        email = request.form['email']
        print(email)
        no_hp = request.form['no_hp']
        print(no_hp)
        alamat = request.form['alamat']
        print(alamat)
        tgl = datetime.now()
        cur.execute("SELECT * FROM login WHERE NIP = %s",(nip,))
        data = cur.fetchall()
        if old_pswd == '':
            None
        else:
            if not check_password_hash(data[0][1],old_pswd):
                status = False
                msg = "password lama salah"
            else: 
                if new_pswd == '':
                    status = False
                    msg= "Password Baru Tidak Boleh kosong"
                else:
                    new_pswd = generate_password_hash(new_pswd)
                    cur.execute("UPDATE login SET pswd = %s WHERE nip = %s",(new_pswd, nip))
                    mysql.connection.commit()
                    status = True
        if email == '':
            None
        else:
            cur.execute("UPDATE karyawan SET email=%s WHERE nip = %s ",(email,nip))
            mysql.connection.commit()
            status = True
        if no_hp == '':
            None
        else:
            cur.execute("UPDATE karyawan SET no_hp=%s WHERE nip = %s",(no_hp,nip,))
            mysql.connection.commit()
            status = True
        if alamat == '':
            None
        else:
            cur.execute("UPDATE karyawan SET alamat=%s WHERE nip = %s",(alamat,nip,))
            mysql.connection.commit()
            status = True
        cur.execute("SELECT nip,nama,posisi,gender,ttl,email,no_hp,alamat FROM karyawan WHERE nip = %s ",(nip,))
        new_data = cur.fetchone()
        print(new_data)
        if status == False :
            print("false")
            return jsonify({"msg":msg})
        else:
            print("true")
            return jsonify({"data":[{"nip":new_data[0],"nama":new_data[1],"posisi":new_data[2],"gender":new_data[3],"ttl":str(new_data[4]),"email":new_data[5],"no_hp":new_data[6],"alamat":new_data[7]}],"msg":"data berhasil diupdate"})
            
api.add_resource(history_absenold, '/api/karyawan/history/absen', methods=['POST'])
api.add_resource(history_pulangold, '/api/karyawan/history/pulang', methods=['POST'])
api.add_resource(apiabsen, '/api/v1/events/absen', methods=['POST'])
api.add_resource(apipulang, '/api/v1/events/pulang', methods=['POST'])
api.add_resource(history_absen, '/api/v1/karyawan/history/absen/<nip>', methods=['GET'])
api.add_resource(search_history_absen, '/api/v1/karyawan/history/absen/<nip>/<tanggal>/<status>', methods=['GET'])
api.add_resource(history_pulang, '/api/v1/karyawan/history/pulang/<nip>', methods=['GET'])
api.add_resource(update_profile, '/api/v1/karyawan/update_profile', methods=['PUT'])
api.add_resource(profile, '/api/v1/karyawan/profile/<token>', methods=['GET'])