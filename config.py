

class Config(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    ENV = 'venv'
    DEVELOPMENT = True
    DEBUG = True
