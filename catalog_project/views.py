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







import sys


from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask import flash


from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker


# sys.path.append('~/Projects/catalog/catalog')
# print(sys.path)

from models import Sports, Teams



from config import SQLALCHEMY_DATABASE_URI
from catalog_project import app, db



# app = Flask(__name__)



# catalog = Blueprint('catalog', __name__, url_prefix='/')




# # Connect to Database and create database session

# engine = create_engine(DATABASE_URI)
# Base.metadata.bind = engine

# # Creates a configured "Session" class factory
# db_session = sessionmaker(bind=engine)

# # Create a Session class
# session = db_session()

session = db.session


@app.teardown_appcontext
def shutdown_session(exception=None):
    """ Automatically remove database sessions at end of request
        or when application shuts down.
    """
    db_session.remove()




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


@app.route('/sports/new', methods=['GET', 'POST'])
def new_sport():
    if request.method == 'POST':
        new_sport = Sports(name=request.form['name'])
        session.add(new_sport)
        flash("New sport added: {0}".format(new_sport.name))
        session.commit()
        return redirect(url_for('show_sports'))
    else:
        return render_template('sports/sportsnew.html')


@app.route('/sports/<int:sport_id>/edit', methods=['GET', 'POST'])
def edit_sport(sport_id):
    edited_sport = session.query(Sports).filter_by(id=sport_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_sport.name = request.form['name']
            flash("Sport successfully edited: {0}".format(edited_sport.name))
            return redirect(url_for('show_sports'))
    else:
        return render_template('/sports/editsports.html', sport=edited_sport)


@app.route('/sports/<int:sport_id>/delete', methods=['GET', 'POST'])
def delete_sport(sport_id):
    deleted_sport = session.query(Sports).filter_by(id=sport_id).one()
    if request.method == 'POST':
        session.delete(deleted_sport)
        session.commit()
        flash("Sport successfully deleted: {0}".format(deleted_sport.name))
        return redirect(url_for('show_sports'))
    else:
        return render_template('/sports/deletesports.html', sport=deleted_sport)



##### Team page routes #####


@app.route('/teams')
def show_all_teams():
    sports = session.query(Sports).all()
    teams = session.query(Teams).order_by(asc(Teams.sport_id))
    return render_template('teams/teams.html', teams=teams)


@app.route('/sports/<int:sport_id>/teams')
def show_sports_teams(sport_id):
    """Show all teams within a given sport."""
    sports = session.query(Sports).filter_by(id=sport_id).one()
    teams = session.query(Teams).filter_by(sport_id=sport_id).all()
    return render_template('teams/sportteams.html', sports=sports, teams=teams)


@app.route('/sports/<int:sport_id>/teams/<int:team_id>')
def show_team(sport_id, team_id):
    team = session.query(Teams).filter_by(id=team_id).one()
    return render_template('/teams/team.html', team=team)


@app.route('/teams/<int:sport_id>/new')
def new_team(sport_id):
    pass



@app.route('/sports/<int:sport_id>/teams/<int:team_id>/edit', methods=['GET', 'POST'], endpoint='edit_sport_teams')
@app.route('/teams/<int:team_id>/edit', methods=['GET', 'POST'], endpoint='edit_all_teams')
def edit_team(sport_id, team_id):
    
    resource_root = request.url.split('/')[3]  # Get first element in app.route
    print(resource_root)
    edited_team = session.query(Teams).filter_by(id=team_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_team.name = request.form['name']
            flash("Sport successfully edited: {0}".format(edited_team.name))
            if resource_root == 'sports':
                return redirect(url_for('show_sports_teams', sport_id=sport_id))
            else:
                return redirect(url_for('show_all_teams'))
    else:
        return render_template('/teams/editteam.html', team=edited_team)



@app.route('/sports/<int:sport_id>/teams/<int:team_id>/delete', methods=['GET', 'POST'])
def delete_team(sport_id, team_id):
    sport = session.query(Sports).filter_by(id=sport_id).one()
    deleted_team = session.query(Teams).filter_by(id=team_id).one()
    if request.method == 'POST':
        session.delete(deleted_team)
        #session.commit()
        flash("Sport successfully deleted: {0}".format(deleted_team.name))
        return redirect(url_for('show_sports_teams', sport_id=sport_id))
    else:
        return render_template('/teams/deleteteams.html', team=deleted_team)





# if __name__ == '__main__':

#     app.run(host='0.0.0.0', port=5000, debug=True)