#! flask/bin/python
# -*- coding: utf-8 -*-
import json 
import numpy as np
import cv2
import math
import shutil
import os

from flask_cors import CORS
from scipy.cluster.vq import kmeans
from flask import Flask, request, jsonify, send_from_directory

# Patches Store
patches = []

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
CORS(app)



##########################################
class Image:
    datafile = []

    def __init__(self, json_data, imageid):
        self.imageid = imageid
        self.screenWidth = json_data["screenWidth"]
        self.screenHeight = json_data["screenHeight"]
        self.imgWidth = json_data["imgWidth"]
        self.imgHeight = json_data["imgHeight"]
        self.imgOffsetX = json_data["imgOffsetX"]
        self.imgOffsetY = json_data["imgOffsetY"]
        self.points = []
        coordinates = json_data["coordinates"]

        for c in coordinates:
            self.points.append(list(c.values()))

        self.points = np.array(self.points, dtype=float)
                

    def clusterData(self, classes):
        """Get the cluster mean points"""
        #self.points = 
        means,ops = kmeans(self.points,classes)
        means = np.asarray(means,dtype=int)

        # Subtract Offset to image coordinate system
        means[:,0] = means[:,0] - self.imgOffsetX 
        means[:,1] = means[:,1] - self.imgOffsetY

        return means.tolist()

    def checkMeans(self, means, window_size):
        """Check if the mean values will produce proper patches"""
        # Remove Outliers
        means2 = []
        for mean in means:
            x = mean[0]
            y = mean[1]
            if not ((x < 0 or x > self.imgWidth) or (y < 0 or y > self.imgHeight)):
                means2.append(mean)
        means = means2[:]

        # Correct when too near to the border
        for i in range(0,len(means)):
            if  means[i][0]  < window_size / 2:
                means[i][0] =  window_size / 2
            if  means[i][0] > (self.imgWidth - window_size / 2): 
                means[i][0] = self.imgWidth - window_size / 2
    
            if  means[i][1] <  window_size / 2:
                means[i][1] = window_size / 2
            if  means[i][1] > (self.imgHeight - window_size / 2): 
                means[i][1] = self.imgHeight - window_size / 2
        #print(means)
        return means
    

    def extract(self,means,window_size):
        """Extract small patches around"""
        
        extracted_patches = []
        for mean in means:
            x = np.asarray(mean[0] - (window_size - 1) / 2, dtype=int)
            y = np.asarray(mean[1] - (window_size - 1) / 2, dtype=int)
            extract = np.empty([window_size, window_size, 3], dtype=int)
            extract = self.datafile[x:x+window_size, y:y+window_size, :]
            extracted_patches.append(extract)

        return extracted_patches

##########################################

def assemble(patches):
    """Assemble Feature Collage"""
    mosaics = []
    for i in range(5):
        np.random.shuffle(patches)
        nb_patches_per_rows = int(math.sqrt(len(patches)))
        nb_patches_per_cols = int(len(patches) / nb_patches_per_rows)
        mosaic = np.zeros([patches[0].shape[0] * nb_patches_per_rows, patches[0].shape[1] * nb_patches_per_cols, 3], dtype='uint8')
        m = n = 0

        for patch in patches:
            l = 0
            for j in range(n * patch.shape[0], n * patch.shape[0] + patch.shape[0]):
                p = 0
                for k in range(m * patch.shape[1], m * patch.shape[1] + patch.shape[1]):
                    mosaic[j, k, :] = patch[l, p, :]
                    p += 1
                l += 1

            m += 1
            if m == nb_patches_per_cols:
                m = 0
                n += 1

        mosaics.append(mosaic)
    
    return mosaics


def dream(self):
    """Dream"""
    return 1

##########################################

@app.route('/api/<imageid>', methods=['POST'])
def postData(imageid):
    content = request.get_json()

    if len(content['coordinates']) == 0:
        return("ERROR: No coordinates !")
    
    window_size = 200
    number_of_classes = 4

    x = Image(content, imageid)
    x.datafile = cv2.imread("images/image{}.jpg".format(imageid))

    means = x.clusterData(number_of_classes)
    means = x.checkMeans(means, window_size)


    global patches
    #patches = x.extract(means,window_size)  
    patches += x.extract([[400, 400], [256, 199], [534, 312], [135, 345], [608, 400], [702, 540]], window_size)
    
    print("Data Received!")
    return("Done!")


@app.route('/api/mosaic', methods=['GET'])
def getData():
    mosaics = assemble(patches)
    urls =[]

    for i, mosaic in enumerate(mosaics):
        cv2.imwrite("output/mosaic{}.jpg".format(i), mosaic)
        urls.append("output/mosaic{}.jpg".format(i))

    return jsonify(urls)
 

@app.route('/output/<path:path>')
def send_mosaic(path):
    return send_from_directory('output',path)


@app.route('/images/<path:path>')
def send_img(path):
    return send_from_directory('images', path)


@app.route('/api/purge', methods=['POST'])
def purge():
    global patches
    patches = []

    if os.path.isdir('output'):
        shutil.rmtree('output/')

    return("OK")

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
