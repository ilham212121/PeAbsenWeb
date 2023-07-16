from functools import wraps
import pandas as pd
import random
import string,os
from time import time
import time
import xlsxwriter
from application import app,mysql,allowed_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, session, url_for,request,flash, jsonify
auth = Blueprint('auth', __name__)

a=time.localtime()
tanggal=""+str(time.gmtime().tm_year)+"-"+str(a.tm_mon)+"-"+str(a.tm_mday)+""

def convertTuple(tup):
    return ''.join([str(x) for x in tup])

def roles_required(*role_names):
    def decorator(original_route):
        @wraps(original_route)
        def decorated_route(*args, **kwargs):
            if 'loggedin' in session:
            # User is loggedin show them the home page
                print(session['time'])
                if session['time'] != ""+str(time.gmtime().tm_year)+"-"+str(time.localtime().tm_mon)+"-"+str(time.localtime().tm_mday)+"":
                    print('session expired')
                    session.pop('loggedin', None)
                    session.pop('id', None)
                    session.pop('role', None)
                    session.pop('username', None)
                    session.pop('time', None)
                    return redirect(url_for('auth.index'))
                if not session['role'] in role_names:
                    print('The user does not have this role.')
                    return redirect(url_for('auth.index'))
                else:
                    print(session['time'])
                    print(""+str(time.localtime().tm_year)+"-"+str(time.localtime().tm_mon)+"-"+str(time.localtime().tm_mday)+"")
                    print('The user is in this role.')
                    return original_route(*args, **kwargs)
            else:
                return redirect(url_for('auth.index'))
        return decorated_route
    return decorator 

@auth.route('/') 
def index():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        role_names=['admin','HRD','karu']
        if not session['role'] in role_names:
            print('The user does not have this role.')
            return redirect(url_for('auth.index'))
        else:
            print('The user is in this role.')
            return redirect(url_for('auth.dashboard'))
    else:
        message = request.args.get('alert')
        return render_template('index.html',message=message)
