from ast import Tuple
import json, numpy
from application import app,mysql,allowed_file
from flask import Blueprint, Flask, jsonify, make_response, redirect, render_template, request, url_for,send_from_directory
from application.auth import session,roles_required

from time import time
import time,random
from datetime import datetime

web = Blueprint('auth', __name__)
def generate_nip(tgl_date,jk,no_urut):
    tgl = datetime.strptime(tgl_date, '%Y-%m-%d').date()
    thn_lahir = tgl.year
    bln_lahir = tgl.month
    tgl_lahir = tgl.day
    thn_ini = datetime.today().year
    no_urut = convertTuple(no_urut)
    no_urut = no_urut.zfill(3)
    if jk == 'L':
        jk = 0
    else :
        jk = 1
    nip = str(thn_lahir)+str(bln_lahir)+str(tgl_lahir)+str(thn_ini)+str(bln_lahir)+str(jk)+str(no_urut)
    return nip

def convertTuple(tup):
    st = ''.join(map(str, tup))
    return st

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
    return render_template('dashboard/form.html',init=init, ruangan=ruangan, shift=shift, bulan=bulan, tahun=tahun)
@web.route('/add/admin',methods=['POST']) 
@roles_required('admin')
def add_admin():
    nama = request.json['nama']
    email = request.json['email']
    jk = request.json['jk']
    tgl_lahir = request.json['tgl_lahir']
    print(tgl_lahir)
    no_hp = request.json['no_hp']
    alamat = request.json['alamat']
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*)+1 FROM admin")
    no_urut = cur.fetchone()
    print(no_urut)
    nip = generate_nip(tgl_lahir,jk,no_urut)
    print(nip)
    today =  datetime.today()
    cur.execute("INSERT INTO `admin`(`nip`, `nama`, `email`, `gender`, `ttl`, `alamat`, `no_hp`, `deleted_at`, `created_at`, `updated_at`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",(nip,nama,email,jk,tgl_lahir,alamat,no_hp,'',today,today))
    mysql.connection.commit()
    return jsonify({"data":None,"meta":{"code":200,"message":"Berhasil ubah Data","status":"success"}})
@web.route('/add/hrd',methods=['POST']) 
@roles_required('admin','HRD')
def add_hrd():
    nama = request.json['nama']
    email = request.json['email']
    jk = request.json['jk']
    tgl_lahir = request.json['tgl_lahir']
    print(tgl_lahir)
    no_hp = request.json['no_hp']
    alamat = request.json['alamat']
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*)+1 FROM hrd")
    no_urut = cur.fetchone()
    print(no_urut)
    nip = generate_nip(tgl_lahir,jk,no_urut)
    print(nip)
    today =  datetime.today()
    cur.execute("INSERT INTO `hrd`(`nip`, `nama`, `email`, `gender`, `ttl`, `alamat`, `no_hp`, `deleted_at`, `created_at`, `updated_at`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",(nip,nama,email,jk,tgl_lahir,alamat,no_hp,'',today,today))
    mysql.connection.commit()
    return jsonify({"data":None,"meta":{"code":200,"message":"Berhasil ubah Data","status":"success"}})
@web.route('/add/karu',methods=['POST']) 
@roles_required('admin','HRD','karu')
def add_karu():
    nama = request.json['nama']
    email = request.json['email']
    jk = request.json['jk']
    tgl_lahir = request.json['tgl_lahir']
    print(tgl_lahir)
    penempatan = request.json['ruangan']
    no_hp = request.json['no_hp']
    alamat = request.json['alamat']
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*)+1 FROM karu")
    no_urut = cur.fetchone()
    print(no_urut)
    nip = generate_nip(tgl_lahir,jk,no_urut)
    print(nip)
    today =  datetime.today()
    cur.execute("INSERT INTO `karu`(`nip`, `nama`,`penempatan`, `email`, `gender`, `ttl`, `alamat`, `no_hp`, `deleted_at`, `created_at`, `updated_at`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",(nip,nama,penempatan,email,jk,tgl_lahir,alamat,no_hp,'',today,today))
    mysql.connection.commit()
    return jsonify({"data":None,"meta":{"code":200,"message":"Berhasil ubah Data","status":"success"}})
@web.route('/add/karyawan',methods=['POST']) 
@roles_required('admin','HRD','karu')
def add_karyawan():
    nama = request.json['nama']
    email = request.json['email']
    jk = request.json['jk']
    tgl_lahir = request.json['tgl_lahir']
    print(tgl_lahir)
    no_hp = request.json['no_hp']
    posisi = request.json['posisi']
    ruangan = request.json['ruangan']
    alamat = request.json['alamat']
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*)+1 FROM karyawan")
    no_urut = cur.fetchone()
    print(no_urut)
    nip = generate_nip(tgl_lahir,jk,no_urut)
    print(nip)
    today =  datetime.today()
    cur.execute("INSERT INTO `karyawan`(`nip`, `nama`,`posisi`,`ruangan`, `email`, `gender`, `ttl`, `alamat`, `no_hp`, `deleted_at`, `created_at`, `updated_at`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",(nip,nama,posisi,ruangan,email,jk,tgl_lahir,alamat,no_hp,'',today,today))
    mysql.connection.commit()
    return jsonify({"data":None,"meta":{"code":200,"message":"Berhasil ubah Data","status":"success"}})
