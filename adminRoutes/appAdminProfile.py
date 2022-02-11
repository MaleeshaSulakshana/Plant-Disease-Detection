import os
import sys
import hashlib
from flask import Blueprint, render_template, redirect, jsonify, request, session

appAdminProfile = Blueprint("appAdminProfile", __name__)
sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

import dbAdmin as ad

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


# Route for admin profile
@appAdminProfile.route('/admin_profile')
def admin_profile():

    if 'adminId' in session:
        return render_template('Admin/admin_profile.html', details=ad.get_admin_details(session['adminId']))

    else:
        return redirect('login')


# Route for add admin recode
@appAdminProfile.route('/update_admin_profile', methods=['GET', 'POST'])
def update_admin_profile():

    if request.method == "POST":

        if 'adminId' in session:

            name = request.form.get('name')

            if len(name) == 0:
                return jsonify({'error': "Fields are empty!"})

            else:
                if ad.update_admin_recode_details(session['adminId'], name) < 1:
                    return jsonify({'error': "Some error occur!"})

                else:
                    return jsonify({'success': "Admin profile update successfully!"})

    return redirect('login')


# Route for admin profile
@appAdminProfile.route('/admin_change_psw')
def admin_change_psw():

    if 'adminId' in session:
        return render_template('Admin/admin_change_psw.html')

    else:
        return redirect('login')


# Route for add admin recode
@appAdminProfile.route('/psw_update', methods=['GET', 'POST'])
def psw_update():

    if request.method == "POST":

        if 'adminId' in session:

            psw = request.form.get('txt_psw', default='')
            cpsw = request.form.get('txt_cpsw', default='')

            if len(psw) == 0 or len(cpsw) == 0:
                return jsonify({'error': "Fields are empty!"})

            elif psw != cpsw:
                return jsonify({'error': "Password and confirm password not matched!"})

            else:
                if ad.update_admin_psw(session['adminId'], hashlib.md5(psw.encode()).hexdigest()) < 1:
                    return jsonify({'error': "Some error occur!"})

                else:
                    return jsonify({'success': "Admin profile password update successfully!"})

    return redirect('login')
