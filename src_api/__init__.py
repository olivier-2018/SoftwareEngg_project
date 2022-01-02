from flask import Flask
import os


app = Flask(__name__, template_folder=os.path.join("..", "templates"))

# Configure the flask app based on FLASK_ENV variable
if app.config["ENV"] == "" or app.config["ENV"] == "development":
    app.config.from_object("configuration.DevelopmentConfig")

elif app.config["ENV"] == "production":
    app.config.from_object("configuration.ProductionConfig")

elif app.config["ENV"] == "testing":
    app.config.from_object("configuration.TestingConfig")

from src_api import views
