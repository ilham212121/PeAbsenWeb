from ast import Tuple
import json, numpy
from application import app,mysql,allowed_file
from flask import Blueprint, Flask, jsonify, make_response, redirect, render_template, request, url_for,send_from_directory
from application.auth import session,roles_required

from time import time
import time,random
from datetime import datetime

web = Blueprint('auth', __name__)
@web.post("/update/<ruangan>/<bulan>/<tahun>")
def update(ruangan,bulan,tahun):
    cur = mysql.connection.cursor()
    print(ruangan)
    print(bulan)
    print(tahun)
    cur.execute("SELECT nip, karyawan.nama FROM karyawan WHERE ruangan = '"+ruangan+"' ORDER by nama ASC")
    datapegawai = cur.fetchall()
    cur.execute("SELECT tanggal, shift FROM jadwal inner join karyawan on jadwal.nip = karyawan.nip where karyawan.ruangan = '"+ ruangan+"'")
    datajadwalabsen = cur.fetchall()
    cobajadwal=[]
    datapegawai= jsonify(datapegawai)
    cobapegawai=[{"nip":"220712001","nama":"Bambang"},{"nip":"220712002","nama":"Farid"},{"nip":"220712003","nama":"Gilang"}]
    
    datajadwalabsen= jsonify(datajadwalabsen)
    # datajadwalabsenfix = []
    # for i in datapegawai:
    #     dictlog=[]
    #     for x in datajadwalabsen:
    #         dictlog.append(datajadwalabsen[x], datajadwalabsen[1])
    #         datajadwalabsenfix.append(dictlog)
    # print(json.loads(datajadwalabsen))
    response = jsonify({"data_pegawai":cobapegawai,"data_jadwal":cobajadwal})
    #response = numpy.array(datapegawai,datajadwalabsen)
    print(cobajadwal)
    return response
@web.post("/updateOrInsertJadwal")
def updateOrInsertJadwal():
    nip = request.json["nip"]
    hari = request.json["hari"]
    shift_id = request.json["shift_id"]
    bulan = request.json["bulan"]
    tahun = request.json["tahun"]
    ruangan = request.json["ruangan"]
    cur = mysql.connection.cursor()
    tanggal= tahun+"-"+bulan+"-"+hari
    #tanggal = datetime.strptime(tanggal,"%Y-%m-%d")
    print(tanggal)
    print(shift_id)
    cur.execute("SELECT nama  FROM shift ")
    listshift = cur.fetchall()
    for i in range(len(listshift)) :
        print(i)
        if str(i+1) == shift_id:
            shift = listshift[i][0]
            break

    cur.execute("SELECT tanggal, shift  FROM jadwal WHERE nip = %s and tanggal = %s ",(nip,tanggal))
    datajadwalabsen = cur.fetchall()
    print(shift)
    print(datajadwalabsen)
    if datajadwalabsen == ():
        print("kosong")
        cur.execute("INSERT INTO jadwal(nip,shift,ruangan,tanggal,bulan) VALUES(%s,%s,%s,%s,%s )",(nip,shift,ruangan,tanggal,bulan))
        mysql.connection.commit()
        return jsonify({"data":"null","meta":{"code":200,"message":"Berhasil menambahkan Data","status":"success"}})
    else:
        print("ada")
        if shift_id == "0":
            #delete data
            cur.execute("DELETE FROM jadwal WHERE nip = %s and tanggal = %s ",(nip,tanggal))
            mysql.connection.commit()
            return jsonify({"data":None,"meta":{"code":200,"message":"Berhasil hapus Data","status":"success"}})
        else:
            #update data
            cur.execute("UPDATE `jadwal` SET `shift`=%s WHERE nip = %s and tanggal = %s ",(shift,nip,tanggal))
            mysql.connection.commit()
            return jsonify({"data":None,"meta":{"code":200,"message":"Berhasil ubah Data","status":"success"}})
    return "coba"
@web.route('/profile') 
@roles_required('admin','HRD','karu')
def profile():
    id = session['id']
    role = session['role']
    cur = mysql.connection.cursor()
    cur.execute("SELECT login.nip, nama, email, gender, ttl, alamat, no_hp FROM login inner join "+role+" on "+role+".nip = login.nip WHERE  login.nip = %s ",(id,))
    dataprofile = cur.fetchone()
    return render_template('dashboard/profile.html',dataprofile=dataprofile)
@web.route('/profile/update', methods=['POST']) 
@roles_required('admin','HRD','karu')
def profileupdate():
    id = session['id']
    print(id)
    role = session['role']
    print(role)
    nama = request.form['nama'] 
    print(nama)
    email = request.form['email'] 
    print(email)
    gender = request.form['gender'] 
    print(gender)
    ttl = request.form['ttl'] 
    print(ttl)
    alamat = request.form['alamat'] 
    print(alamat)
    no_hp = request.form['no_hp']
    print(no_hp)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE login inner join "+role+" on "+role+".nip = login.nip SET nama=%s, email=%s, gender=%s, ttl=%s, alamat=%s, no_hp=%s WHERE login.nip = %s ",(nama, email, gender, ttl, alamat, no_hp,id,))
    mysql.connection.commit()
    return redirect(url_for('web.profile'))
