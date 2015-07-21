from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Sports, Base, Teams, Users


app = Flask(__name__)

# Load config variables
app.config.from_object('config.DevelopmentConfig')

engine = create_engine(app.config['DATABASE_URI'])
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
user1 = Users(name="J. Ryan Rembert", email="rynliquid@gmail.com",
             picture='https://pbs.twimg.com/profile_images/588416345416404992/y8EvAjvm.jpg')
session.add(user1)

# Teams for Baseball
sport1 = Sports(user_id=1, name="Baseball")
session.add(sport1)

team1 = Teams(user_id=1, name="Atlanta Braves", wins=10, losses=5, 
              league = 'NL', sport=sport1)
session.add(team1)

team2 = Teams(user_id=1, name="St. Louis Cardinals", wins=10, losses=5, 
              league = 'NL', sport=sport1)
session.add(team2)

team3 = Teams(user_id=1, name="Los Angeles Dodgers", wins=10, losses=5, 
              league = 'NL', sport=sport1)
session.add(team3)

team4 = Teams(user_id=1, name="Texas Rangers", wins=10, losses=5, 
              league = 'AL', sport=sport1)
session.add(team4)

team5 = Teams(user_id=1, name="Tampa Bay Rays", wins=10, losses=5, 
              league = 'AL', sport=sport1)
session.add(team5)

# Teams for Baseball
sport2 = Sports(user_id=1, name="Football")
session.add(sport2)

team6 = Teams(user_id=1, name="Atlanta Falcons", wins=10, losses=5, 
              league = 'AFC', sport=sport2)
session.add(team6)

team7 = Teams(user_id=1, name="New England Patriots", wins=10, losses=5, 
              league = 'AFC', sport=sport2)
session.add(team7)

team8 = Teams(user_id=1, name="Indianapolis Colts", wins=10, losses=5, 
              league = 'AFC', sport=sport2)
session.add(team8)

team9 = Teams(user_id=1, name="Denver Broncos", wins=10, losses=5, 
              league = 'NFC', sport=sport2)
session.add(team9)

team10 = Teams(user_id=1, name="Seattle Seahawks", wins=10, losses=5, 
              league = 'NFC', sport=sport2)
session.add(team10)

# Teams for Baseball
sport3 = Sports(user_id=1, name="Basketball")
session.add(sport3)

team11 = Teams(user_id=1, name="Atlanta Hawks", wins=10, losses=5, 
              league = 'Eastern Conference', sport=sport3)
session.add(team11)

team12 = Teams(user_id=1, name="Indiana Pacers", wins=10, losses=5, 
              league = 'Eastern Conference', sport=sport3)
session.add(team12)

team13 = Teams(user_id=1, name="Detroit Pistons", wins=10, losses=5, 
              league = 'Eastern Conference', sport=sport3)
session.add(team13)

team14 = Teams(user_id=1, name="Los Angeles Clippers", wins=10, losses=5, 
              league = 'Western Conference', sport=sport3)
session.add(team14)

team15 = Teams(user_id=1, name="Denver Nuggets", wins=10, losses=5, 
              league = 'Western Conference', sport=sport3)
session.add(team15)
session.commit()

print "added some teams."
