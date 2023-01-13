from functools import wraps
import random
import string
from time import time
import time
from application import app,mysql,allowed_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, session, url_for,request,flash, jsonify
auth = Blueprint('auth', __name__)

a=time.localtime()
tanggal=""+str(time.gmtime().tm_year)+"-"+str(a.tm_mon)+"-"+str(a.tm_mday)+""
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
            return render_template('dashboard/index.html', username=session['username'])
    else:
        return render_template('index.html')
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
            return render_template('dashboard/index.html', username=session['username'])
    else:
        return redirect(url_for('auth.index'))
@auth.route('/api/login',methods=['POST'])
def apilogindashboard():
    cur = mysql.connection.cursor()
    nip = request.form['nip']
    password = request.form['password']
    cur.execute("SELECT * FROM login WHERE nip = %s" , (nip,))
    datalogin = cur.fetchone()
    if str(datalogin) == '':
        cur.close()
        return "maaf nip tida ada"
    elif not check_password_hash(datalogin[1],password):
        cur.close()
        return "maaf password salah"
    else:
        if datalogin[2]=='admin':
            cur.execute("SELECT login.nip,login.role, admin.nama,admin.email,admin.alamat,admin.no_hp FROM login INNER JOIN admin ON login.nip = admin.nip WHERE login.nip = %s" , (nip,))
            datalogin= cur.fetchone()
        elif datalogin[2]=='HRD':
            cur.execute("SELECT login.nip,login.role, hrd.nama,hrd.email,hrd.alamat,hrd.no_hp FROM login INNER JOIN hrd ON login.nip = hrd.nip WHERE login.nip = %s" , (nip,))
            datalogin= cur.fetchone()
        elif datalogin[2]=='karu':
            cur.execute("SELECT login.nip,login.role, karu.nama,karu.email,karu.alamat,karu.no_hp FROM login INNER JOIN karu ON login.nip = karu.nip WHERE login.nip = %s " , (nip,))
            datalogin= cur.fetchone()
        else:
            return "maaf nip tida ada"
        session['loggedin'] = True
        session['id'] = datalogin[0]
        session['role'] = datalogin[1]
        session['username'] = datalogin[2]
        session['time'] = tanggal
        cur.close()
        return redirect(url_for('auth.dashboard'))
@auth.route('/api/login/karyawan',methods=['POST'])
def apilogin():
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
        return jsonify({"data":{"nip":datalogin[0][0],"nama":datalogin[0][1],"posisi":datalogin[0][2],"gender":datalogin[0][3],"ttl":str(datalogin[0][4]),"email":datalogin[0][5],"no_hp":datalogin[0][6],"alamat":datalogin[0][7]},"msg":"login berhasil","token":refresh_token}),200
@auth.route('/logout')
@roles_required('admin','HRD','karu')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('role', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('auth.index'))