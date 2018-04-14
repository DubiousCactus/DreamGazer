#! flask/bin/python
# -*- coding: utf-8 -*-
import json 
import numpy as np

from flask_cors import CORS
from scipy.cluster.vq import kmeans
from flask import Flask, request, jsonify, send_from_directory

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
CORS(app)

class Image:

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
        """Cluster Gaze Points"""
        means = kmeans(self.points,classes)
        return means
    
    def extract(self):
        """Extract Small Image Feature"""
        return 1

    def assemble(self):
        """Assemble Feature Collage"""
        return 1

    def dream(self):
        """Dream"""
        return 1


@app.route('/api/<imageid>', methods=['POST'])
def postData(imageid):
    content = request.get_json()
    
    x = Image(content,imageid)
    print(x.clusterData(2))
            
    
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
