from flask import Blueprint, current_app, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
import os
import shutil
import pathlib
import librosa
import numpy as np
from werkzeug.utils import secure_filename
import tensorflow
import soundfile as sf
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

views = Blueprint("views", __name__)


@views.route("/predict_from_file", methods=["GET", "POST"])
@views.route("/predict_from_mic", methods=["GET", "POST"])
@login_required
def predict_from_file():
    """Makes a digit prediction by uploading a wav file using the audio MNIST ML model

    Returns:
        [render_template]: Render template object with prediction variable (int)
    """

    UPLOAD_FOLDER = current_app.config["UPLOAD_FOLDER"]
    APP_FOLDER = current_app.config["APP_FOLDER"]
    img_filename = ""
    prediction = ""
    audio_sequence = np.zeros(1)

    if request.method == "POST":
        current_app.logger.info("=== FORM RECEIVED ===")

        if "file" not in request.files:
            current_app.logger.error("=== No selected file detected ===")
            return redirect(request.url)

        request_object = request.files["file"]

        if is_valid_filename(request_object):
            audio_filename = request_object.filename
            # Save selected audio file on server backend
            backend_save_request_object(request_object, upload_path=UPLOAD_FOLDER)
        else:
            current_app.logger.error("Invalid filename.")
            flash("Invalid filename", category="error")
            return redirect(request.url)

        if not is_valid_audio_file(audio_filename, upload_path=UPLOAD_FOLDER):

            flash("Invalid file format (not an audio wav file)", category="error")
            return redirect(request.url)

        else:

            # Process audio file if required (future app developments)
            # waveform, sr_read = backend_rawfile_load (audio_filename, upload_path=UPLOAD_FOLDER)

            # Query basic audio characteristics
            sampling_rate = get_sampling_rate(audio_filename, upload_path=UPLOAD_FOLDER)
            duration = get_duration(audio_filename, upload_path=UPLOAD_FOLDER)

            # Set ML model input layer dimensional constraint
            model_input_dim = 8000

            # Adjust sampling rate if required (future app developments)
            # new_sampling_rate = int(model_input_dim / duration)

            # Load audio sequence
            audio_sequence = load_audio_sequence(
                filename=audio_filename, upload_path=UPLOAD_FOLDER, sampling_rate=8000, max_seq_length=model_input_dim
            )

            # Supress audio file on backend server
            backend_file_delete(audio_filename, upload_path=UPLOAD_FOLDER)

            # Save processed audio sequence (DEBUG for future app developments)
            # sf.write('test.wav', audio_sequence, new_sampling_rate, 'PCM_16')

            # Load ML model based on installed Tensorflow version (necessary to handle conda vs pip TF version)
            TF_ver = tensorflow.__version__
            if TF_ver == "2.3.0":
                current_app.logger.info("Tensorflow v2.3.0 (conda) detected, ML model audio_MNIST_v3-TF_v2.3.0.tf used.")
                model = load_ML_model(model_path="/ML_model/audio_MNIST_v3-TF_v2.3.0.tf")
            elif TF_ver == "2.7.0":
                current_app.logger.info("Tensorflow v2.7.0 (pip) detected, ML model audio_MNIST_v3-TF_v2.7.0.tf used.")
                model = load_ML_model(model_path="/ML_model/audio_MNIST_v3-TF_v2.7.0.tf")
            else:
                current_app.logger.critical("App requires either Tensorflow v2.3.0 (conda) or Tensorflow 2.7.0 (pip) installed.")
                flash("App requires either Tensorflow v2.3.0 (conda) or Tensorflow 2.7.0 (pip) installed.", category="error")
                return redirect(request.url)

            # Make prediction based on ML model and audio sequence input
            prediction = make_prediction(model, audio_sequence, model_input_dim)

            # Generate waveform picture
            img_path = os.path.join(APP_FOLDER, "static", "client", img_filename)
            img_filename = plot_audio(audio_sequence, label=audio_filename, path=img_path, sr=8000)

    URL_rule = request.url_rule
    current_app.logger.debug("Endpoint detected: %s", URL_rule)

    if "file" in URL_rule.rule:
        return render_template("predict_from_file.html", model_prediction=prediction, user=current_user, filename=img_filename)

    elif "mic" in URL_rule.rule:
        return render_template("predict_from_mic.html", model_prediction=prediction, user=current_user, filename=img_filename)


