import os
import sqlite3
class Config(object):
    SECRET_KEY ='lACLAVE'
class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='sqlite:///db/app.db '
    SQLALCHEMY_TRACK_MODIFICATIONS=False