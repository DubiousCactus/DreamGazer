#! flask/bin/python
# -*- coding: utf-8 -*-
import json 
import numpy as np
import cv2
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
        #self.points = 
        #means,ops = kmeans(self.points,classes)
        means = np.asarray([[0,0],[1400,200],[0,0],[0,0],[0,0]],dtype=int)
        # Subtract Offset to image coordinate system
        means[:,0] = means[:,0] - self.imgOffsetX 
        means[:,1] = means[:,1] - self.imgOffsetY

        return means.tolist()

    def checkMeans(self,means,window_size):
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
            if  means[i][0]  < window_size/2:
                means[i][0] =  window_size/2
            if  means[i][0] > (self.imgWidth - window_size/2): 
                means[i][0] = self.imgWidth - window_size/2
    
            if  means[i][1] <  window_size/2:
                means[i][1] = window_size/2
            if  means[i][1] > (self.imgHeight - window_size/2): 
                means[i][1] = self.imgHeight - window_size/2
        #print(means)
        return means
    

    def extract(self,means,window_size):
        """Extract small patches around"""
        
        extracted_patches = []
        for mean in means:
            # Subtract offset 
           x = np.asarray(mean[0] - (window_size-1)/2 , dtype=int) 
            y = np.asarray(mean[1] - (window_size-1)/2,dtype=int)
            # Extract Image Patches
            extract = np.empty([window_size,window_size,3], dtype=int)
            extract = self.datafile[x:x+window_size,y:y+window_size,:]
            print(mean)
            # Display Patch
            extracted_patches.append(extract) 
            cv2.imshow('Patch',extract)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return extracted_patches
            

    def assemble(self):
        """Assemble Feature Collage"""
        return 1

    def dream(self):
        """Dream"""
        return 1


@app.route('/api/<imageid>', methods=['POST'])
def postData(imageid):
    content = request.get_json()
    
    window_size = 200
    number_of_classes = 4

    x = Image(content,imageid)
    x.datafile = cv2.imread("images/johnny850x850.jpg")
    #cv2.imshow('Patch',x.datafile)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    means = x.clusterData(number_of_classes)
    means = x.checkMeans(means,window_size)
    x.extract(means,window_size)  
            
    
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
