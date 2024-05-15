import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    PRODUCTS_PER_PAGE = 5
    PRODUCT_LISTING_PER_PAGE = 1
    ORDER_LISTING_PER_PAGE = 2
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.jpeg']
    UPLOAD_PATH = 'static/img/product_image'

class DevelopmentConfig(Config):
    DEBUG = True

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
