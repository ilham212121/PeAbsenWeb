from flask import Blueprint, render_template, redirect, session, url_for,request,flash, jsonify
auth = Blueprint('auth', __name__)

@auth.route('/dashboard') 
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
