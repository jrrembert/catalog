#!/usr/bin/env python
"""
Author: J. Ryan Rembert
Project: catalog
Source: https://github.com/jrrembert/catalog

Copyright (C) 2015 J. Ryan Rembert. All rights reserved.

Redistribution of source code perfectly cool as long as the
above copyright notice is provided and you don't sue me if
something (somehow) explodes. Unless it explodes into a
rainbow of mutant dinosaurs made out of cookie batter.
Then I assume complete credit.
"""
from flask import Flask, render_template

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Sports, Teams



app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


# Connect to Database and create database session

engine = create_engine(app.config['DATABASE_URI'])
Base.metadata.bind = engine

# Bind Base class metadata to engine to use declaratives in a DBSession()
DBSession = sessionmaker(bind=engine)
session = DBSession()




@app.route('/')
@app.route('/sports')
def show_sports():
    sports = session.query(Sports).order_by(asc(Sports.name))
    return render_template('sports.html', sports=sports)




@app.route('/teams')
def show_teams():
    sports = session.query(Sports).order_by(asc(Sports.name))
    teams = session.query(Teams).order_by(asc(Teams.name))
    return render_template('teams.html', sports=sports, teams=teams)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)