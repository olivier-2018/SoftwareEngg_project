from src_api import app
from flask import render_template, request, redirect
import os
import librosa
import numpy as np
from werkzeug.utils import secure_filename
import tensorflow


@app.route("/", methods=["GET", "POST"])
def predict_from_file():

    prediction = ""

    if request.method == "POST":
        app.logger.info("=== FORM RECEIVED ===")

        if "file" not in request.files:
            app.logger.error("=== No file detected ===")
            return redirect(request.url)

        request_object = request.files["file"]
        app.logger.debug(f"Type request_object: {type(request_object)}")
        app.logger.debug(f"dir request_object: {dir(request_object)}")

        if request_object.filename == "":
            return redirect(request.url)

        if request_object:
            audio_filename = request_object.filename

            backend_save_request_object(request_object)

            # waveform, sr_read = backend_rawfile_load (audio_filename, upload_path=app.config["UPLOAD_FOLDER"])

            sampling_rate = get_sampling_rate(audio_filename, upload_path=app.config["UPLOAD_FOLDER"])
            duration = get_duration(audio_filename, upload_path=app.config["UPLOAD_FOLDER"])

            model_input_dim = 8000

            int(model_input_dim / duration)

            audio_sequence = load_audio_sequence(
                filename=audio_filename, sampling_rate=sampling_rate, max_seq_length=model_input_dim, upload_path=app.config["UPLOAD_FOLDER"]
            )

            backend_file_delete(audio_filename)

            # sf.write('test.wav', audio_sequence, new_sampling_rate, 'PCM_16')

            model = load_ML_model(model_path="/ML_model/audio_MNIST_v3.tf")

            prediction = make_prediction(model, audio_sequence, model_input_dim)

    return render_template("index.html", model_prediction=prediction)


def backend_save_request_object(request_object, upload_path=app.config["UPLOAD_FOLDER"]):
    app.logger.info("===== backend_save_request_object =====")
    filename = request_object.filename
    app.logger.debug(f"Selected filename: {filename}")

    path = os.path.join(upload_path, secure_filename(filename))
    request_object.save(path)
    app.logger.debug(f"File {filename} saved in {upload_path}")
    return None


def backend_rawfile_load(filename, upload_path=app.config["UPLOAD_FOLDER"]):
    app.logger.info("===== backend_rawfile_load =====")
    path = os.path.join(upload_path, filename)
    waveform, sr_read = librosa.core.load(path, sr=None)
    app.logger.debug(f"Loading waveform of type: {type(waveform)}, shape: {waveform.shape} and sampling rate: {sr_read}")
    return waveform


def backend_file_load(filename, sampling_rate=None, upload_path=app.config["UPLOAD_FOLDER"]):
    app.logger.info("===== load_sound_file =====")
    path = os.path.join(upload_path, filename)
    waveform, sr_read = librosa.core.load(path, sr=sampling_rate)
    app.logger.debug(f"Loading waveform of type: {type(waveform)}, shape: {waveform.shape} and sampling rate: {sr_read}")
    return waveform


def get_duration(filename, upload_path=app.config["UPLOAD_FOLDER"]):
    app.logger.info("===== get_duration =====")
    path = os.path.join(upload_path, filename)
    duration = librosa.get_duration(filename=path)
    app.logger.debug(f"File {filename} has duration= {duration}sec")
    return duration


def get_sampling_rate(filename, upload_path=app.config["UPLOAD_FOLDER"]):
    app.logger.info("===== get_sampling_rate =====")
    path = os.path.join(upload_path, filename)
    sampling_rate = librosa.get_samplerate(path)
    app.logger.debug(f"File {filename} has sampling_rate: {sampling_rate}")
    return sampling_rate


def load_audio_sequence(filename, sampling_rate=8000, max_seq_length=8000, upload_path=app.config["UPLOAD_FOLDER"]):
    app.logger.info("===== load_audio_sequence =====")
    path = os.path.join(upload_path, filename)

    waveform, __ = librosa.core.load(path, sr=sampling_rate)
    app.logger.debug(f"File {filename} read with sampling_rate {sampling_rate}Hz and shape {waveform.shape}")

    audio_sequence = np.zeros(max_seq_length)
    waveform = waveform[: len(audio_sequence)]
    audio_sequence[: len(waveform)] = waveform
    app.logger.debug(f"audio_sequence adjusted to shape {audio_sequence.shape}")

    return audio_sequence


def backend_file_delete(filename, upload_path=app.config["UPLOAD_FOLDER"]):
    app.logger.info("===== backend_file_delete =====")
    path = os.path.join(upload_path, filename)
    os.remove(path)
    app.logger.debug(f"File {filename} deleted in {upload_path}.")
    return None


def play_sound():
    pass


def load_ML_model(model_path="/ML_model/audio_MNIST_v1.tf"):
    app.logger.info("===== load_ML_model =====")
    # path = os.path.join(app.config["APP_FOLDER"], model_path)
    path = app.config["APP_FOLDER"] + model_path
    app.logger.debug(f"model path: {path}")

    tensorflow.get_logger().setLevel("ERROR")
    model = tensorflow.keras.models.load_model(path)
    app.logger.debug("ML model loaded.")

    return model


def make_prediction(model, audio_sequence, model_input_dim=8000):
    app.logger.info("===== make_prediction =====")

    prediction_proba = model.predict(audio_sequence.reshape(1, model_input_dim, 1))

    app.logger.warning("Taking argmax of prediction probability.")
    prediction = np.argmax(prediction_proba)

    app.logger.info(f"Prediction: {prediction}")

    return prediction


@app.route("/hello")
def helloworld():
    return "Hello world !"