@auth.route('/dashboard') 
def dashboard():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        role_names=['admin','HRD','karu']
        if not session['role'] in role_names:
            print('The user does not have this role.')
            return redirect(url_for('auth.index'))
        else:
            print('The user is in this role.')
            cur = mysql.connection.cursor()
            print(tanggal)
            cur.execute(
                'SELECT dataabsen.id, dataabsen.nip, karyawan.nama,jadwal.ruangan,shift.nama,`latitude`, `longitude`, `foto`, dataabsen.tanggal, `waktu`, dataabsen.status'
                ' FROM dataabsen INNER JOIN karyawan ON karyawan.nip = dataabsen.nip INNER JOIN jadwal on karyawan.nip = jadwal.nip INNER JOIN shift on shift.nama = jadwal.shift '
                ' WHERE dataabsen.status = "telat" AND dataabsen.tanggal = "'+tanggal+'"'
                ' GROUP by dataabsen.id DESC')
            datatelat = cur.fetchall()
            print(datatelat)
            tahun=str(time.gmtime().tm_year)
            bulan=a.tm_mon
            nmbulan=''
            jumlahHari=''
            if bulan==1: 
                nmbulan="jan"
                jumlahHari=31
            elif bulan==2:
                nmbulan="feb"
                if((tahun %4 == 0 and tahun % 100 !=0) or tahun % 400 == 0):
                    jumlahHari = 29
                else:
                    jumlahHari = 28
            elif bulan==3:
                nmbulan="mar"
                jumlahHari= 31
            elif bulan==4:
                nmbulan="apr"
                jumlahHari = 30
            elif bulan==5:
                nmbulan="mei"
                jumlahHari = 31
            elif bulan== 6:
                nmbulan="jun"
                jumlahHari = 30
            elif bulan== 7:
                nmbulan="jul"
                jumlahHari = 31
            elif bulan== 8:
                nmbulan="agu"
                jumlahHari = 31
            elif bulan== 9:
                nmbulan="sep"
                jumlahHari = 30
            elif bulan== 10:
                nmbulan="okt"
                jumlahHari = 31
            elif bulan== 11:
                nmbulan="nov"
                jumlahHari = 30
            elif bulan== 12:
                nmbulan="des"
                jumlahHari =31
            
            tgl = a.tm_mday

            cur.execute(
                'SELECT nama from ruangan')
            ruangan = cur.fetchall()
            
            print(jumlahHari)
            setengahbln = jumlahHari/2
            if tgl < setengahbln:
                lbl = []
                data =[]
                for i in range(1,int(setengahbln)):
                    print(i)
                    lbl.append(str(nmbulan)+" "+str(i))
                    cari = ""+str(time.gmtime().tm_year)+"-"+str(a.tm_mon)+"-"+str(i)+""
                    cur.execute('SELECT Count(*) from dataabsen where tanggal = %s and status= "telat" ',(cari,))
                    item = cur.fetchone()
                    if item == None:
                        data.append(0)
                    else:
                        data.append(item)
            else:
                lbl = []
                data =[]
                mulai = int(setengahbln)
                for i in range(mulai,jumlahHari):
                    print(i)
                    lbl.append(str(nmbulan)+" "+str(i))
                    cari = ""+str(time.gmtime().tm_year)+"-"+str(a.tm_mon)+"-"+str(i)+""
                    print(cari)
                    cur.execute('SELECT Count(*) from dataabsen where tanggal = %s and status= "telat" ',(cari,))
                    item = cur.fetchone()
                    print(item)
                    if item == None:
                        data.append(0)
                    else:
                        data.append(item)
            print(data)
            print(session['role'])
            cur.execute('SELECT Count(*) from karyawan where posisi ="Perawat"')
            perawat = cur.fetchone()
            cur.execute('SELECT Count(*) from karyawan where posisi ="Dokter Umum"')
            dokter_umum = cur.fetchone()
            cur.execute('SELECT Count(*) from karu ')
            karu = cur.fetchone() 
            cur.execute('SELECT Count(*) from admin')
            admin = cur.fetchone()
            lblkaryawan = ['perawat','dokter umum', 'kepala ruangan','admin']
            datakaryawan = [[int(convertTuple(perawat))],[int(convertTuple(dokter_umum))],[int(convertTuple(karu))],[int(convertTuple(admin))]]
            print(datakaryawan)

            # Create an new Excel file and add a worksheet.
            excellpth = os.path.join(app.config['FOLDER_EXCELL'], 'table-kedisiplinan.xlsx')
            workbook = xlsxwriter.Workbook(excellpth)
            worksheet = workbook.add_worksheet()

            # Insert an image.
            imgpth = os.path.join(app.config['FOLDER_ABSEN'], '2207120012022-7-1676AM.jpg')
            worksheet.write('A1', 'bulan')
            worksheet.write('B1', 'jumlah telat')

            for i in range(len(lbl)):
                print(str(i+2)+'y', data[int(i)])
                worksheet.write('A'+str(i+2)+'', lbl[int(i)])
                worksheet.write('B'+str(i+2)+'', data[int(i)][0])
           
            workbook.close()
            
            excellpth = os.path.join(app.config['FOLDER_EXCELL'], 'table-karyawan.xlsx')
            workbook = xlsxwriter.Workbook(excellpth)
            worksheet = workbook.add_worksheet()

            # Widen the first column to make the text clearer.
            worksheet.write('A1', 'posisi karyawan')
            worksheet.write('B1', 'jumlah karyawan')

            for i in range(len(lblkaryawan)):
                worksheet.write('A'+str(i+2)+'', lblkaryawan[int(i)])
                worksheet.write('B'+str(i+2)+'', datakaryawan[int(i)][0])

            workbook.close()
            
            excellpth = os.path.join(app.config['FOLDER_EXCELL'], 'table-telat-hari-ini.xlsx')
            lbltlt = ['NIP','Nama','Ruangan','Shift','Latitude','Longitude','Foto','Tanggal','Waktu','Status']
            
            workbook = xlsxwriter.Workbook(excellpth)
            worksheet = workbook.add_worksheet()
            
            # Widen the image column to make space for the image clearer.
            worksheet.set_column("G:G", 23)
            print(range(len(lbltlt)))
            kolom = ["A","B","C","D","E","F","G","H","I","J"]
            for j in range(len(datatelat)):
                worksheet.set_row(int(j+1), 125)
                for i in  range(len(kolom)):
                    print(kolom[int(i)])
                    # Insert an image.
                    worksheet.write(str(kolom[i])+'1', lbltlt[int(i)])
                    if str(kolom[int(i)]) == "G":
                        imgpth = os.path.join(app.config['FOLDER_ABSEN'], datatelat[j][int(i+1)])
                        worksheet.insert_image(str(kolom[int(i)])+str(j+2),imgpth,{'x_scale': 0.5, 'y_scale': 0.5})
                    else:
                        #insert data
                        worksheet.write(str(kolom[i])+str(j+2), datatelat[j][int(i+1)])
                    
            workbook.close()
            # data={}
            # z= ''
            # for i in datatelat :
            #     a = []
            #     for j in datatelat[i]:
            #         a.append(datatelat[i][j])
            #     b = ''
            # data = {'p': ['computer', 'printer', 'tablet', 'monitor'],
            #         'price': [1200, 150, 300, 450]
            #         }

            # df = pd.DataFrame(data)

            # df.to_excel(r'C:\Users\Ilhkam\Documents\GitHub\PeAbsenWeb\application\static\api\table-kedisiplin.xlsx', index=False)
            # data = {'product_name': ['computer', 'printer', 'tablet', 'monitor'],
            #         'price': [1200, 150, 300, 450]
            #         }

            # df = pd.DataFrame(data)

            # df.to_excel(r'C:\Users\Ilham\Documents\GitHub\PeAbsenWeb\application\static\api\table-karyawan.xlsx', index=False)
            # data = {'product_name': ['computer', 'printer', 'tablet', 'monitor'],
            #         'price': [1200, 150, 300, 450]
            #         }

            # df = pd.DataFrame(data)

            # df.to_excel(r'C:\Users\Ilham\Documents\GitHub\PeAbsenWeb\application\static\api\table-telat-hari-ini.xlsx', index=False)
            print(datatelat)
            return render_template('dashboard/index.html',datatelat=datatelat,ruangan=ruangan,nmbulan=nmbulan, lbl=lbl,data=data,lblkaryawan=lblkaryawan,datakaryawan=datakaryawan)   
    else:
        return redirect(url_for('auth.index'))


