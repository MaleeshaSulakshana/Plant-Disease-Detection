import os
import sys
import random
from datetime import datetime
from flask import Flask, render_template, redirect, jsonify, url_for, request

sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))
sys.path.append(os.path.abspath('adminRoutes/'))

import Predictions
import user
import utils

# Import admin route files
from appAdmin import appAdmin
from appAdminDiseases import appAdminDiseases
from appAdminModel import appAdminModel
from appAdminProfile import appAdminProfile
from appAdminAdministration import appAdminAdministration
from appAdminRecoveryPsw import appAdminRecoveryPsw

app = Flask(__name__)
# Blueprints
app.register_blueprint(appAdmin, url_prefix="")
app.register_blueprint(appAdminDiseases, url_prefix="")
app.register_blueprint(appAdminModel, url_prefix="")
app.register_blueprint(appAdminProfile, url_prefix="")
app.register_blueprint(appAdminAdministration, url_prefix="")
app.register_blueprint(appAdminRecoveryPsw, url_prefix="")

app.secret_key = "PlantDisease"
app.static_folder = "templates/"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# Create the folder structure
def genarate_folder():
    # Get date and time
    date_time = datetime.now()
    date_time = str(date_time.strftime("%d_%m_%Y_%H_%M_%S"))

    # Get random number
    random_no = str(random.randint(100000, 999999))

    # Paths
    folder_name = date_time + "_" + random_no + "/"
    folder_path = os.path.join(APP_ROOT, 'upload_images/')
    input_img = os.path.join(folder_path, folder_name)
    uploaded_img_path = os.path.join(input_img, 'images/')

    # Genarate folders
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    if not os.path.isdir(input_img):
        os.mkdir(input_img)

    if not os.path.isdir(uploaded_img_path):
        os.mkdir(uploaded_img_path)

    return input_img, uploaded_img_path


# Route for index/home page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', details=utils.read_config_json(APP_ROOT + "/python/config.json")['DISEASES'])


# Route for deseases view page
@app.route('/diseases', methods=['GET', 'POST'])
def diseases():
    search = request.args.get('search', None)

    if search is not None:
        return render_template('diseases.html', search=user.search_diseases(search), search_value=search)

    return render_template('diseases.html', plants=user.select_plants(), diseases=user.select_diseases())


# Route for getting predictions
@app.route('/prediction_process', methods=['GET', 'POST'])
def prediction_process():

    uploaded_image = request.files.get('image_upload')

    if uploaded_image == None:
        return jsonify({'error_msg': "Image not Uploaded"})

    else:

        # Save image
        input_img, uploaded_img_path = genarate_folder()

        img_name = uploaded_image.filename
        uploaded_image.save(
            uploaded_img_path + img_name)

        try:
            # Getting prediction
            result = Predictions.prediction(input_img)
            result['REDIRECT'] = url_for(
                'diseases', search=result['PREDICTED_DISEASE'][1:].replace("_", " ").lower())

            rowcount = user.prediction_count(
                utils.date_picker(), result['ACCURACY'])

            return jsonify({'result': result})

        except Exception as e:
            return jsonify({'error_msg': "Some error occur!"})


# Route for view diseases details page
@app.route('/disease_details')
def disease_details():

    id = request.args['id']
    details = user.get_disease_details(id)

    if len(details) == 0:
        return redirect('/diseases')

    else:
        return render_template('disease-detail.html', details=details[0])


# Main
if __name__ == '__main__':
    app.run(debug=True)
