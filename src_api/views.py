from src_api import app
from flask import render_template, request, redirect
import os
import librosa
import numpy as np
from werkzeug.utils import secure_filename
import tensorflow


@app.route("/", methods=["GET", "POST"])
@app.route("/predict_from_file", methods=["GET", "POST"])
def predict_from_file():
    """Makes a digit prediction by uploading a wav file using the audio MNIST ML model

    Returns:
        [render_template]: Render template object with prediction variable (int)
    """

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
            app.logger.warning("No filename selected.")
            return redirect(request.url)

        if request_object:
            audio_filename = request_object.filename

            # Save selected audio file on server backend
            backend_save_request_object(request_object)

            # Process audio file if required (future app developments)
            # waveform, sr_read = backend_rawfile_load (audio_filename, upload_path=app.config["UPLOAD_FOLDER"])

            # Query basic audio characteristics
            sampling_rate = get_sampling_rate(audio_filename, upload_path=app.config["UPLOAD_FOLDER"])
            duration = get_duration(audio_filename, upload_path=app.config["UPLOAD_FOLDER"])

            # Set ML model input layer dimensional constraint
            model_input_dim = 8000

            # Adjust sampling rate if required (future app developments)
            # new_sampling_rate = int(model_input_dim / duration)

            # Load audio sequence
            audio_sequence = load_audio_sequence(
                filename=audio_filename, sampling_rate=sampling_rate, max_seq_length=model_input_dim, upload_path=app.config["UPLOAD_FOLDER"]
            )

            # Supress audio file on backend server
            backend_file_delete(audio_filename)

            # Save processed audio sequence (DEBUG for future app developments)
            # sf.write('test.wav', audio_sequence, new_sampling_rate, 'PCM_16')

            # Load ML model based on installed Tensorflow version (necessary to handle conda vs pip TF version)
            TF_ver = tensorflow.__version__
            if TF_ver == "2.3.0":
                model = load_ML_model(model_path="/ML_model/audio_MNIST_v3-TF_v2.3.0.tf")
                app.logger.info("Tensorflow v2.3.0 (conda) detected, ML model audio_MNIST_v3-TF_v2.3.0.tf used.")
            elif TF_ver == "2.7.0":
                model = load_ML_model(model_path="/ML_model/audio_MNIST_v3-TF_v2.7.0.tf")
                app.logger.info("Tensorflow v2.7.0 (pip) detected, ML model audio_MNIST_v3-TF_v2.7.0.tf used.")
            else:
                app.logger.error("App requires either Tensorflow v2.3.0 (conda) or Tensorflow 2.7.0 (pip) installed.")
                return redirect(request.url)

            # Make prediction based on ML model and audio sequence input
            prediction = make_prediction(model, audio_sequence, model_input_dim)

    return render_template("index.html", model_prediction=prediction)


def backend_save_request_object(request_object: complex, upload_path: str = app.config["UPLOAD_FOLDER"]) -> None:
    """Saves a POST request object in the upload folder in the backend app server (locally or deployed)

    Args:
        request_object (flask request object): selected flask POST request object
        upload_path (str, optional): Upload folder path on backend server. Defaults to app.config["UPLOAD_FOLDER"].

    Returns:
        None
    """
    app.logger.info("===== backend_save_request_object =====")
    filename = request_object.filename
    app.logger.debug(f"Selected filename: {filename}")

    path = os.path.join(upload_path, secure_filename(filename))
    request_object.save(path)
    app.logger.debug(f"File {filename} saved in {upload_path}")
    return None


def backend_rawfile_load(filename: str, upload_path: str = app.config["UPLOAD_FOLDER"]) -> complex:
    """Load an audio sequence from a wav file using the native sampling rate.

    Args:
        filename (str):  audio wav filename
        upload_path (str, optional): Upload folder path on backend server. Defaults to app.config["UPLOAD_FOLDER"].

    Returns:
        numpy array: audio sequence (mono channel)
    """
    app.logger.info("===== backend_rawfile_load =====")
    path = os.path.join(upload_path, filename)
    waveform, sr_read = librosa.core.load(path, sr=None)
    app.logger.debug(f"Loading waveform of type: {type(waveform)}, shape: {waveform.shape} and sampling rate: {sr_read}")
    return waveform


def backend_file_load(filename: str, sampling_rate: int = None, upload_path: str = app.config["UPLOAD_FOLDER"]) -> complex:
    """Load an audio sequence from a wav file using the specified sampling rate.

    Args:
        filename (str): audio wav filename
        sampling_rate (int, optional): sampling rate to use when loading audio sequence. Defaults to None.
        upload_path (type, optional): Backend client upload folder path. Defaults to app.config["UPLOAD_FOLDER"].

    Returns:
        numpy array: audio sequence (mono channel)
    """
    app.logger.info("===== load_sound_file =====")
    path = os.path.join(upload_path, filename)
    waveform, sr_read = librosa.core.load(path, sr=sampling_rate)
    app.logger.debug(f"Loading waveform of type: {type(waveform)}, shape: {waveform.shape} and sampling rate: {sr_read}")
    return waveform


