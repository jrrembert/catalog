from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('catalog_project.config')
# Uncomment this is you want to use a class/inheritance config model
# app.config.from_object('catalog.config.DevelopmentConfig')

db = SQLAlchemy(app)


from catalog_project import views, models