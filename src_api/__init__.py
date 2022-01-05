from flask import Flask
import os
import logging


app = Flask(__name__, template_folder=os.path.join("..", "templates"))

# Configure logging
# Debug: 10, Info: 20, Warning: 30,  Error: 40,  Critical: 50

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")

log_file = "app.log"
if os.path.exists(log_file):
    os.remove(log_file)
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# logging.basicConfig(level=logging.INFO)
# logging.basicConfig(filename='app.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# Configure the flask app based on FLASK_ENV variable
if app.config["ENV"] == "" or app.config["ENV"] == "development":
    app.config.from_object("configuration.DevelopmentConfig")
    logger.setLevel(logging.DEBUG)

elif app.config["ENV"] == "production":
    app.config.from_object("configuration.ProductionConfig")
    logger.setLevel(logging.WARNING)

elif app.config["ENV"] == "testing":
    app.config.from_object("configuration.TestingConfig")
    logger.setLevel(logging.DEBUG)

from src_api import views
