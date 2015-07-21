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
class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///testdb.db'


class DevelopmentConfig(Config):
    SECRET_KEY = "Not so secret key"
    DEBUG = True


class ProductionConfig(Config):
    SECRET_KEY = 'vj2tj2@C#r2c89PP98P3HC32fjio233$r%t9d$23r3fvnti5588!!24'
    DATABASE_URI = ''


class TestingConfig(DevelopmentConfig):
    TESTING = True