@views.route("/display/<filename>")
@login_required
def display_image(filename: str):
    """Create dynamic URL with image filename as key

    Args:
        filename (str): Image filename

    Returns:
        flask: redirect to dynamic url (permanent ie code=301)
    """
    current_app.logger.debug("Image filename: %s", filename)
    return redirect(url_for("static", filename=os.path.join("client", "img", filename)), code=301)


def plot_audio(audio: complex, label: str, path: str, sr=8000) -> str:
    """Generate a waveform plot of the audio signal

    Args:
        audio (numpy array): audio sequence (mono-channel)
        label (str): [description]
        path (str): path to image storage location on app backend server
        sr (int, optional): sampling rate. Defaults to 8000.

    Returns:
        str: image filename (hard coded)
    """
    img_filename = "waveform.png"
    img_path = os.path.join(path, img_filename)
    fig, ax = plt.subplots()
    duration = len(audio) / sr
    t = np.linspace(0, duration, len(audio))
    ax.plot(t, audio)
    ax.set_title(label)
    ax.set_xlabel("Time")
    plt.savefig(img_path)
    current_app.logger.info("Waveform chart saved in path: %s", img_path)

    img_path_copy = os.path.join(path, "img", img_filename)
    shutil.copyfile(img_path, img_path_copy)
    current_app.logger.debug("url_for bug: Image copied in path: %s", img_path)

    return img_filename


def is_valid_filename(request_object: complex) -> bool:
    """Check filename extension

    Returns:
        [render_template]: Render template object with prediction variable (int)
    """
    current_app.logger.info("Check filename extension")
    if request_object.filename == "":
        current_app.logger.error("No filename selected.")
        return False
    elif not pathlib.Path(request_object.filename).suffix.lower() == ".wav":
        current_app.logger.warning("Wrong file extension. Is this really a wav audio file ?")
    else:
        current_app.logger.debug("Correct file extension detected.")
    return True


def backend_save_request_object(request_object: complex, upload_path: str) -> None:
    """Saves a POST request object in the upload folder in the backend app server (locally or deployed)

    Args:
        request_object (flask request object): selected flask POST request object
        upload_path (str, optional): Upload folder path on backend server.

    Returns:
        None
    """
    current_app.logger.info("===== backend_save_request_object =====")
    filename = request_object.filename
    current_app.logger.debug("Selected filename: %s", filename)

    path = os.path.join(upload_path, secure_filename(filename))
    current_app.logger.debug("Selected path: %s", path)
    request_object.save(path)
    current_app.logger.debug("File %s saved in %s", filename, upload_path)
    return None


def is_valid_audio_file(audio_filename: str, upload_path: str) -> bool:
    """Check audio file format

    Args:
        filename (str):  audio wav filename
        upload_path (str, optional): Upload folder path on backend server.

    Returns:
        Bool: True if file format is a wav audio, False otherwise
    """

    current_app.logger.info("Checking audio file format.")

    path = os.path.join(upload_path, audio_filename)
    current_app.logger.debug("Selected path: %s", path)
    try:
        s = sf.info(path)
    except RuntimeError:
        current_app.logger.warning("Cannot open audio file. Selected file is not an audio file. File deleted.")
        backend_file_delete(audio_filename, upload_path)
        return False

    if s.format.lower() == "wav":
        current_app.logger.info("Detected wav audio format.")
        return True
    else:
        current_app.logger.warning("Selected file is not a wav audio format.")
        return False


def backend_rawfile_load(filename: str, upload_path: str) -> complex:
    """Load an audio sequence from a wav file using the native sampling rate.

    Args:
        filename (str):  audio wav filename
        upload_path (str, optional): Upload folder path on backend server.

    Returns:
        numpy array: audio sequence (mono channel)
    """
    current_app.logger.info("===== backend_rawfile_load =====")
    path = os.path.join(upload_path, filename)
    waveform, sr_read = librosa.core.load(path, sr=None)
    current_app.logger.debug("Loading waveform of type: %s , shape: %s and sampling rate: %s", type(waveform), waveform.shape, sr_read)
    return waveform


