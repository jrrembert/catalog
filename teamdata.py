from flask import Flask

from catalog_project.models import Sports, Teams, Users

from catalog_project import db

# Load config variables


# engine = create_engine(DATABASE_URI)
# # Bind the engine to the metadata of the Base class so that the
# # declaratives can be accessed through a DBSession instance
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# # A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = db.session()


# Create dummy user
user1 = Users(name="J. Ryan Rembert", email="rynliquid@gmail.com",
             picture='https://pbs.twimg.com/profile_images/588416345416404992/y8EvAjvm.jpg')
session.add(user1)

# Teams for Baseball
sports = [Sports(user_id=1, name="Baseball"),
          Sports(user_id=1, name="Football"),
          Sports(user_id=1, name="Basketball")]
session.add_all(sports)


baseball_teams = [Teams(user_id=1, name="Atlanta Braves", wins=10,
                        losses=5, league = 'NL', sport=sports[0]),
                  Teams(user_id=1, name="St. Louis Cardinals", wins=10, losses=5, 
                        league = 'NL', sport=sports[0]),
                  Teams(user_id=1, name="Los Angeles Dodgers", wins=10, losses=5, 
                        league = 'NL', sport=sports[0]),
                  Teams(user_id=1, name="Texas Rangers", wins=10, losses=5, 
                        league = 'AL', sport=sports[0]),
                  Teams(user_id=1, name="Tampa Bay Rays", wins=10, losses=5, 
                        league = 'AL', sport=sports[0])]

session.add_all(baseball_teams)

# Teams for Football


football_teams = [Teams(user_id=1, name="Atlanta Falcons", wins=10, 
                        losses=5, league = 'AFC', sport=sports[1]),
                  Teams(user_id=1, name="New England Patriots", wins=10, losses=5, 
                        league = 'AFC', sport=sports[1]),
                  Teams(user_id=1, name="Indianapolis Colts", wins=10, losses=5, 
                        league = 'AFC', sport=sports[1]),
                  Teams(user_id=1, name="Denver Broncos", wins=10, losses=5, 
                        league = 'NFC', sport=sports[1]),
                  Teams(user_id=1, name="Seattle Seahawks", wins=10, losses=5, 
                         league = 'NFC', sport=sports[1])]

session.add_all(football_teams)

# Teams for Baseball

basketball_teams = [Teams(user_id=1, name="Atlanta Hawks", wins=10, 
                          losses=5, league = 'Eastern Conference', sport=sports[2]),
                    Teams(user_id=1, name="Indiana Pacers", wins=10, 
                          losses=5, league = 'Eastern Conference', sport=sports[2]),
                    Teams(user_id=1, name="Detroit Pistons", wins=10, 
                          losses=5, league = 'Eastern Conference', sport=sports[2]),
                    Teams(user_id=1, name="Los Angeles Clippers", wins=10, 
                          losses=5, league = 'Western Conference', sport=sports[2]),
                    Teams(user_id=1, name="Denver Nuggets", wins=10, 
                          losses=5, league = 'Western Conference', sport=sports[2])]

session.add_all(basketball_teams)
session.commit()

print "added some teams."
