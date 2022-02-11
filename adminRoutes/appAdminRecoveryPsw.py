import os
import sys
import hashlib
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

appAdminRecoveryPsw = Blueprint("appAdminRecoveryPsw", __name__)
sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))
sys.path.append(os.path.abspath('python/psw_recovery'))

import utils
import dbAdmin as ad
import email_sender

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


# Route for admin psw recovery page
@appAdminRecoveryPsw.route('/forget_password')
def forget_password():

    if 'adminId' in session:
        return redirect('Admin')

    else:
        return render_template('Admin/forget_password.html')


# Route for admin logout
@appAdminRecoveryPsw.route('/password_recovery')
def password_recovery():
    return render_template('Admin/psw_recovery.html')


# Route for admin send recovery code
@appAdminRecoveryPsw.route('/send_recovery_code', methods=['GET', 'POST'])
def send_recovery_code():

    if request.method == "POST":

        if 'adminId' in session:
            return jsonify({'redirect': url_for('appAdmin.admin')})

        else:
            txtEmail = request.form.get('txtEmail')

            if len(txtEmail) == 0:
                return jsonify({'error': "Fields are empty!"})

            else:
                # Check login
                if ad.email_exist(txtEmail) < 1:
                    return jsonify({'error': "Your email incorrect!"})

                else:
                    recovery_code = utils.random_number()
                    email_sender.send_recovery_code(txtEmail, recovery_code)
                    session['forgetPswEmail'] = str(txtEmail)
                    session['recovery_code'] = recovery_code

                    return jsonify({'exist': "exist"})

    return redirect('login')


# Route for admin send recovery code
@appAdminRecoveryPsw.route('/re_send_recovery_code', methods=['GET', 'POST'])
def re_send_recovery_code():

    if request.method == "POST":

        if 'adminId' in session:
            return jsonify({'redirect': url_for('appAdmin.admin')})

        else:
            resend = request.form.get('resend')
            if resend == 'resend':
                if 'forgetPswEmail' in session:
                    recovery_code = utils.random_number()
                    email_sender.send_recovery_code(
                        session['forgetPswEmail'], recovery_code)
                    session['recovery_code'] = recovery_code

                    return jsonify({'success': "Recovery code sent your email!"})

            return jsonify({'error': "Some error occur!"})

    return redirect('login')


# Route for admin send recovery code
@appAdminRecoveryPsw.route('/psw_recovery', methods=['GET', 'POST'])
def psw_recovery():

    if request.method == "POST":

        if 'adminId' in session:
            return jsonify({'redirect': url_for('appAdmin.admin')})

        else:
            txtCode = request.form.get('txtCode')
            if len(txtCode) == 0:
                return jsonify({'error': "Fields are empty!"})

            else:
                # Check recovery code
                if txtCode != session['recovery_code']:
                    return jsonify({'error': "Recovery code incorrect!"})

                else:

                    session.pop('recovery_code', None)
                    return jsonify({'redirect': url_for('appAdminRecoveryPsw.password_recovery')})

    return redirect('login')


# Route for admin change recovery psw
@appAdminRecoveryPsw.route('/change_recovery_psw', methods=['GET', 'POST'])
def change_recovery_psw():

    if request.method == "POST":

        if 'adminId' in session:
            return jsonify({'redirect': url_for('appAdmin.admin')})

        elif 'forgetPswEmail' not in session:
            return jsonify({'redirect': url_for('appAdmin.login')})

        else:
            txtPsw = request.form.get('txtPsw')
            txtCPsw = request.form.get('txtCPsw')

            if len(txtPsw) == 0 or len(txtCPsw) == 0:
                return jsonify({'error': "Fields are empty!"})

            elif txtPsw != txtCPsw:
                return jsonify({'error': "Password & confirm password not matched!"})

            else:
                # Update psw
                if ad.update_admin_recovery_psw(session['forgetPswEmail'], hashlib.md5(txtPsw.encode()).hexdigest()) < 1:
                    return jsonify({'error': "Password not updated!"})

                else:
                    session.pop('forgetPswEmail', None)
                    return jsonify({'redirect': url_for('appAdmin.login')})

    return redirect('login')
