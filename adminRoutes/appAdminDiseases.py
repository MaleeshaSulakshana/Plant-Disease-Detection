import os
import sys
import shutil
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

appAdminDiseases = Blueprint("appAdminDiseases", __name__)
sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

import utils
import dbAdmin as ad

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


# Route for admin diseases view page
@appAdminDiseases.route('/view_diseases')
def view_diseases():

    if 'adminId' in session:
        return render_template('Admin/view_diseases.html', details=ad.get_diseases_details())

    else:
        return redirect('login')


# Route for admin update disease images
@appAdminDiseases.route('/update_disease_image', methods=['GET', 'POST'])
def update_disease_image():

    if 'adminId' in session:
        image_id = int(request.args.get('image_id', None))
        disease_id = request.args.get('disease_id', None)

        if (image_id is not None or image_id != '' or disease_id is not None or disease_id != ''):
            if (image_id >= 0 and image_id <= 5) and ad.is_exist_disease(disease_id) > 0:
                if image_id == 0:
                    image = 'thumbnail'
                else:
                    image = 'image' + str(image_id)

                return render_template('Admin/update_disease_image.html', image_id=image,
                                       disease_id=disease_id, image_name=ad.get_disease_image_name(image, disease_id))

        return redirect(url_for('appAdminDiseases.view_diseases'))

    else:
        return redirect(url_for('appAdmin.login'))


# Route for update disease images
@appAdminDiseases.route('/update_image', methods=['GET', 'POST'])
def update_image():

    if 'adminId' in session:
        if request.method == "POST":

            image = request.files.get('input_image')
            image_id = request.form.get('txt_image_id')
            disease_id = request.form.get('txt_disease_id')

            if (image is None or image == '' or disease_id is None or disease_id == ''
                    or image_id is None or image_id == ''):
                return jsonify({'error': "Fields are empty!"})

            else:
                save_folder = os.path.join(
                    root, 'templates/images/diseases/')
                db_image_name = ad.get_disease_image_name(
                    image_id, disease_id)
                pre_image_path = save_folder + db_image_name
                if db_image_name != 'None':
                    if os.path.isdir(pre_image_path):
                        shutil.rmtree(pre_image_path)

                image_name = utils.file_save(image, save_folder)
                if ad.update_disease_image(image_id, image_name, disease_id) > 0:
                    return jsonify({'success': "Image update successfully!"})

                else:
                    return jsonify({'error': "Some error occur!"})

    return redirect(url_for('appAdmin.login'))


# Route for delete disease images
@appAdminDiseases.route('/delete_image', methods=['GET', 'POST'])
def delete_image():

    if 'adminId' in session:
        if request.method == "POST":

            image_id = request.form.get('txt_image_id')
            disease_id = request.form.get('txt_disease_id')

            if (disease_id is None or disease_id == ''
                    or image_id is None or image_id == ''):
                return jsonify({'error': "Fields are empty!"})

            else:
                path = os.path.join(
                    root, 'templates/images/diseases/')
                db_image_name = ad.get_disease_image_name(
                    image_id, disease_id)
                pre_image_path = path + db_image_name
                if db_image_name != 'None':
                    if os.path.isdir(pre_image_path):
                        shutil.rmtree(pre_image_path)

                if ad.update_disease_image(image_id, 'None', disease_id) > 0:
                    return jsonify({'success': "Image Remove successfully!"})

                else:
                    return jsonify({'error': "Some error occur!"})

    return redirect(url_for('appAdmin.login'))


# Route for admin diseases add page
@appAdminDiseases.route('/add_diseases')
def add_diseases():

    if 'adminId' in session:
        return render_template('Admin/add_diseases.html')

    else:
        return redirect('login')


