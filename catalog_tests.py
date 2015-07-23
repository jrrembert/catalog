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
import os
import unittest
import tempfile

from flask import Flask






app = Flask(__file__)
from sqlalchemy import create_engine

from models import Sports, Base, Teams, Users

from config import DATABASE_URI










class CatalogTestCase(unittest.TestCase):

    def setUp(self):
        # sqlite is a filesystem-based db so just create temp file
        self.db_fd, app.config['TEST_DATABASE_URI'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        client =  app.test_client()
        engine = create_engine(self.db_fd)
        Base.metadata.bind = engine
        db_session = sessionmaker(bind=engine)
        session = db_session()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['TEST_DATABASE_URI'])

    def test_empty_db(self):
        root = client.get('/')
        assert 'this thing' in root.data


if __name__ == '__main__':
    unittest.main()