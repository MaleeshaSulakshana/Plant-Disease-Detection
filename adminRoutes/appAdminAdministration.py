import os
import sys
import hashlib
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

appAdminAdministration = Blueprint("appAdminAdministration", __name__)
sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

import utils
import dbAdmin as ad

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


# Route for view admins details
@appAdminAdministration.route('/admin_details')
def admin_details():

    if 'adminId' in session:
        return render_template('Admin/admin_details.html', details=ad.get_all_admin_recodes(session['adminId']))

    else:
        return redirect('login')


# Route for view admins details
@appAdminAdministration.route('/add_admin')
def add_admin():

    if 'adminId' in session:
        return render_template('Admin/add_admin.html')

    else:
        return redirect('login')


# Route for delete admin recode
@appAdminAdministration.route('/delete_admin', methods=['GET', 'POST'])
def delete_admin():
    if 'adminId' in session:
        id = request.args.get('id', default='no-id')

        success = ad.delete_admin_recode(id)
        return redirect(url_for('appAdminAdministration.admin_details'))

    else:
        return redirect('login')


# Route for add admin recode
@appAdminAdministration.route('/add_admin_recode', methods=['GET', 'POST'])
def add_admin_recode():

    if request.method == "POST":

        if 'adminId' in session:

            name = request.form.get('name')
            email = request.form.get('email')
            psw = request.form.get('psw')
            cpsw = request.form.get('cpsw')

            if len(name) == 0 or len(email) == 0 or len(psw) == 0 or len(cpsw) == 0:
                return jsonify({'error': "Fields are empty!"})

            elif psw != cpsw:
                return jsonify({'error': "Password and confirm password not matched!"})

            else:
                # Insert recode
                id = name + utils.random_number()
                if ad.add_new_admin_recode(id, name, email, hashlib.md5(psw.encode()).hexdigest()) < 1:
                    return jsonify({'error': "Some error occur!"})

                else:
                    return jsonify({'success': "New administer add successfully!"})

    return redirect('login')
