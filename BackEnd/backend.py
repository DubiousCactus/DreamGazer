#! flask/bin/python
# -*- coding: utf-8 -*-
import json 
from flask import Flask, request, jsonify
app = Flask(__name__)



@app.route('/api/<imageid>', methods=['GET', 'POST'])
def post_data(imageid):
    if request.method == 'POST':
        content = request.get_json()
        with open('received_data.json', 'w') as outfile:
            json.dump(content, outfile)
        print("Data Received!")
        return "Data Received!"


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
