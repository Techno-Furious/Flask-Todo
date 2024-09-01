import os

POSTGRES_URL = os.environ.get('POSTGRES_URL')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', POSTGRES_URL)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