@web.route('/form/<init>') 
@roles_required('admin','HRD','karu')
def form(init):
    cur = mysql.connection.cursor()
    cur.execute("SELECT Nama FROM RUANGAN")
    ruangan = cur.fetchall()
    cur.execute("SELECT Nama FROM SHIFT")
    shift = cur.fetchall()
    bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    tahun = datetime.today().year
    return render_template('dashboard/form.html', init=init, ruangan=ruangan, shift=shift, bulan=bulan, tahun=tahun)
@web.route('/edit/admin/<no>',methods=['GET','PUT']) 
@roles_required('admin')
def editformadmin(no):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin where nip= %s",(no,))
        admin = cur.fetchall()
        return render_template('dashboard/formedit.html',init="admin",data=admin)
    elif request.method == "PUT":
        cur = mysql.connection.cursor()
        nama = request.json['nama']
        email = request.json[ 'email']
        gender = request.json[ 'gender']
        tanggal_lahir = request.json['tanggal_lahir']
        alamat = request.json['alamat']
        no_hp = request.json['no_hp']
        cur.execute("UPDATE admin SET nama=%s, email=%s, gender=%s, ttl=%s, alamat=%s,no_hp=%s where nip= %s",(nama,email,gender,tanggal_lahir,alamat,no_hp, str(no),))
        mysql.connection.commit()
        return jsonify({"status":"sukses","url":"/data_admin?msg='data berhasil diedit'"})
@web.route('/edit/hrd/<no>',methods=['GET','PUT']) 
@roles_required('admin','HRD')
def editformhrd(no):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM hrd where nip= %s",(no,))
        hrd = cur.fetchall()
        return render_template('dashboard/formedit.html',init="hrd",data=hrd)
    elif request.method == "PUT":
        cur = mysql.connection.cursor()
        nama = request.json['nama']
        email = request.json[ 'email']
        gender = request.json[ 'gender']
        tanggal_lahir = request.json['tanggal_lahir']
        alamat = request.json['alamat']
        no_hp = request.json['no_hp']
        cur.execute("UPDATE hrd SET nama=%s, email=%s, gender=%s, ttl=%s, alamat=%s,no_hp=%s where nip= %s",(nama,email,gender,tanggal_lahir,alamat,no_hp, str(no),))
        mysql.connection.commit()
        return redirect(url_for('web.data_hrd'))
    
@web.route('/edit/karu/<no>',methods=['GET','PUT']) 
@roles_required('admin','HRD','karu')
def editformkaru(no):
    
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM karu where nip= %s",(no,))
        karu = cur.fetchall()
        return render_template('dashboard/formedit.html',init="karu",data=karu)
    
    elif request.method == "PUT":
        cur = mysql.connection.cursor()
        nama = request.json['nama']
        email = request.json[ 'email']
        gender = request.json[ 'gender']
        tanggal_lahir = request.json['tanggal_lahir']
        alamat = request.json['alamat']
        no_hp = request.json['no_hp']
        cur.execute("UPDATE karu SET nama=%s, email=%s, gender=%s, ttl=%s, alamat=%s,no_hp=%s where nip= %s",(nama,email,gender,tanggal_lahir,alamat,no_hp, no,))
        mysql.connection.commit()
        return redirect(url_for('web.data_karu'))

@web.route('/edit/karyawan/<no>',methods=['GET','PUT']) 
@roles_required('admin','HRD','karu')
def editformkaryawan(no):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM karyawan where nip= %s",(no,))
        karyawan = cur.fetchall()
        return render_template('dashboard/formedit.html',init="karyawan",data=karyawan)
    elif request.method == "PUT":
        cur = mysql.connection.cursor()
        nama = request.json['nama']
        email = request.json[ 'email']
        gender = request.json[ 'gender']
        tanggal_lahir = request.json['tanggal_lahir']
        alamat = request.json['alamat']
        no_hp = request.json['no_hp']
        cur.execute("UPDATE karyawan SET nama=%s, email=%s, gender=%s, ttl=%s, alamat=%s,no_hp=%s where nip= %s",(nama,email,gender,tanggal_lahir,alamat,no_hp, no,))
        mysql.connection.commit()
        return redirect(url_for('web.data_karyawan'))
@web.route('/data_admin') 
@roles_required('admin')
def data_admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin")
    admin = cur.fetchall()
    print
    return render_template('dashboard/data_admin.html',admin=admin)
