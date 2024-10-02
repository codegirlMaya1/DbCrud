import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:568312@localhost/gymdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    app = Flask(__name__)
    app.config.from_object('config.Config')
    db = SQLAlchemy(app)
    ma = Marshmallow(app)