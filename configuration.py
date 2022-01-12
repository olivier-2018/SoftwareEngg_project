import os
import secrets


class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """

    # Default settings
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    ALLOWED_EXTENSIONS = set(["wav"])
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", default=secrets.token_urlsafe(128))
    SESSION_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    """
    Development configuration class. Contains Base configuration settings + configuration settings applicable to Development.
    """

    # current_app.logger.info("Logger in init /ENV dev")
    DEBUG = True


class TestingConfig(Config):
    """
    Testing configuration class. Contains Base configuration settings + configuration settings applicable to Testing.
    """

    # current_app.logger.info("Logger in init /ENV test")
    TESTING = True


class ProductionConfig(Config):
    """
    Production configuration class. Contains Base configuration settings + configuration settings applicable to Production.
    """

    # current_app.logger.info("Logger in init /ENV prod")
    FLASK_ENV = "production"
