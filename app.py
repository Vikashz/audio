from flask import Flask,render_template,request,jsonify
import os
from flask_pymongo import PyMongo
from pymongo import MongoClient
songs_api = Flask(__name__)
songs_api.config['MONGO_DBNAME'] = 'filed_task'
songs_api.config['Mongo_URI'] = 'mongodb://127.0.0.1:27017/filed_task'
mongo = MongoClient(songs_api.config['Mongo_URI'])
mongo = mongo[songs_api.config['MONGO_DBNAME']]

from applicantion import views

if __name__ == '__main__':
    songs_api.run(debug=True)
