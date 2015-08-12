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
import datetime
import httplib2
import logging
import json
import random
import requests
import string

import ipdb




from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask import flash, make_response
from flask import session as login_session
from sqlalchemy import asc

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from oauth2client.client import AccessTokenCredentials

from models import Sports, Teams, Users
from catalog_project import app, db


session = db.session

##### Utility Functions #####

def create_user(login_session):
    new_user = Users(name=login_session['username'], 
                     email=login_session['email'], 
                     picture=login_session['picture'],
                     created_date=datetime.datetime.now())
    session.add(new_user)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user


def get_user_info(user_id):
    user = session.query(Users).filter_by(id=user_id).one()
    return user

def get_user_id(email):
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.teardown_appcontext
def shutdown_session(exception=None):
    """ Automatically remove database sessions at end of request
        or when application shuts down.
    """
    session.remove()

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




















##### Authentication #####

# Create CSRF anti-forgery state token
@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + 
                                  string.ascii_lowercase + 
                                  string.digits) for x in xrange(32))
    login_session['state'] = state
    print("Current session state is %s" % login_session['state'])
    return render_template('access/login.html',
                           STATE=state,
                           CLIENT_ID=app.config['OAUTH_CREDENTIALS']['google']['client_id'])


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """ Exchange one-time authorization code for a token and store the
        token in the session.
    """

    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Comment out to allow user to connect and disconnect without reloading
    # page.
    # del login_session['state']

    
    code = request.data
    
    try:
        # Update authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            app.config['CLIENT_SECRET_PATH'],
            scope='')
        oauth_flow.redirect_uri = 'postmessage'
        authorize_url = oauth_flow.step1_get_authorize_url()
        credentials = oauth_flow.step2_exchange(code)
        
        # login_session['credentials'] = credentials.access_token
        # credentials = AccessTokenCredentials(login_session['credentials'], 'user-agent-value')
    except FlowExchangeError:
        response = make_response(
            json.dumps("Failed to upgrade the authorization code."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != app.config['OAUTH_CREDENTIALS']['google']['client_id']:
        response = make_response(
            json.dumps("Token's client ID does not match app's"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = response = make_response(
            json.dumps("Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    


    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()


    

    
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # See if user exists. If not, create one
    user_id = get_user_id(data['email'])
    if not user_id:
        create_user(login_session)
    
    login_session['user_id'] = user_id
    

    login_success = "<h1>Welcome {0}!</h1><img src='{1}' ".format(login_session['username'], login_session['picture'])
    login_success += "style='width: 300px; height: 300px; border-radius: 150px; -webkit-border-radius: 150px; -moz-border-radius: 150px;'>"
    flash("You are now logged in as {0}".format(login_session['username']))

    return login_success


@app.route('/gdisconnect')
def gdisconnect():
    """ Revoke access token for Google Sign-in. """
    # We're not storing the entire credentials object in our login_session
    credentials = login_session.get('access_token')
    if credentials is None:
        response = make_response(
            json.dumps('Current user is not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = app.config['OAUTH_CREDENTIALS']['google']['revoke_url'] + "{0}".format(credentials)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps("Failed to revoke token for given user.", 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    """ General disconnect route for all providers. """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            # Remove session info for user
            for key in login_session.keys():
                del login_session[key]
            flash("You have been successfully logged out.", "info")
            return redirect(url_for('show_sports'))
    else:
        flash("You weren't logged in.")
        return redirect(url_for('show_sports'))





##### Sport page routes #####

@app.route('/')
@app.route('/sports')
def show_sports():
    sports = session.query(Sports).order_by(asc(Sports.name)).all()
    teams = session.query(Teams).all()

    # Aggregate all items and sort by created date (descending order)
    latest_items = sorted(sports + teams, 
                          key=lambda item: item.created_date,
                          reverse=True)
    return render_template('sports/sports.html', 
                           sports=sports,
                           latest_items=latest_items)


@app.route('/sports/new', methods=['GET', 'POST'])
def new_sport():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        new_sport = Sports(name=request.form['name'], created_date=datetime.datetime.now())
        session.add(new_sport)
        flash("New sport added: {0}".format(new_sport.name))
        session.commit()
        return redirect(url_for('show_sports'))
    else:
        return render_template('sports/sportsnew.html')


@app.route('/sports/<int:sport_id>/edit', methods=['GET', 'POST'])
def edit_sport(sport_id):
    if 'username' not in login_session:
        return redirect('/login')
    edited_sport = session.query(Sports).filter_by(id=sport_id).one()
    if edited_sport.user_id != login_session['user_id']:
        flash('You are not authorized to edit this sport', 'error')
        return redirect(url_for('show_sports'))
    if request.method == 'POST':
        if request.form['name']:
            edited_sport.name = request.form['name']
            session.add(edited_sport)
            session.commit()
            flash("Sport successfully edited: {0}".format(edited_sport.name))
            return redirect(url_for('show_sports'))
    else:
        return render_template('/sports/editsports.html', sport=edited_sport)


@app.route('/sports/<int:sport_id>/delete', methods=['GET', 'POST'])
def delete_sport(sport_id):
    if 'username' not in login_session:
        return redirect('/login')
    deleted_sport = session.query(Sports).filter_by(id=sport_id).one()
    if deleted_sport.user_id != login_session['user_id']:
        flash('You are not authorized to delete this sport', 'error')
        return redirect(url_for('show_sports'))
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
    sports = session.query(Sports).order_by(asc(Sports.name)).all()
    teams = session.query(Teams).order_by(asc(Teams.sport_id))
    return render_template('teams/teams.html', sports=sports, teams=teams)


@app.route('/sports/<int:sport_id>/teams')
def show_sports_teams(sport_id):
    """Show all teams within a given sport."""
    sports = session.query(Sports).order_by(asc(Sports.name)).all()
    teams = session.query(Teams).filter_by(sport_id=sport_id).all()
    team_sport = session.query(Sports).filter_by(id=sport_id).one()
    return render_template('teams/sportteams.html', sports=sports, 
                           teams=teams, team_sport=team_sport)


@app.route('/sports/<int:sport_id>/teams/<int:team_id>')
def show_team(sport_id, team_id):
    teams = session.query(Teams).filter_by(sport_id=sport_id).all()
    team = session.query(Teams).filter_by(id=team_id).one()
    return render_template('/teams/team.html', teams=teams, team=team)


@app.route('/teams/<int:sport_id>/new', methods=['GET', 'POST'])
def new_team(sport_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        new_team = Teams(name=request.form['name'],
                         league=request.form['league'],
                         wins=request.form['wins'],
                         losses=request.form['losses'], 
                         created_date=datetime.datetime.now(), 
                         sport_id=sport_id)
        session.add(new_team)
        session.commit()
        flash("New team added: {0}".format(new_team.name))
        return redirect(url_for('show_sports_teams', sport_id=sport_id))
    else:
        return render_template('teams/teamsnew.html')


@app.route('/sports/<int:sport_id>/teams/<int:team_id>/edit', methods=['GET', 'POST'])
def edit_team(sport_id, team_id):
    if 'username' not in login_session:
        return redirect('/login')
    resource_root = request.url.split('/')[3]  # Get first element in app.route
    edited_team = session.query(Teams).filter_by(id=team_id).one()
    if edited_team.user_id != login_session['user_id']:
        flash('You are not authorized to edit this team', 'error')
        return redirect(url_for('show_sports_teams', sport_id=sport_id))
    if request.method == 'POST':
        if request.form['name']:
            edited_team.name = request.form['name']
            edited_team.league = request.form['league']
            edited_team.wins = request.form['wins']
            edited_team.losses = request.form['losses']
            session.add(edited_team)
            session.commit()
            flash("Sport successfully edited: {0}".format(edited_team.name))
            # TODO: determine canonical url for team editing and create route
            #       if necessary.
            if resource_root == 'sports':
                return redirect(url_for('show_sports_teams', sport_id=sport_id))
            else:
                return redirect(url_for('show_sports_teams', sport_id=sport_id))
    else:
        return render_template('/teams/editteam.html', team=edited_team)


@app.route('/sports/<int:sport_id>/teams/<int:team_id>/delete', methods=['GET', 'POST'])
def delete_team(sport_id, team_id):
    if 'username' not in login_session:
        return redirect('/login')
    sport = session.query(Sports).filter_by(id=sport_id).one()
    deleted_team = session.query(Teams).filter_by(id=team_id).one()
    if deleted_team.user_id != login_session['user_id']:
        flash('You are not authorized to delete this team', 'error')
        return redirect(url_for('show_sports_teams', sport_id=sport_id))
    if request.method == 'POST':
        session.delete(deleted_team)
        session.commit()
        flash("Sport successfully deleted: {0}".format(deleted_team.name))
        return redirect(url_for('show_sports_teams', sport_id=sport_id))
    else:
        return render_template('/teams/deleteteams.html', team=deleted_team)
