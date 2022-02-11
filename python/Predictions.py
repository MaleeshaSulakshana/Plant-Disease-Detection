# Import libraries

from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image

import numpy as np
import os
import pandas as pd
import json
import pickle
import shutil

import utils


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def prediction(img_path):

    config = utils.read_config_json(APP_ROOT + "/config.json")

    # Get data from json
    test_data = img_path
    img_width = 224
    img_height = 224
    model_path = os.path.join(APP_ROOT, "model", config['MODEL_NAME'])
    pickle_path = os.path.join(APP_ROOT, "pickle", config['PICKLE_NAME'])

    # Load model
    model = keras.models.load_model(model_path)
    print(model.summary())

    # Genarate data for prediction
    predict_datagen = ImageDataGenerator(rescale=1. / 255)
    predict_generator = predict_datagen.flow_from_directory(
        test_data,
        shuffle=False,
        target_size=(img_height, img_width))

    # Get prediction
    predictions = model.predict_generator(predict_generator)
    predicted_class_indices = np.argmax(predictions, axis=1)

    # Load init_dict pickle
    init_dic = pickle.load(open(pickle_path, 'rb'))

    print(init_dic)
    swap_dict = dict([(value, key) for key, value in init_dic.items()])

    # Get true name in the predictions
    predClassArray = []
    for class_indices in predicted_class_indices:
        predClassArray.append(swap_dict.get(class_indices))

    # Calculate score of the predictions
    predPercentArray = []
    for predPercentage in predictions:
        predPercentArray.append("{0:0.1f}".format(
            (np.max(predPercentage) / np.sum(predPercentage) * 100)))

    # Create dataframe for prediction results
    prediction = pd.DataFrame({'IMAGE_NAME': predict_generator.filenames,
                               'PREDICTED_CLASS': predClassArray, 'SCORE': predPercentArray})

    predicted_data = {
        "IMAGE_NAME": os.path.basename(str(prediction['IMAGE_NAME'][0])),
        "PREDICTED_PLANT": ((str(prediction['PREDICTED_CLASS'][0]).split('__')[0]).replace("_", " ")).upper(),
        "PREDICTED_DISEASE": ((str(prediction['PREDICTED_CLASS'][0]).split('__')[1]).replace("_", " ")).upper(),
        "ACCURACY": int(float(prediction['SCORE'][0])),
    }

    shutil.rmtree(test_data[:-1])

    return predicted_data
