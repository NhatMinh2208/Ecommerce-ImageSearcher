from flask import Flask,render_template,request,send_file,send_from_directory,jsonify
import cv2
import glob
import os
import sys
import numpy as np
import imsearch

import base64
import requests
from PIL import Image
from io import BytesIO



app = Flask(__name__,static_folder='static',template_folder='templates')

def create_index(name, images):
    # Initialize the index
    index = imsearch.init(name)
    # Clear the index and data if any exists
    index.cleanIndex()
    # Add images in batch (List of image paths locally stored)
    index.addImageBatch(images[0:])
    # Build the index
    index.createIndex()

    return index

"""
def create_index_with_config(name):
    '''
    parameters:
        name: name of the index (unique identifier name)
        MONGO_URI
        REDIS_URI
        DETECTOR_MODE:  select 'local' or 'remote'. 
                        local: detector backend should be running on the same machine
                        remote: Process should not start detector backend
        pass any configuration you want to expose as environment variable. 
    '''
    index = imsearch.init(name=name,
                          MONGO_URI='mongodb://localhost:27017/',
                          REDIS_URI='redis://localhost:6379/0',
                          DETECTOR_MODE='local')
"""
def load_index(name, file_path):
    index = imsearch.init_from_file(file_path=file_path, name=name)
    index.createIndex()
    return index

def load_from_db(name, passwd):
    # Initialize the index
    index = imsearch.init(name, passwd)

    # Clear the index and data if any exists
    index.cleanIndex()
    index.loadFromDB()
    index.createIndex()
    return index
'''
def show_results(similar, qImage):
    qImage = imsearch.utils.check_load_image(qImage)
    qImage = cv2.cvtColor(qImage, cv2.COLOR_RGB2BGR)
    cv2.imshow('qImage', qImage)
    for _i, _s in similar:
        rImage = cv2.imread(_i['image'])
        print([x['name'] for x in _i['primary']])
        print(_s)
        cv2.imshow('rImage', rImage)
        cv2.waitKey(0)
'''
#index = load_index('clothes', 'clothes_index.tar.gz')
print("App started")
index = load_from_db(name='products', passwd='')    

def main_path(img):
    # all_images = glob.glob(os.path.join(
    #     os.path.dirname(__file__), '.', 'images/*/*.jpg'))
    #index = create_index('test', all_images)
    
    #index = load_index('clothes', 'clothes_index.tar.gz')
    
    # query index with image path
    '''
    image_path: path to image or URL
    k: Number of results
    policy: choose policy from 'object' or 'global'. Search results will change accordingly.
    '''
    #similar, _ = index.knnQuery(image_path=all_images[-1], k=10, policy='object')
    #show_results(similar, all_images[-1])

    # query with image URL
    #img_url = 'https://www.wallpaperup.com/uploads/wallpapers/2014/04/14/332423/d5c09641cb3af3a18087937d55125ae3-700.jpg'
    #similar, _ = index.knnQuery(image_path=img_url, k=10, policy='global')
    similar = index.knnQuery_from_img(image=img, k=10, policy='global')
    
    #show_results(similar, img_url)

    # Create index with configuration
    #index = create_index_with_config('test')
    return similar

@app.route('/',methods=['POST','GET'])
def predict():
  if request.method=='POST':
    img=request.files['file'].read()
    response=main_path(img)
    #print(response)
    dicts={}
    i = 0
    for _i, _s in response:
        if _i != None:
            dicts[i] = _i[6]
            print(_i[6])
        i = i + 1
    '''
    print(response)
    dicts={}
    for jj in range(len(response)):
      dicts[jj]=response[jj]
    return jsonify(dicts)
    '''
    return jsonify(dicts)
  if request.method=='GET':
    return render_template('index.html')
  

if __name__=='__main__':
    app.run(debug=False,threaded=False)






