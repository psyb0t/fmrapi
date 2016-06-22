from flask import Flask
from pymongo import MongoClient
from fmrapi import config


app = Flask(__name__)
app.jinja_env.cache = None

client = MongoClient(connect=False)
database = client[config.db_name]
