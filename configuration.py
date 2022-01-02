from src_api import app
import os


class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """

    # Default settings
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    APP_FOLDER = os.path.abspath(os.path.join(app.root_path, os.pardir))
    UPLOAD_FOLDER = os.path.join(APP_FOLDER, "static", "client", "wav")
    app.logger.debug(f"=== APP FOLDER: {APP_FOLDER}")
    app.logger.debug(f"=== UPLOAD FOLDER: {UPLOAD_FOLDER}")

    ALLOWED_EXTENSIONS = set(["wav"])

    SECRET_KEY = os.getenv("SECRET_KEY", default="p9?nR-$wv=7$ruz7*v$peçG=ozcA7e£S22o-Pic46_tMb?o4+z8YtruweB=033706")
    SESSION_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    """
    Development configuration class. Contains Base configuration settings + configuration settings applicable to Development.
    """

    DEBUG = True


class TestingConfig(Config):
    """
    Testing configuration class. Contains Base configuration settings + configuration settings applicable to Testing.
    """

    TESTING = True


class ProductionConfig(Config):
    """
    Production configuration class. Contains Base configuration settings + configuration settings applicable to Production.
    """

    FLASK_ENV = "production"
