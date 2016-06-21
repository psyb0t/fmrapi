from flask import Flask
from pymongo import MongoClient


app = Flask(__name__)
app.jinja_env.cache = None

client = MongoClient(connect=False)
database = client['fmrest']
