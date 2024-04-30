import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'never-guess'
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

class TestingConfig(Config):
    TESTING = True
    
class ProductionConfig(Config):
    pass

# Map environment names to configuration classes
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

# Default configuration
default_config = DevelopmentConfig

def get_config(env_name):
    # Returns the configuration class for the given environment name.
    # If the environment name is not recognized, returns the default configuration.
    return config_by_name.get(env_name, default_config)