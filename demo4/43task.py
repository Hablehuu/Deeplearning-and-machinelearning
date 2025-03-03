from flask import Flask, request, Response, render_template, redirect, session, url_for
import json
import hashlib
from functools import wraps
import keras
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import io
#import PIL
app = Flask(__name__)

model = ResNet50(weights='imagenet')


@app.route('/',methods=['GET','POST'])

def ImageClassificationService():
    
    
    if request.method == "POST":

        # Print request.files to inspect its contents
        print(request.files)


        if 'Image' not in request.files:
            return render_template("jinja.html",error="no image was given")
        picture = request.files['Image']
        if picture.filename == '':
            return render_template("jinja.html",error="no image was given")

        precdiction_num = request.values.get("precdiction_num",3)
        if precdiction_num == "":
            precdiction_num = 3

        img_bytes = picture.read()
        img = load_img(io.BytesIO(img_bytes), target_size=(224, 224))
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = model.predict(x)


        print('Predicted:', decode_predictions(preds, top=int(precdiction_num))[0])
        predictions =  decode_predictions(preds, top=int(precdiction_num))[0]

        return render_template("jinja.html",predictions=predictions,error="",show=True)
    #default return when coming to the page for the first time
    return render_template("jinja.html",error="")

@app.route('/satellite',methods=['GET','POST'])

def ImageClassificationServicesatellite():
    
    
    if request.method == "POST":

        
        if 'Image' not in request.files:
            return render_template("satellite.html",error="no image was given")
        picture = request.files['Image']
        if picture.filename == '':
            return render_template("satellite.html",error="no image was given")

        precdiction_num = request.values.get("precdiction_num",3)
        if precdiction_num == "":
            precdiction_num = 3
        img_bytes = picture.read()
        img = load_img(io.BytesIO(img_bytes), target_size=(64, 64))
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        model = tf.keras.models.load_model("demo4model.h5")
        preds = model.predict(x)
        print(preds)
        class_labels = ['AnnualCrop', 'Forest', 'HerbaceousVegetation', 'Highway', 'Industrial', 'Pasture', 'PermanentCrop', 'Residential', 'River', 'SeaLake']
        top_indices = np.argsort(preds[0])[-precdiction_num:][::-1]
        print(top_indices)
        #predicted_label = class_labels[predicted_class_index]
        # Printing the predicted class label and its corresponding probability
        for i in top_indices:
            print("Predicted class:", class_labels[i])
            print("Probability:", preds[0][i])
        predictions = [(i, class_labels[i], preds[0][i]) for i in top_indices]
        return render_template("satellite.html",predictions=predictions,error="",show=True)
    #default return when coming to the page for the first time
    return render_template("satellite.html",error="")


