from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
import logging

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__, template_folder=os.path.join("..", "templates"), static_folder=os.path.join("..", "static"))

    # Setting the app logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s:%(name)s:%(module)s.py:%(funcName)s:line %(lineno)d => %(message)s")
    # logging.Formatter("%(levelname)s:%(name)s:%(threadName)s:%(message)s:%(module)s:%(funcName)s:%(lineno)d")
    log_file = "app.log"

    if os.path.exists(log_file):
        try:
            os.remove(log_file)
            os.unlink(log_file)
        except:
            pass

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    app.logger.info("Starting logging.")

    # Setting applicable environment variables
    app.config["APP_FOLDER"] = os.path.abspath(os.path.join(app.root_path, os.pardir))
    app.config["UPLOAD_FOLDER"] = os.path.join(app.config["APP_FOLDER"], "static", "client", "wav")

    app.logger.info("APP FOLDER: %s", app.config["APP_FOLDER"])
    app.logger.info("UPLOAD FOLDER: %s", app.config["UPLOAD_FOLDER"])

    if app.config["ENV"] == "" or app.config["ENV"] == "development":
        app.config.from_object("configuration.DevelopmentConfig")
        logger.setLevel(logging.DEBUG)
    elif app.config["ENV"] == "production":
        app.config.from_object("configuration.ProductionConfig")
        logger.setLevel(logging.WARNING)
    elif app.config["ENV"] == "testing":
        app.config.from_object("configuration.TestingConfig")
        logger.setLevel(logging.INFO)

    app.logger.info("%s environment detected.", app.config["ENV"])

    # Initializing database
    app.config["SECRET_KEY"] = "hjshjhdjah kjshkjdhjs"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    db.init_app(app)
    app.logger.info("Database initialized.")

    # Importing routes
    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.logger.info("Blueprints registered.")

    # Initializing database file if needed
    create_database(app)

    # Initializing login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    app.logger.info("Login manager initialized.")

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not os.path.exists(DB_NAME):
        db.create_all(app=app)
        app.logger.info("Database Created!")
    else:
        app.logger.info("Database already existing!")
