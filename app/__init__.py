from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

import os
import pymongo

app = Flask("AuthApp")
api = Api(app)

app.config.from_object('config.' + os.environ.get('AUTHAPP_CONFIG_MOD', 'DevLocalConfig'))
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

jwt = JWTManager(app)

print(" * Connecting to MongoDB * " + app.config['DATABASES']['mongo']['dbname'])
db = pymongo.MongoClient(app.config['DATABASES']['mongo']['url'])[app.config['DATABASES']['mongo']['dbname']]

from app.views import *
from app.resources import *
