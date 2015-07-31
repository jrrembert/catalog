from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config.from_object('catalog_project.config')
# Uncomment this is you want to use a class/inheritance config model
# app.config.from_object('catalog.config.DevelopmentConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(use_debugger=True,
                                        use_reloader=True,
                                        host='0.0.0.0',
                                        port=5000)
                   )

from catalog_project import views