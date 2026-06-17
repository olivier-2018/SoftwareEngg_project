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
    log_file = "app.log"
    if os.path.exists(log_file):
        try:
            os.remove(log_file)
            print("app.log detected and removed. New log file created.")
        except (SystemError, FileNotFoundError, PermissionError):
            print("Could not remove the app.log, will append logs to file.")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s:%(name)s:%(module)s.py:%(funcName)s:line %(lineno)d => %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    app.logger.info("Starting logging.")

    # Setting applicable environment variables
    app.config["APP_FOLDER"] = os.path.abspath(os.path.join(app.root_path, os.pardir))
    app.config["UPLOAD_FOLDER"] = os.path.join(app.config["APP_FOLDER"], "static", "client", "wav")

    app.logger.info("APP FOLDER: %s", app.config["APP_FOLDER"])
    app.logger.info("UPLOAD FOLDER: %s", app.config["UPLOAD_FOLDER"])

    flask_env = os.getenv("FLASK_ENV", "development")
    if flask_env == "" or flask_env == "development":
        app.config.from_object("configuration.DevelopmentConfig")
        logger.setLevel(logging.DEBUG)
    elif flask_env == "production":
        app.config.from_object("configuration.ProductionConfig")
        logger.setLevel(logging.WARNING)
    elif flask_env == "testing":
        app.config.from_object("configuration.TestingConfig")
        logger.setLevel(logging.INFO)

    app.logger.info("%s environment detected.", flask_env)

    # Initializing database
    db_dir = os.path.join(app.config["APP_FOLDER"], "sqlite_db")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, DB_NAME)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    db.init_app(app)
    app.logger.info("Database initialized.")

    # Importing routes
    from .views import views
    from .auth import auth
    from .misc import misc
    from .models import User
    from .misc import misc

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(misc, url_prefix="/")
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
        with app.app_context():
            db.create_all()
        app.logger.info("Database Created!")
    else:
        app.logger.info("Database already existing!")
