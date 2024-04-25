# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Create an instance of the Flask class.
myapp_obj = Flask(__name__)

# Get the base directory of the application to configure the database
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure Secret Key
# SQLALCHEMY_DATABASE_URI is the path to database.
myapp_obj.config.from_mapping(
    SECRET_KEY='you-will-never-guess',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Create SQLAlchemy object
db = SQLAlchemy(myapp_obj)

# Ensures that the database is accessible when handling a request
# After, database tables are created
with myapp_obj.app_context():
    from app.models import User

    db.create_all()

# Import the routes module from the 'app' package. This has the different urls for application
from app import routes