@web.route('/add/shift',methods=['POST']) 
@roles_required('admin','HRD')
def add_shift():
    nama = request.json['nama']
    jam_berangkat = request.json['jam_berangkat']
    jam_pulang = request.json['jam_pulang']
    jam_kerja = request.json['jam_kerja']
    # jam_berangkat = jam_berangkat.split(".")
    # jam_pulang = jam_pulang.split(".")
    # jam_kerja = jam_kerja.split(".")

    # print(jam_berangkat)
    # berangkat = ""
    # for i in jam_berangkat:
    #     if i == jam_berangkat.last_index():
    #         berangkat =+str(i)
    #         berangkat =+":00"
    #     else:
    #         berangkat =+str(i)
    #         berangkat =+":"
    # pulang = ""
    # for i in jam_pulang:
    #     if i == jam_pulang.last_index():
    #         pulang =+str(i)
    #         pulang =+":00"
    #     else:
    #         pulang =+str(i)
    #         pulang =+":"
    # kerja = ""
    # for i in jam_kerja:
    #     if i == jam_kerja.last_index():
    #         kerja =+str(i)
    #         kerja =+":00"
    #     else:
    #         kerja =+str(i)
    #         kerja =+":"
    # print(jam_pulang)
    # print(jam_kerja)
    # jam_berangkat = datetime. strptime(jam_berangkat, '%H:%M:%S')
    # jam_pulang = datetime. strptime(jam_pulang, '%H:%M:%S')
    # jam_kerja = datetime. strptime(jam_kerja, '%H:%M:%S')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `shift`(`Nama`,`berangkat`,`pulang`, `jam_kerja`) VALUES (%s,%s,%s,%s) ",(nama,jam_berangkat,jam_pulang,jam_kerja))
    mysql.connection.commit()
    return jsonify({"data":None,"meta":{"code":200,"message":"Berhasil ubah Data","status":"success"}})

@web.route('/edit/admin/<no>',methods=['GET','PUT']) 
@roles_required('admin')
def editformadmin(no):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT nip,nama,email,gender,ttl,no_hp,alamat FROM admin where nip= %s",(no,))
        admin = cur.fetchall()
        cur.execute('SELECT nama from ruangan')
        ruangan = cur.fetchall()
        return render_template('dashboard/formedit.html',init="admin",data=admin,ruangan=ruangan)
    elif request.method == "PUT":
        cur = mysql.connection.cursor()
        nama = request.json['nama']
        print(nama)
        email = request.json[ 'email']
        gender = request.json[ 'gender']
        tanggal_lahir = request.json['tanggal_lahir']
        alamat = request.json['alamat']
        no_hp = request.json['no_hp']
        cur.execute("UPDATE admin SET nama=%s, email=%s, gender=%s, ttl=%s, alamat=%s,no_hp=%s where nip= %s",(nama,email,gender,tanggal_lahir,alamat,no_hp, str(no),))
        mysql.connection.commit()
        return jsonify({"status":"sukses","url":"data_admin?msg='data berhasil diedit'"})
@web.route('/edit/hrd/<no>',methods=['GET','PUT']) 
@roles_required('admin','HRD')
def editformhrd(no):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT nip,nama,email,gender,ttl,no_hp,alamat FROM hrd where nip= %s",(no,))
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
        return jsonify({"msg":"sukses","url":"data_hrd?msg='data berhasil diedit'"})
    
@web.route('/edit/karu/<no>',methods=['GET','PUT']) 
@roles_required('admin','HRD','karu')
def editformkaru(no):
    
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT nip,nama,email,gender,ttl,no_hp,alamat,penempatan FROM karu where nip= %s",(no,))
        karu = cur.fetchall()
        cur.execute('SELECT nama from ruangan')
        ruangan = cur.fetchall()
        return render_template('dashboard/formedit.html',init="karu",data=karu,ruangan=ruangan)
    
    elif request.method == "PUT":
        cur = mysql.connection.cursor()
        nama = request.json['nama']
        email = request.json[ 'email']
        gender = request.json[ 'gender']
        penempatan = request.json[ 'ruangan']
        tanggal_lahir = request.json['tanggal_lahir']
        alamat = request.json['alamat']
        no_hp = request.json['no_hp']
        cur.execute("UPDATE karu SET nama=%s, email=%s, gender=%s, penempatan=%s, ttl=%s, alamat=%s,no_hp=%s where nip= %s",(nama,email,gender,penempatan, tanggal_lahir,alamat,no_hp, no,))
        mysql.connection.commit()
        return jsonify({"msg":"sukses","url":"data_karu?msg='data berhasil diedit'"})