def backend_file_load(filename: str, upload_path: str, sampling_rate: int = None) -> complex:
    """Load an audio sequence from a wav file using the specified sampling rate.

    Args:
        filename (str): audio wav filename
        sampling_rate (int, optional): sampling rate to use when loading audio sequence. Defaults to None.
        upload_path (type, optional): Backend client upload folder path.

    Returns:
        numpy array: audio sequence (mono channel)
    """
    current_app.logger.info("===== load_sound_file =====")
    path = os.path.join(upload_path, filename)
    waveform, sr_read = librosa.core.load(path, sr=sampling_rate)
    current_app.logger.debug("Loading waveform of type: %s, shape: %s and sampling rate: %s", type(waveform), waveform.shape, sr_read)
    return waveform


def get_duration(filename: str, upload_path: str) -> float:
    """Query native duration of audio file seuqence (in sec).

    Args:
        filename (str): audio wav filename
        upload_path (str, optional): Upload folder path on backend server.

    Returns:
        float: Audio file duration (in seconds)
    """
    current_app.logger.info("===== get_duration =====")
    path = os.path.join(upload_path, filename)
    duration = librosa.get_duration(filename=path)
    current_app.logger.debug("File %s has duration= %ssec", filename, duration)
    return duration


def get_sampling_rate(filename: str, upload_path: str) -> int:
    """Query native sampling rate of audio file sequence.

    Args:
        filename (str): audio wav filename
        upload_path (str, optional): Upload folder path on backend server.

    Returns:
        int: Audio file sampling rate
    """
    current_app.logger.info("===== get_sampling_rate =====")
    path = os.path.join(upload_path, filename)
    sampling_rate = librosa.get_samplerate(path)
    current_app.logger.debug("File %s has sampling_rate: %s", filename, sampling_rate)
    return sampling_rate


def load_audio_sequence(filename: str, upload_path: str, sampling_rate: int = 8000, max_seq_length: int = 8000) -> complex:
    """Load sequence from audio file using specified sampling rate and generates a ML model compatible input.

    Args:
        filename (str): audio wav filename
        sampling_rate (int, optional): Required sampling rate. Defaults to 8000.
        max_seq_length (int, optional): ML model maximum input sequence length. Defaults to 8000.
        upload_path (str, optional): Upload folder path on backend server.

    Returns:
        numpy array: ML model input layer compatible array of floats.
    """
    current_app.logger.info("===== load_audio_sequence =====")
    path = os.path.join(upload_path, filename)

    waveform, __ = librosa.core.load(path, sr=sampling_rate)
    current_app.logger.debug("File %s read with sampling_rate %sHz and shape %s", filename, sampling_rate, waveform.shape)

    audio_sequence = np.zeros(max_seq_length)
    waveform = waveform[: len(audio_sequence)]
    audio_sequence[: len(waveform)] = waveform
    current_app.logger.debug("audio_sequence adjusted to shape %s", audio_sequence.shape)

    return audio_sequence


def backend_file_delete(filename: str, upload_path: str) -> None:
    """Delete audio file on backend server.

    Args:
        filename (str): audio wav filename
        upload_path (str, optional): Upload folder path on backend server.

    Returns:
        None
    """
    current_app.logger.info("===== backend_file_delete =====")
    path = os.path.join(upload_path, filename)
    os.remove(path)
    current_app.logger.debug("File %s deleted in %s.", filename, upload_path)
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
    current_app.logger.info("===== load_ML_model =====")
    path = current_app.config["APP_FOLDER"] + model_path
    current_app.logger.debug("model path: %s", path)

    tensorflow.get_logger().setLevel("ERROR")
    model = tensorflow.keras.models.load_model(path)
    current_app.logger.debug("ML model loaded.")

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
    current_app.logger.info("===== make_prediction =====")

    prediction_proba = model.predict(audio_sequence.reshape(1, model_input_dim, 1))

    current_app.logger.warning("Taking argmax of prediction probability.")
    prediction = np.argmax(prediction_proba)

    current_app.logger.info("Prediction: %s", prediction)

    return prediction


@views.route("/hello")
def helloworld() -> str:
    return "Hello world !"
