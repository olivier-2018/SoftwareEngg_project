from flask import Flask
import os

app = Flask(__name__, template_folder="../templates")

from src_api import views

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename='app.log', level=logging.DEBUG,format=’%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s’)

app.config["APP_FOLDER"] = os.path.abspath(os.path.join(app.root_path, os.pardir))
app.logger.info("APP FOLDER: " + app.config["APP_FOLDER"])

app.config["UPLOAD_FOLDER"] = app.config["APP_FOLDER"] + "/static/client/wav"
app.logger.info("UPLOAD FOLDER: " + app.config["UPLOAD_FOLDER"])

app.config["ALLOWED_EXTENSIONS"] = set(["wav"])
