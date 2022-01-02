from src_api import app
from flask import render_template, request, redirect
import os
import librosa
import numpy as np
from werkzeug.utils import secure_filename
import tensorflow
import logging


logging.basicConfig(level=logging.INFO)
# logging.basicConfig(filename='app.log', level=logging.DEBUG,format=’%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s’)


@app.route("/", methods=["GET", "POST"])
def predict_from_file():

    prediction = ""

    if request.method == "POST":
        app.logger.info("=== FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        audiofile = request.files["file"]

        if audiofile.filename == "":
            return redirect(request.url)

        if audiofile:
            app.logger.info(f"AUDIO FILENAME: {audiofile.filename}")

            audiofile.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(audiofile.filename)))
            app.logger.info("Audio file saved.")

            model_path = app.config["APP_FOLDER"] + "/ML_model/audio_MNIST_v1.tf"
            app.logger.info(f"MODEL PATH: {model_path}")

            # tensorflow.get_logger().setLevel("ERROR")
            model = tensorflow.keras.models.load_model(model_path)
            app.logger.info("ML model loaded.")

            SAMPLING_RATE = 16_000
            MAX_DURATION_S = 0.5

            audio = np.zeros(int(MAX_DURATION_S * SAMPLING_RATE))
            path = os.path.join(app.config["UPLOAD_FOLDER"], audiofile.filename)

            app.logger.info("Reading audio file with librosa, then deleting wav file.")
            waveform, __ = librosa.load(path, sr=SAMPLING_RATE)
            os.remove(path)
            app.logger.debug("Uploaded file deleted after loading.")

            waveform = waveform[: len(audio)]
            audio[: len(waveform)] = waveform
            audio_input = audio.reshape((1, 8000, 1))

            app.logger.info("Making prediction.")
            prediction_proba = model.predict(audio_input)

            app.logger.info("Taking argmax of prediction probability.")
            prediction = np.argmax(prediction_proba)

    return render_template("index.html", model_prediction=prediction)


@app.route("/hello")
def helloworld():
    return "Hello world !"