@web.route('/data_hrd')
@roles_required('admin','HRD')
def data_hrd():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hrd")
    hrd = cur.fetchall()
    return render_template('dashboard/data_hrd.html',hrd=hrd)
@web.route('/data_karu')
@roles_required('admin','HRD','karu')
def data_karu():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM karu")
    karu = cur.fetchall()
    return render_template('dashboard/data_karu.html',karu=karu)
@web.route('/data_karyawan') 
@roles_required('admin','HRD','karu')
def data_karyawan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM karyawan")
    karyawan = cur.fetchall()
    return render_template('dashboard/data_karyawan.html',karyawan=karyawan)
@web.route('/laporan_absen') 
@roles_required('admin','HRD','karu')
def laporan_absen():
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT dataabsen.id, dataabsen.nip, karyawan.nama,jadwal.ruangan,shift.nama,`latitude`, `longitude`, `foto`, dataabsen.tanggal, `waktu`, dataabsen.status'
        ' FROM dataabsen INNER JOIN jadwal on dataabsen.nip = jadwal.nip INNER JOIN shift on shift.nama = jadwal.shift INNER JOIN karyawan ON dataabsen.nip = karyawan.nip '
        ' GROUP by jadwal.tanggal desc, waktu desc')
    dataabsen = cur.fetchall()
    cur.execute(
        'SELECT nama from ruangan')
    ruangan = cur.fetchall()
    return render_template('dashboard/laporan_absen.html',dataabsen=dataabsen,ruangan=ruangan)
@web.route('/laporan_pulang') 
@roles_required('admin','HRD','karu')
def laporan_pulang():
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT datapulang.id, datapulang.nip, karyawan.nama,jadwal.ruangan,shift.nama,`latitude`, `longitude`, `foto`, datapulang.tanggal, `waktu`, datapulang.status'
        ' FROM datapulang INNER JOIN jadwal on datapulang.nip = jadwal.nip INNER JOIN shift on shift.nama = jadwal.shift INNER JOIN karyawan ON datapulang.nip = karyawan.nip '
        ' GROUP by tanggal desc, waktu desc')
    datapulang = cur.fetchall()
    cur.execute(
        'SELECT nama from ruangan')
    ruangan = cur.fetchall()
    return render_template('dashboard/laporan_pulang.html',datapulang=datapulang,ruangan=ruangan)
@web.route('/cetak_laporan') 
@roles_required('admin','HRD','karu')
def cetak_laporan():
    return render_template('dashboard/charts.html')
@web.route('/cetak_data') 
@roles_required('admin','HRD','karu')
def cetak_data():
    return render_template('dashboard/tables.html')
@web.route('/jadwal') 
@roles_required('admin','HRD','karu')
def jadwal():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jadwal")
    jadwal = cur.fetchall()
    return render_template('dashboard/jadwal.html',jadwal=jadwal)
@web.route('/shift') 
@roles_required('admin','HRD','karu')
def shift():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM shift")
    shift = cur.fetchall()
    day= datetime.strptime("2","%d")
    listx = list(shift) 

    for i in range(len(listx)):
        if listx[i][1]=="malam":
            a = listx[i][3]-listx[i][2]+day #timedelta(days=1)
            b = str(a.hour)+':'+str(a.minute)+'0:0'+str(a.second)
            c = (b,)
            listx[i] = listx[i]+c
        else:
            a = listx[i][3]-listx[i][2]
            b = (a,)
            listx[i]= listx[i]+b
    shiftt = tuple(listx)
    return render_template('dashboard/shift.html',shift=shiftt,day=day)
@web.route('/admin/warga',methods=['GET'])
@roles_required('admin','HRD')
def warga():
    warga = mysql.connection.cursor()
    warga.execute("SELECT * FROM data_warga")
    data_warga = warga.fetchall()
    warga.close()
    return render_template('admin/data_warga.html',data_warga=data_warga)
@web.route('/delete/<init>/<id>',methods=['DELETE'])
@roles_required('admin','HRD')
def deleteuser(init,id):
    try:
        if request.method == 'DELETE':
            warga = mysql.connection.cursor()
            warga.execute("DELETE FROM data_warga where id = "+id)
            mysql.connection.commit()
    except Exception as e:
        return make_response(e)
    return redirect(url_for('auth.index'))
@web.route('/coba')
def coba():
    cur = mysql.connection.cursor()
    nip='220712001'
    cur.execute('SELECT * FROM dataabsen WHERE nip = %s GROUP BY tanggal DESC',(nip,))
    datahistory= cur.fetchall()
    respon=[]
    for i in range(len(datahistory)):
        dictlogs={}
        dictlogs.update({"tanggal":str(datahistory[int(i)][5]),"waktu":str(datahistory[int(i)][6]),"status":str(datahistory[int(i)][7])})   
        respon.append(dictlogs)
    return jsonify({"data":respon,"msg":'get history sukses'})
