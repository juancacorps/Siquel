from flask import Flask
from flask_mysqldb import MySQL

def config():
    app = Flask(__name__)
    SECRET_KEY = 'super_secreto'
    app.config['SECRET_KEY'] = SECRET_KEY
    return app