@web.route('/edit/karyawan/<no>',methods=['GET','PUT']) 
@roles_required('admin','HRD','karu')
def editformkaryawan(no):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT nip,nama,email,gender,ttl,no_hp,alamat,posisi,ruangan FROM karyawan where nip= %s",(no,))
        karyawan = cur.fetchall()
        cur.execute('SELECT nama from ruangan')
        ruangan = cur.fetchall()
        return render_template('dashboard/formedit.html',init="karyawan",data=karyawan,ruangan=ruangan)
    elif request.method == "PUT":
        cur = mysql.connection.cursor()
        nama = request.json['nama']
        email = request.json[ 'email']
        gender = request.json[ 'gender']
        posisi = request.json[ 'posisi']
        ruangan = request.json[ 'ruangan']
        tanggal_lahir = request.json['tanggal_lahir']
        alamat = request.json['alamat']
        no_hp = request.json['no_hp']
        cur.execute("UPDATE karyawan SET nama=%s, email=%s,posisi=%s,ruangan=%s, gender=%s, ttl=%s, alamat=%s,no_hp=%s where nip= %s",(nama,email,posisi, ruangan , gender,tanggal_lahir,alamat,no_hp, no,))
        mysql.connection.commit()
        return jsonify({"msg":"sukses","url":"data_karyawan?msg='data berhasil diedit'"})

@web.route('/edit/shift/<no>',methods=['GET','PUT']) 
@roles_required('admin','HRD','karu')
def editformshift(no):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM shift where id= %s",(no,))
        shift = cur.fetchall()
        berangkat = shift[0][2]
        pulang = shift[0][3]
        jam_kerja = shift[0][4]
        berangkat = str(berangkat).zfill(8)
        pulang = str(pulang).zfill(8)
        jam_kerja = str(jam_kerja).zfill(8)
        cur.execute('SELECT nama from ruangan')
        ruangan = cur.fetchall()
        return render_template('dashboard/formedit.html',init="shift",data=shift,berangkat=berangkat,pulang=pulang,jam_kerja=jam_kerja, ruangan=ruangan)
    elif request.method == "PUT":
        cur = mysql.connection.cursor()
        nama = request.json['nama']
        berangkat = request.json[ 'jam_berangkat']
        pulang = request.json[ 'jam_pulang']
        jam_kerja = request.json[ 'jam_berangkat']
        cur.execute("UPDATE shift SET nama=%s, berangkat=%s,pulang=%s,jam_kerja=%s where id= %s",(nama,berangkat,pulang,jam_kerja , no,))
        mysql.connection.commit()
        return jsonify({"msg":"sukses","url":"shift?msg='data berhasil diedit'"})
@web.route('/edit/jadwal/<no>',methods=['GET','PUT']) 
@roles_required('admin','HRD','karu')
def editformjadwal(no):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT jadwal.id,jadwal.nip, karyawan.nama, jadwal.shift,karyawan.ruangan,jadwal.tanggal FROM jadwal INNER JOIN karyawan ON karyawan.nip = jadwal.nip WHERE jadwal.id = %s",(no,))
        jadwal = cur.fetchall()
        return redirect(url_for("/form/jadwal"))
    elif request.method == "PUT":
        cur = mysql.connection.cursor()
        nama = request.json['nama']
        berangkat = request.json[ 'jam_berangkat']
        pulang = request.json[ 'jam_pulang']
        jam_kerja = request.json[ 'jam_berangkat']
        cur.execute("UPDATE jadwal SET nama=%s, berangkat=%s,pulang=%s,jam_kerja=%s where id= %s",(nama,berangkat,pulang,jam_kerja , no,))
        mysql.connection.commit()
        return jsonify({"msg":"sukses","url":"jadwal?msg='data berhasil diedit'"})
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
    cur.execute("SELECT jadwal.id,jadwal.nip, karyawan.nama, jadwal.shift,karyawan.ruangan,jadwal.tanggal FROM jadwal INNER JOIN karyawan ON karyawan.nip = jadwal.nip")
    jadwal = cur.fetchall()
    return redirect(url_for("/form/jadwal"))
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
@roles_required('admin','HRD','karu')
def deleteuser(init,id):
    try:
        if request.method == 'DELETE':
            warga = mysql.connection.cursor()
            where = ""
            if init == 'shift' :
                where = "id"
            elif init == 'jadwal':
                where = "id"
            else:
                where = "nip"
            warga = mysql.connection.cursor()
            warga.execute("DELETE FROM "+init+" where "+where+" = "+id)
            mysql.connection.commit()
            
            return jsonify({"data":None,"meta":{"code":200,"message":"Berhasil ubah Data","status":"success"}})
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
