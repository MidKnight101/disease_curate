from flask import Flask, render_template, url_for, request, redirect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. Successfully connected!")
except Exception as e:
    print(e)    

curate = Flask(__name__)

@curate.route('/')
def index():
    return render_template("base.html")


if __name__ == "__main__":
    curate.run(debug=True)