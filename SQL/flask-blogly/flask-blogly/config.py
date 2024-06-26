import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql:///blogly'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = os.urandom(24)


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL', 'postgresql:///blogly_test')
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False