def get_duration(filename: str, upload_path: str = app.config["UPLOAD_FOLDER"]) -> float:
    """Query native duration of audio file seuqence (in sec).

    Args:
        filename (str): audio wav filename
        upload_path (str, optional): Upload folder path on backend server. Defaults to app.config["UPLOAD_FOLDER"].

    Returns:
        float: Audio file duration (in seconds)
    """
    app.logger.info("===== get_duration =====")
    path = os.path.join(upload_path, filename)
    duration = librosa.get_duration(filename=path)
    app.logger.debug(f"File {filename} has duration= {duration}sec")
    return duration


def get_sampling_rate(filename: str, upload_path: str = app.config["UPLOAD_FOLDER"]) -> int:
    """Query native sampling rate of audio file sequence.

    Args:
        filename (str): audio wav filename
        upload_path (str, optional): Upload folder path on backend server. Defaults to app.config["UPLOAD_FOLDER"].

    Returns:
        int: Audio file sampling rate
    """
    app.logger.info("===== get_sampling_rate =====")
    path = os.path.join(upload_path, filename)
    sampling_rate = librosa.get_samplerate(path)
    app.logger.debug(f"File {filename} has sampling_rate: {sampling_rate}")
    return sampling_rate


def load_audio_sequence(
    filename: str, sampling_rate: int = 8000, max_seq_length: int = 8000, upload_path: str = app.config["UPLOAD_FOLDER"]
) -> complex:
    """Load sequence from audio file using specified sampling rate and generates a ML model compatible input.

    Args:
        filename (str): audio wav filename
        sampling_rate (int, optional): Required sampling rate. Defaults to 8000.
        max_seq_length (int, optional): ML model maximum input sequence length. Defaults to 8000.
        upload_path (str, optional): Upload folder path on backend server. Defaults to app.config["UPLOAD_FOLDER"].

    Returns:
        numpy array: ML model input layer compatible array of floats.
    """
    app.logger.info("===== load_audio_sequence =====")
    path = os.path.join(upload_path, filename)

    waveform, __ = librosa.core.load(path, sr=sampling_rate)
    app.logger.debug(f"File {filename} read with sampling_rate {sampling_rate}Hz and shape {waveform.shape}")

    audio_sequence = np.zeros(max_seq_length)
    waveform = waveform[: len(audio_sequence)]
    audio_sequence[: len(waveform)] = waveform
    app.logger.debug(f"audio_sequence adjusted to shape {audio_sequence.shape}")

    return audio_sequence


def backend_file_delete(filename: str, upload_path: str = app.config["UPLOAD_FOLDER"]) -> None:
    """Delete audio file on backend server.

    Args:
        filename (str): audio wav filename
        upload_path (str, optional): Upload folder path on backend server. Defaults to app.config["UPLOAD_FOLDER"].

    Returns:
        None
    """
    app.logger.info("===== backend_file_delete =====")
    path = os.path.join(upload_path, filename)
    os.remove(path)
    app.logger.debug(f"File {filename} deleted in {upload_path}.")
    return None


def play_sound():
    """Play audio wave sound (future development)"""


def load_ML_model(model_path: str = "/ML_model/audio_MNIST_v1.tf") -> complex:
    """Load tensorflow Keras ML model

    Args:
        model_path (str, optional): ML model folder path on backend server. Defaults to "/ML_model/audio_MNIST_v1.tf".

    Returns:
        Keras model: tensorflow Keras ML model to be used for prediction
    """
    app.logger.info("===== load_ML_model =====")
    path = app.config["APP_FOLDER"] + model_path
    app.logger.debug(f"model path: {path}")

    tensorflow.get_logger().setLevel("ERROR")
    model = tensorflow.keras.models.load_model(path)
    app.logger.debug("ML model loaded.")

    return model


def make_prediction(model, audio_sequence, model_input_dim: str = 8000) -> int:
    """Generates a probability distribution corresponding to 0-9 digits from the provided audio sequence using the ML model.
        Returns the argmax of the probability distribution.

    Args:
        model (tensorflow model): Trained audio MNIST model (test accuracy~93%)
        audio_sequence (numpy array, dtype=float64): Audio sequence used ML model input
        model_input_dim (int, optional): ML model input layer dimension . Defaults to 8000.

    Returns:
        int: Argmax of model predicted probability ( digits between 0 to 9)
    """
    app.logger.info("===== make_prediction =====")

    prediction_proba = model.predict(audio_sequence.reshape(1, model_input_dim, 1))

    app.logger.warning("Taking argmax of prediction probability.")
    prediction = np.argmax(prediction_proba)

    app.logger.info(f"Prediction: {prediction}")

    return prediction


@app.route("/hello")
def helloworld() -> str:
    return "Hello world !"
