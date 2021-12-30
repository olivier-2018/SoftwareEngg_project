from flask import Flask
import os

app = Flask(__name__, template_folder=os.path.join("..", "templates"))

from src_api import views

app.config["APP_FOLDER"] = os.path.abspath(os.path.join(app.root_path, os.pardir))
app.config["UPLOAD_FOLDER"] = os.path.join(app.config["APP_FOLDER"], "static", "client", "wav")

app.config["ALLOWED_EXTENSIONS"] = set(["wav"])
