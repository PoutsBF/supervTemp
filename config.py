# -*- coding: utf-8 -*-
#! python3

import os

SECRET_KEY = "I+z9K>6H'g\\p>R?^W'j44r{S"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SCHEDULER_API_ENABLED = True