import cv2
import face_recognition
import glob
import os
import logging
import time
import re
import json
import flask 
import datetime
import requests
import base64
import numpy as np
import face_recognition
from flask import Flask, send_file
from flask import request
from flask import jsonify
#from waitress import serve
from flask_cors import CORS
from PIL import Image, ImageDraw
#from ocrr import tesseract
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from keras.preprocessing import image
app = Flask(__name__)
CORS(app)

#res = load_model('sign_classifier_1.h5')
IMG_SHAPE = 150


@app.route('/sign_validation',methods = ['POST','GET'])
def sign_classifier():
    res = load_model('sign_classifier_1.h5')
    #print("verifyPhoto.face_detection: {}".format("Entered service method"),flush=True)
    #print("Hello")
    result="No faces detected"
    output="sucess"
    if request.method == 'POST':
        try:
         #result="No faces detected"
             #output="invalid"
             error_status="Sucess"
             #print("Hellooooo face_validation")
             result="No faces detected"
             #file = request.files['file']
             req_json=request.json
             #print("face_detection.req_json: {}".format(req_json),flush=True)
             #print(type(req_json))
             if 'img1' in request.json:   #{"compare":"sucess"}
                req_json=request.json
                #print("inside validate..")
                #print("face_detection.req_json: {}".format(req_json),flush=True)
                #print(type(req_json))
                #print(req_json['img1'])
                img_name=req_json['filename']
                s=req_json['img1']
                #print("#########################################################")
                #print(s)
                x = s.split(",")
                #print(len(x))
                #print(x[1])
                encod_img1=x[1].encode()
                #encod_img1=req_json['img1'][18:].encode()
                #print(req_json['img1'][18:])  #iV
                image1_decode = base64.decodestring(encod_img1)
                with open('sign_validation.jpg', 'wb') as image1_result:
                    image1_result.write(image1_decode)
                test_image = image.load_img('sign_validation.jpg', target_size = (IMG_SHAPE, IMG_SHAPE))
                test_image = image.img_to_array(test_image)
                test_image = np.expand_dims(test_image, axis = 0)
                #print("murugannnnnnnnnnnnn")
                result = res.predict(test_image)
                #training_set.class_indices
                print(result)
                print()
                if result[0][0] == 1:
                    prediction = 'invalid_signture'
                    print(prediction)
                    output="invalid_signture"
                else:
                    prediction = 'valid_signature'
                    print(prediction)
                    output="valid_signature"
                
                '''unknown_image = face_recognition.load_image_file('photo_validation.jpg')
                face_locations = face_recognition.face_locations(unknown_image) #face_locations = face_recognition.face_locations(image, model="cnn")
                print("There are ",len(face_locations),"people in this image")
                #result="single faces detected"
                img = cv2.imread('photo_validation.jpg', cv2.IMREAD_GRAYSCALE)   # my_photo, incorrect_3
                n_white_pix = np.sum(img == 255)
                print("Gray image shape is :",img.shape)
                print("Total pixels is (gray image ) :",img.size)
                print('Number of white pixels:', n_white_pix)

                if n_white_pix >50000:
                    print("Photo is not valid..")
                    result="Scaned faces detected"
                    output="invalid"
                    error_code=0
                else:
                    print("Valid photo..")
                    if len(face_locations)==0:
                        print("No Faces Detected..")
                        result="No faces detected"
                        output="invalid"
                        error_code=0
                    elif len(face_locations)>1:
                        print("More than One Face detected....")
                        result="More faces detected"
                        output="invalid"
                        error_code=2
                    elif len(face_locations)==1:
                        print("Single Face detected....")
                        result="single faces detected"
                        output="valid"
                        error_code=1'''
        except Exception as e:
            print(e)
            output="invalid"
            '''error_status=e
            result="Error Occured..."
            output="invalid"
            print("Error occured ....")
            error_code=0'''
            
    os.remove('sign_validation.jpg')        
    #return jsonify({'output' : output,'result':result,'error_code':error_code,'error_status':error_status})
    return jsonify({'output' : output,'result':prediction})

   

if __name__ == '__main__':
    #context = ('/etc/ssl/certs/my.crt', '/etc/ssl/private/my.key')#certificate and key files
    #app.run(host='0.0.0.0',port=8443 ,debug=True,ssl_context=context,threaded=True)
    #serve(app, host='0.0.0.0', port=5030)
    app.run(host='0.0.0.0',port=5030 ,debug=True,threaded=True)
