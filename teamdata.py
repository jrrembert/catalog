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
from catalog_project import db
from catalog_project.models import Sports, Teams, Users


session = db.session()

# Create dummy user
user1 = Users(name="J. Ryan Rembert", email="rynliquid@gmail.com",
             picture='https://pbs.twimg.com/profile_images/588416345416404992/y8EvAjvm.jpg')
session.add(user1)

# Create sports
sports = [Sports(user_id=1, name="Baseball"),
          Sports(user_id=2, name="Football"),
          Sports(user_id=1, name="Basketball")]
session.add_all(sports)

# Commit sports so that sqlite will assign them an id
session.commit()  

# Teams for Baseball
baseball_teams = [Teams(user_id=1, name="Atlanta Braves", wins=10,
                        losses=5, league = 'NL', sport_id=sports[0].id),
                  Teams(user_id=1, name="St. Louis Cardinals", wins=10, losses=5, 
                        league = 'NL', sport_id=sports[0].id),
                  Teams(user_id=1, name="Los Angeles Dodgers", wins=10, losses=5, 
                        league = 'NL', sport_id=sports[0].id),
                  Teams(user_id=1, name="Texas Rangers", wins=10, losses=5, 
                        league = 'AL', sport_id=sports[0].id),
                  Teams(user_id=1, name="Tampa Bay Rays", wins=10, losses=5, 
                        league = 'AL', sport_id=sports[0].id)]

session.add_all(baseball_teams)

# Teams for Football
football_teams = [Teams(user_id=1, name="Atlanta Falcons", wins=10, 
                        losses=5, league = 'AFC', sport_id=sports[1].id),
                  Teams(user_id=1, name="New England Patriots", wins=10, losses=5, 
                        league = 'AFC', sport_id=sports[1].id),
                  Teams(user_id=1, name="Indianapolis Colts", wins=10, losses=5, 
                        league = 'AFC', sport_id=sports[1].id),
                  Teams(user_id=1, name="Denver Broncos", wins=10, losses=5, 
                        league = 'NFC', sport_id=sports[1].id),
                  Teams(user_id=1, name="Seattle Seahawks", wins=10, losses=5, 
                         league = 'NFC', sport_id=sports[1].id)]

session.add_all(football_teams)

# Teams for Basketball
basketball_teams = [Teams(user_id=2, name="Atlanta Hawks", wins=10, 
                          losses=5, league = 'Eastern Conference', sport_id=sports[2].id),
                    Teams(user_id=2, name="Indiana Pacers", wins=10, 
                          losses=5, league = 'Eastern Conference', sport_id=sports[2].id),
                    Teams(user_id=2, name="Detroit Pistons", wins=10, 
                          losses=5, league = 'Eastern Conference', sport_id=sports[2].id),
                    Teams(user_id=2, name="Los Angeles Clippers", wins=10, 
                          losses=5, league = 'Western Conference', sport_id=sports[2].id),
                    Teams(user_id=2, name="Denver Nuggets", wins=10, 
                          losses=5, league = 'Western Conference', sport_id=sports[2].id)]

session.add_all(basketball_teams)
session.commit()

num_teams = len(baseball_teams) + len(football_teams) + len(basketball_teams)

print("Added {} sports and {} teams.").format(len(sports), num_teams)