# Route for add disease
@appAdminDiseases.route('/add_new_disease', methods=['GET', 'POST'])
def add_new_disease():

    if 'adminId' in session:
        if request.method == "POST":

            txt_plant_name = request.form.get('txt_plant_name')
            txt_disease_name = request.form.get('txt_disease_name')
            txt_disease_detail = request.form.get('txt_disease_detail')
            txt_treatment_detail = request.form.get('txt_treatment_detail')
            thumbnail = request.files.get('thumbnail')
            image1 = request.files.get('image1')
            image2 = request.files.get('image2')
            image3 = request.files.get('image3')
            image4 = request.files.get('image4')

            if (len(txt_plant_name) == 0 or len(txt_disease_name) == 0
                    or len(txt_disease_detail) == 0 or len(txt_treatment_detail) == 0 or thumbnail == None):
                return jsonify({'error': "Fields are empty!"})

            elif ad.check_disease_is_exist(txt_plant_name, txt_disease_name) != 0:
                return jsonify({'error': txt_plant_name + " '" + txt_disease_name + "' This plant and disease already added!"})

            else:

                # Save uploaded images and get file names
                save_folder = os.path.join(
                    root, 'templates/images/diseases/')
                thumbnail_name = utils.file_save(thumbnail, save_folder)
                image1_name = utils.file_save(image1, save_folder)
                image2_name = utils.file_save(image2, save_folder)
                image3_name = utils.file_save(image3, save_folder)
                image4_name = utils.file_save(image4, save_folder)

                disease_id = (txt_plant_name + txt_disease_name +
                              utils.random_number()).replace(" ", "")

                # Insert disease recodes
                if ad.add_new_disease(disease_id, txt_plant_name, txt_disease_name, txt_disease_detail, txt_treatment_detail,
                                      thumbnail_name, image1_name, image2_name, image3_name, image4_name) < 1:
                    return jsonify({'error': "Disease not added!"})

                else:
                    return jsonify({'success': "Disease added successfully!"})

    return redirect(url_for('appAdmin.admin'))


# Route for update disease details
@appAdminDiseases.route('/update_disease_details')
def update_disease_details():

    if 'adminId' in session:
        id = request.args.get('id', default='no-id')
        details = ad.disease_details(id)

        if len(details) == 0:
            return redirect(url_for('appAdminDiseases.view_diseases'))
        else:
            return render_template('Admin/update_disease_details.html', details=details[0])

    else:
        return redirect('login')


# Route for update disease details
@appAdminDiseases.route('/update_disease', methods=['GET', 'POST'])
def update_disease():

    if 'adminId' in session:
        if request.method == "POST":

            txt_id = request.form.get('txt_id')
            txt_plant_name = request.form.get('txt_plant_name')
            txt_disease_name = request.form.get('txt_disease_name')
            txt_disease_detail = request.form.get('txt_disease_detail')
            txt_treatment_detail = request.form.get('txt_treatment_detail')

            if (len(txt_id) == 0 or len(txt_plant_name) == 0 or len(txt_disease_name) == 0
                    or len(txt_disease_detail) == 0 or len(txt_treatment_detail) == 0):
                return jsonify({'error': "Fields are empty!"})

            else:
                if ad.update_disease_details(txt_id, txt_plant_name, txt_disease_name, txt_disease_detail, txt_treatment_detail) < 1:
                    return jsonify({'error': "Disease details not updated!"})

                else:
                    return jsonify({'success': "Disease details update successfully!"})

    return redirect(url_for('appAdmin.admin'))


# Route for delete diseases
@appAdminDiseases.route('/delete_desease', methods=['GET', 'POST'])
def delete_desease():
    if 'adminId' in session:
        id = request.args.get('id', default='no-id')
        details = ad.disease_details(id)

        if ad.delete_disease_details(id) > 0:

            if len(details) != 0:
                image_folder = os.path.join(
                    root, 'templates/images/diseases/')
                for item in details[0][5:]:
                    if item != 'None':
                        image_path = image_folder + item
                        if os.path.exists(image_path):
                            os.remove(image_path)

        return redirect(url_for('appAdminDiseases.view_diseases'))

    else:
        return redirect('login')
