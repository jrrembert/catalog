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
from flask import Flask, render_template, jsonify

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from app.models import Base, Sports, Teams



app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


# Connect to Database and create database session

engine = create_engine(app.config['DATABASE_URI'])
Base.metadata.bind = engine

# Bind Base class metadata to engine to use declaratives in a DBSession()
DBSession = sessionmaker(bind=engine)
session = DBSession()


##### JSON API endpoints #####

@app.route('/sports/JSON')
def show_sports_json():
    sports = session.query(Sports).all()
    return jsonify(sports=([s.serialize for s in sports]))


@app.route('/teams/JSON')
def show_teams_json():
    teams = session.query(Teams).all()
    return jsonify(teams=([t.serialize for t in teams]))


@app.route('/sports/<int:sport_id>/teams/JSON')
def show_sport_teams_json(sport_id):
    sports = session.query(Sports).filter_by(id=sport_id).one()
    teams = session.query(Teams).filter_by(sport_id=sport_id)
    return jsonify(teams=([t.serialize for t in teams]))


@app.route('/sports/<int:sport_id>/teams/<int:team_id>/JSON')
def show_sport_teams_info_json(sport_id, team_id):
    team = session.query(Teams).filter_by(id=team_id).one()
    return jsonify(team=team.serialize)



##### Sport page routes #####

@app.route('/')
@app.route('/sports')
def show_sports():
    sports = session.query(Sports).order_by(asc(Sports.name)).all()
    
    return render_template('sports/sports.html', sports=sports)


@app.route('/sports/new')
def new_sport():
    pass


@app.route('/sports/<int:sport_id>/edit')
def edit_sport(sport_id):
    pass


@app.route('/sports/<int:sport_id>/delete')
def delete_sport(sport_id):
    pass


##### Team page routes #####


@app.route('/teams')
def show_all_teams():
    teams = session.query(Teams).order_by(asc(Teams.sport_id))
    return render_template('teams/teams.html', teams=teams)


@app.route('/sports/<int:sport_id>/teams')
def show_sports_teams(sport_id):
    sports = session.query(Sports).filter_by(id=sport_id).one()
    teams = session.query(Teams).filter_by(sport_id=sport_id).all()
    return render_template('teams/sportteams.html', sports=sports, teams=teams)


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