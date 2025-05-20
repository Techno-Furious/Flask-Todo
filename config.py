import os

class Config:
    """Base config for Flask application."""
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    
    # Default SQLite database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///todos.db')
    
    # Use PostgreSQL if configured (mainly for Vercel)
    if os.environ.get('POSTGRES_URL_SQL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_URL_SQL')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configurations."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configurations."""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Get configuration from environment or default to 'default'
def get_config():
    return config[os.environ.get('FLASK_ENV', 'default')]
