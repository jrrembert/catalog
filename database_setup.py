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
from flask import Flask
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)

# Load config variables
app.config.from_object('config.DevelopmentConfig')
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(75), nullable=False)
    picture = Column(String(250))


class Teams(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    wins = Column(Integer)
    losses = Column(Integer)
    league = Column(String(40))
    user = relationship(Users)
    user_id = Column(Integer, ForeignKey('users.id'))
    sport = relationship(Sports)


class Sports(Base):
    __tablename__ = 'sports'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user = relationship(Users)
    user_id = Column(Integer, ForeignKey('users.id'))


# class Leagues(Base):
#     __tablename__ = 'leagues'
    
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), nullable=False)
#     user = relationship(Users)
#     user_id = Column(Integer, ForeignKey('users.id'))


# class Players(Base:)
#     __tablename__ = 'players'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), nullable=False)
#     user = relationship(Users)
#     user_id = Column(Integer, ForeignKey('users.id')) 


# Prepare a database by createing an Engine object
engine = create_engine(app.config['DATABASE_URI'])

# Create our tables
Base.metadata.create_all(engine)