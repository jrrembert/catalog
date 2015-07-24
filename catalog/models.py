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

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


from config import DATABASE_URI


from catalog import db



Base = declarative_base()




class Users(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(75), nullable=False)
    picture = Column(String(250))

    def __init__(self, name=None, email=None, picture=None):
        self.name = name
        self.email = email
        self.picture = picture

    def __repr__(self):
        return "<Users(name={0}, email={1})>".format(self.name, self.email)


class Sports(db.Model):
    __tablename__ = 'sports'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user = relationship(Users)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, user_id=None, name=None):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return "<Sports(name={0})>".format(self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id
        }

    
class Teams(db.Model):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    wins = Column(Integer)
    losses = Column(Integer)
    league = Column(String(40))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)
    sport_id = Column(Integer, ForeignKey('sports.id'))
    sport = relationship(Sports)

    def __init__(self, user_id=None, name=None, wins=None, 
                 losses=None, league=None, sport=None):
        self.user_id = user_id
        self.name = name
        self.wins = wins
        self.losses = losses
        self.league = league
        self.sport = sport

    def __repr__(self):
        return "<Teams(name={0})>".format(self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'wins': self.wins,
            'losses': self.losses,
            'league': self.league,
            'user_id': self.user_id,
            'sport': self.sport_id
        }


# # class Leagues(Base):
# #     __tablename__ = 'leagues'

# #     id = Column(Integer, primary_key=True)
# #     name = Column(String(100), nullable=False)
# #     user = relationship(Users)
# #     user_id = Column(Integer, ForeignKey('users.id'))


# # class Players(Base:)
# #     __tablename__ = 'players'

# #     id = Column(Integer, primary_key=True)
# #     name = Column(String(100), nullable=False)
# #     user = relationship(Users)
# #     user_id = Column(Integer, ForeignKey('users.id')) 


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
#engine = create_engine(DATABASE_URI)
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
#Base.metadata.create_all(engine)
db.create_all()