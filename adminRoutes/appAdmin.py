import os
import sys
import hashlib
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

appAdmin = Blueprint("appAdmin", __name__)
sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

import utils
import dbAdmin as ad

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


# Route for admin dashboard page
@appAdmin.route('/Admin')
def admin():
    if 'adminId' in session:
        return render_template('Admin/index.html', date=utils.date_picker(),
                               prediction_count=ad.get_prediction_count())

    else:
        return redirect('login')


# Route for return admin name
@appAdmin.route('/admin_name', methods=['GET', 'POST'])
def admin_name():
    if 'adminId' in session:
        data = ad.get_admin_name(session['adminId'])
        if len(data) != 0:
            return jsonify({"admin_name": data})

    return jsonify({'admin_name': "Admin"})


# Route for admin login page
@appAdmin.route('/login')
def login():

    if 'adminId' in session:
        return redirect('Admin')

    else:
        return render_template('Admin/login.html')


# Route for admin logout
@appAdmin.route('/logout')
def logout():
    if 'adminId' in session:
        session.pop('adminId', None)

    return redirect(url_for('appAdmin.admin'))


# Route for admin login
@appAdmin.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == "POST":

        if 'adminId' in session:
            return jsonify({'redirect': url_for('appAdmin.admin')})

        else:
            txtEmail = request.form.get('txtEmail')
            txtPsw = request.form.get('txtPsw')

            if len(txtEmail) == 0 or len(txtPsw) == 0:
                return jsonify({'error': "Fields are empty!"})

            else:
                # Check login
                adminId = ad.admin_login(
                    txtEmail, hashlib.md5(txtPsw.encode()).hexdigest())
                if len(adminId) < 1:
                    return jsonify({'error': "Email or Password incorrect!"})

                else:
                    session['adminId'] = str(adminId[0][0])
                    return jsonify({'redirect': url_for('appAdmin.admin')})

    return redirect('login')


# Route for add admin chart data
@ appAdmin.route('/adminChartDetails', methods=['GET', 'POST'])
def adminChartDetails():
    if request.method == "POST":
        prediction_details = ad.get_week_prediction_count()
        disease_details = ad.get_plant_diseases_count()
        accuracy_details = ad.get_prediction_accuracy()

        days = []
        day_values = []
        for i in prediction_details:
            days.append(str(i[0].strftime("%A")))
            day_values.append(str(i[1]))

        prediction = [days, day_values]

        plant = []
        disease_count = []
        presentage_count = []
        plant_count = sum([int(i[1]) for i in disease_details])
        for item in disease_details:
            plant.append(str(item[0]))
            disease_count.append(str(item[1]))
            presentage_count.append((int(item[1]) / plant_count) * 100)

        disease = [plant, disease_count]
        plantPercentage = [plant, presentage_count]

        days = []
        accuracy_values = []
        for i in accuracy_details:
            days.append(str(i[0].strftime("%A")))
            accuracy_values.append(str(i[1]))

        accuracy = [days, accuracy_values]
        return jsonify({'prediction': prediction, 'disease': disease,
                        'accuracy': accuracy, 'plantPercentage': plantPercentage})
