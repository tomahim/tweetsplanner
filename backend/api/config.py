class Config(object):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://tpuser:tppassword@192.168.99.100/tweetsplanner'
    SQLALCHEMY_TRACK_MODIFICATIONS = False