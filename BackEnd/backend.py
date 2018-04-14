#! flask/bin/python
# -*- coding: utf-8 -*-
import json 
import numpy as np
import cv2
from flask_cors import CORS
from scipy.cluster.vq import kmeans
from flask import Flask, request, jsonify

app = Flask(__name__)
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
        
        for mean in means:
            x = np.asarray(mean[0] - (window_size-1)/2,dtype=int)
            y = np.asarray(mean[1] - (window_size-1)/2,dtype=int)
            n = 0
            m = 0
            extract = np.empty([window_size+1,window_size+1,3])
            print(self.datafile)
            for i in range(x,x+window_size-1):
                for j in range(y,y+window_size-1):
                    extract[n,m,:] = self.datafile[i,j,:]
                    m = m + 1
                n = n +1
            return extract
            

        return 1

    def assemble(self):
        """Assemble Feature Collage"""
        return 1

    def dream(self):
        """Dream"""
        return 1


@app.route('/api/<imageid>', methods=['GET', 'POST'])
def postData(imageid):
    if request.method == 'POST':
        content = request.get_json()
        
        x = Image(content,imageid)
        x.datafile = cv2.imread("resources/image" + str(imageid) + ".png")
        print(x.datafile.shape)
        means = x.clusterData(2)
        x.extract(means[0],49)    
        #print(x.clusterData(2))

                
        
        print("Data Received!")
        return("Done!")
        
        

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
