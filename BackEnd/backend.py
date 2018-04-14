#! flask/bin/python
# -*- coding: utf-8 -*-
import json 
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt

from flask_cors import CORS
from scipy.cluster.vq import kmeans
from flask import Flask, request, jsonify, send_from_directory

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
CORS(app)

class Image:
    datafile = []

    def __init__(self,json_data,imageid):
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

        self.points = np.array(self.points,dtype=float)
                

    def clusterData(self,classes):
        """Get the cluster mean points"""
        means = kmeans(self.points,classes)
        return means
    

    def extract(self,means,window_size):
        """Extract small patches around"""
        
        extracted_patches = []
        for mean in means:
            x = np.asarray(mean[0] - (window_size-1)/2,dtype=int)
            y = np.asarray(mean[1] - (window_size-1)/2,dtype=int)
            extract = np.empty([window_size,window_size,3], dtype=int)
            extract = self.datafile[x:x+window_size,y:y+window_size,:]
            print(extract.shape)
            extracted_patches.append(extract) 
            cv2.imshow('Patch',extract)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return extracted_patches



    def assemble(self, patches):
        """Assemble Feature Collage"""
        mozaiques = []
        for i in range(5):
            # patches = np.random.shuffle(patches)
            nb_patches_per_rows = int(math.sqrt(len(patches)))
            nb_patches_per_cols = len(patches) / nb_patches_per_rows
            mozaique = np.zeros([patches[0].shape[0] * nb_patches_per_rows, patches[0].shape[1] * nb_patches_per_cols, 3], dtype=int)
            m = n = 0

            for patch in patches:
                # mozaique[n:patch.shape[0],m:patch.shape[1],:] = patch
                l = 0
                for j in range(n, patch.shape[0]):
                    p = 0
                    for k in range(m, patch.shape[1]):
                        # print("j={} k={} l={} p={}".format(j,k,l,p))
                        mozaique[j, k, :] = patch[l, p, :]
                        # print(mozaique)
                        p += 1
                    l += 1

                m += 1
                if m == nb_patches_per_cols:
                    m = 0
                    n += 1

            print(mozaique)
            print(mozaique.shape)
            cv2.imshow('Mozaique', mozaique)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            plt.imshow(mozaique)
            plt.show()
            mozaiques.append(mozaique)
        
        return mozaiques


    def dream(self):
        """Dream"""
        return 1


@app.route('/api/<imageid>', methods=['POST'])
def postData(imageid):
    content = request.get_json()
    
    x = Image(content,imageid)
    x.datafile = cv2.imread("images/johnny850x850.jpg")
    #cv2.imshow('Patch',x.datafile)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    means = x.clusterData(3)

    patches = x.extract([[400,400], [256, 199], [534, 312]], 100)
    x.assemble(patches)
            
    
    print("Data Received!")
    return("Done!")


@app.route('/api/mozaique', methods=['GET'])
def getData():
    return("Not ready")
        

@app.route('/images/<path:path>')
def send_img(path):
    return send_from_directory('images', path)


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
