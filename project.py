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


##### JSON API endpoints #####





##### Sport page routes #####

@app.route('/')
@app.route('/sports')
def show_sports():
    sports = session.query(Sports).order_by(asc(Sports.name)).all()
    
    return render_template('sports.html', sports=sports)


@app.route('/sports/new')
def new_sport():
    pass


@app.route('/sports/<int:sports_id>/edit')
def edit_sport(sport_id):
    pass


@app.route('/sports/<int:sports_id>/delete')
def delete_sport(sport_id):
    pass


##### Team page routes #####


@app.route('/teams')
def show_all_teams():
    sports = session.query(Sports).order_by(asc(Sports.name))
    teams = session.query(Teams).order_by(asc(Teams.sport_id))
    return render_template('teams.html', sports=sports, teams=teams)


@app.route('/sports/<int:sport_id>/teams')
def show_sports_teams(sport_id):
    sports = session.query(Sports).filter_by(id=sport_id).one()
    teams = session.query(Teams).filter_by(sport_id=sport_id).all()
    return render_template('sportteams.html', sports=sports, teams=teams)


@app.route('/teams/<int:sport_id>/new')
def new_team(sport_id):
    pass



@app.route('/sports/<int:sport_id>/teams/<int:team_id>/edit')
def new_team(sport_id, team_id):
    pass



@app.route('/teams/<int:sport_id>/teams/<int:team_id>/delete')
def new_team(sport_id, team_id):
    pass





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)