@auth.route('/api/login',methods=['POST'])
def apilogindashboard():
    cur = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    cur.execute("SELECT * FROM login WHERE nip = %s" , (nip,))
    datalogin = cur.fetchone()
    print(datalogin)
    if datalogin is None:
        print("laka")
        cur.close()
        return redirect(url_for('auth.index',alert="maaf nip tidak ada"))
    elif not check_password_hash(datalogin[1],password):
        cur.close()
        return redirect(url_for('auth.index',alert="maaf password salah"))
    else:
        print(datalogin[2])
        if datalogin[2]=='admin':
            cur.execute("SELECT login.nip,login.role, admin.nama,admin.email,admin.alamat,admin.no_hp FROM login INNER JOIN admin ON login.nip = admin.nip WHERE login.nip = %s" , (nip,))
            datasession= cur.fetchone()
        elif datalogin[2]=='HRD':
            print(nip)
            cur.execute("SELECT login.nip,login.role, hrd.nama,hrd.email,hrd.alamat,hrd.no_hp FROM login INNER JOIN hrd ON login.nip = hrd.nip WHERE login.nip = %s" , (nip,))
            datasession= cur.fetchone()
            print(datasession)
        elif datalogin[2]=='karu':
            cur.execute("SELECT login.nip,login.role, karu.nama,karu.email,karu.alamat,karu.no_hp FROM login INNER JOIN karu ON login.nip = karu.nip WHERE login.nip = %s " , (nip,))
            datasession= cur.fetchone()
        else:
            return "maaf nip tida ada"
        session['loggedin'] = True
        session['id'] = datasession[0]
        session['role'] = datasession[1]
        session['username'] = datasession[2]
        session['time'] = tanggal
        cur.close()
        return redirect(url_for('auth.dashboard'))
@auth.route('/api/login/karyawan',methods=['POST'])
def apilogin():
    print(generate_password_hash("baru123"))
    cur = mysql.connection.cursor()
    nip = request.form['nip']
    access_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 15))
    refresh_token=access_token
    password = request.form['password']
    cur.execute("SELECT * FROM login WHERE role = 'karyawan'and nip = %s" , (nip,))
    datalogin= cur.fetchall()
    if str(datalogin) == '()':
        cur.close()
        print("maaf nip tidak ada")
        return jsonify({"msg":"maaf nip tidak ada"}),401
    elif not check_password_hash(datalogin[0][1],password):
        cur.close()
        print("maaf password salah")
        return jsonify({"msg":"maaf password salah"}),401
    else:
        cur.execute("UPDATE login SET token = %s WHERE role = 'karyawan' and nip = %s" , (refresh_token,nip))
        mysql.connection.commit()
        cur.execute("SELECT * FROM karyawan WHERE nip = %s" , (nip,))
        datalogin = cur.fetchall()
        print(access_token)
        cur.close()
        return jsonify({"data":{"nip":datalogin[0][0],"nama":datalogin[0][1],"posisi":datalogin[0][2],"gender":datalogin[0][4],"ttl":str(datalogin[0][5]),"email":datalogin[0][6],"no_hp":datalogin[0][7],"alamat":datalogin[0][8]},"msg":"login berhasil","token":refresh_token}),200
@auth.route('/logout')
@roles_required('admin','HRD','karu')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('role', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('auth.index'))

