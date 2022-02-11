import os
import sys
import shutil
import json
import pickle
from flask import Blueprint, render_template, redirect, jsonify, json, url_for, request, session

appAdminModel = Blueprint("appAdminModel", __name__)
sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

import utils
import dbAdmin as ad

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


# Route for view model details
@appAdminModel.route('/model_details')
def model_details():

    if 'adminId' in session:
        return render_template('Admin/model_details.html', details=utils.read_config_json(root + "/python/config.json"))

    else:
        return redirect('login')


# Route for update model
@appAdminModel.route('/model_update')
def model_update():

    if 'adminId' in session:
        return render_template('Admin/model_update.html')

    else:
        return redirect('login')


# Route for update model
@appAdminModel.route('/model_update_details', methods=['GET', 'POST'])
def model_update_details():

    if 'adminId' in session:
        if request.method == "POST":

            save_model = request.files.get('input_model')
            save_pickle = request.files.get('input_pkl')
            accuracy = request.form.get('txt_accuracy')

            if (len(accuracy) == 0 or save_model == None or save_pickle == None):
                return jsonify({'error': "Fields are empty!"})

            else:

                try:
                    # Save uploaded images and get file names
                    model_save_folder = os.path.join(root, 'python/model/')
                    pickle_save_folder = os.path.join(
                        root, 'python/pickle/')
                    json_save_path = os.path.join(
                        root, 'python/config.json')

                    # Remove existing model folder
                    if os.path.exists(model_save_folder):
                        shutil.rmtree(model_save_folder[:-1])

                    if not os.path.exists(model_save_folder):
                        os.makedirs(model_save_folder)

                    # Remove existing pickle folder
                    if os.path.exists(pickle_save_folder):
                        shutil.rmtree(pickle_save_folder[:-1])

                    if not os.path.exists(pickle_save_folder):
                        os.makedirs(pickle_save_folder)

                    model_name = utils.file_save(save_model, model_save_folder)
                    pickle_name = utils.file_save(
                        save_pickle, pickle_save_folder)

                    pkl_path = os.path.join(pickle_save_folder, pickle_name)
                    init_dic = pickle.load(open(pkl_path, 'rb'))

                    diseases_list = [item for item in init_dic]

                    model_json = {
                        "MODEL_NAME": model_name,
                        "PICKLE_NAME": pickle_name,
                        "MODEL_ACCURACY": accuracy,
                        "DISEASES_COUNT": len(diseases_list),
                        "DISEASES": diseases_list,
                        "ADDED_DATE": utils.date_picker(),
                    }

                    with open(json_save_path, 'w') as config:
                        json.dump(model_json, config, indent=4, sort_keys=True)

                    return jsonify({'success': "New model update successfully!"})

                except Exception as e:
                    return jsonify({'error': "Some error occur! " + str(e)})

    return redirect(url_for('appAdmin.admin'))
