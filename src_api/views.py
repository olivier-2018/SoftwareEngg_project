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

    URL_rule = request.url_rule
    is_mic_route = "mic" in URL_rule.rule

    if request.method == "POST":
        current_app.logger.info("=== FORM RECEIVED ===")

        if "file" not in request.files:
            current_app.logger.error("=== No selected file detected ===")
            return redirect(request.url)

        request_object = request.files["file"]

        if is_valid_filename(request_object, allow_webm=is_mic_route):
            audio_filename = request_object.filename
            # Save selected audio file on server backend
            backend_save_request_object(request_object, upload_path=UPLOAD_FOLDER)
        else:
            current_app.logger.error("Invalid filename.")
            flash("Invalid filename", category="error")
            return redirect(request.url)

        if not is_valid_audio_file(audio_filename, upload_path=UPLOAD_FOLDER, allow_webm=is_mic_route):

            flash("Invalid file format", category="error")
            current_app.logger.info("Invalid audio file format.")
            return redirect(request.url)

        else:

            # Read raw audio file
            waveform, sr_read = backend_rawfile_load(audio_filename, upload_path=UPLOAD_FOLDER)

            # Query basic audio characteristics
            # sampling_rate = get_sampling_rate(audio_filename, upload_path=UPLOAD_FOLDER)
            # duration = get_duration(audio_filename, upload_path=UPLOAD_FOLDER)

            # Set ML model constraints (hard coded)
            model_input_dim = 8000
            model_sampling_rate = 8000

            # Adjust sampling rate if required (future app developments)
            # new_sampling_rate = int(model_input_dim / duration)

            # Process audio file if required (future app developments)
            audio_sequence = audio_process(waveform, sr=sr_read, model_dim=model_input_dim, model_sr=model_sampling_rate)

            # Save processed audio sequence (DEBUG for future app developments)
            # sf.write('test.wav', audio_sequence, new_sampling_rate, 'PCM_16')

            # Load audio sequence
            # audio_sequence = load_audio_sequence(
            #     filename=audio_filename, upload_path=UPLOAD_FOLDER, sampling_rate=8000, max_seq_length=model_input_dim
            # )

            # Supress audio file on backend server
            backend_file_delete(audio_filename, upload_path=UPLOAD_FOLDER)

            # Load ML model
            current_app.logger.info("Loading ML model audio_MNIST_v3-TF_v2.7.0.tf (TensorFlow v%s).", tensorflow.__version__)
            model = load_ML_model(model_path="/ML_model/audio_MNIST_v3-TF_v2.7.0.tf")

            # Make prediction based on ML model and audio sequence input
            prediction = make_prediction(audio_sequence, model, model_input_dim)

            # Generate waveform picture
            img_path = os.path.join(APP_FOLDER, "static", "client")
            img_filename = plot_audio(audio_sequence, label=audio_filename, path=img_path, sr=8000)

    current_app.logger.debug("Endpoint detected: %s", URL_rule)

    if "file" in URL_rule.rule:
        return render_template("predict_from_file.html", model_prediction=prediction, user=current_user, filename=img_filename)

    elif "mic" in URL_rule.rule:
        # For POST requests from the mic page, return JSON so JavaScript can update the page
        if request.method == "POST":
            from flask import jsonify
            return jsonify({"prediction": int(prediction), "filename": img_filename})
        else:
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


def audio_process(waveform, sr, model_dim=8000, model_sr=8000):
    """Process audio signal to ensure it matches ML model constraints and requirements (sampling frequency and input layer dimension)

    Args:
        waveform (numpy array): raw audio sequence
        sr (int): raw audio sampling rate (read from file)
        model_dim (int): ML model input layer dimension. Default to 8000.
        model_sr (int): ML model sampling frequency. Default to 8000.

    Returns:
        numpy array: process audio sequence, ready for ML model prediction.
    """
    current_app.logger.info("===== audio_processing =====")

    audio_sequence = np.zeros(model_dim)

    duration = librosa.get_duration(y=waveform, sr=sr)
    audio_seq_length = waveform.shape[0]
    current_app.logger.debug("input signal: sequence_length= %s, sampling rate=%s, duration=%s", audio_seq_length, sr, duration)

    if not sr == model_sr:
        waveform = librosa.resample(waveform, orig_sr=sr, target_sr=model_sr)
        audio_seq_length = waveform.shape[0]
        duration = librosa.get_duration(y=waveform, sr=model_sr)
        current_app.logger.debug("resampled signal: sequence_length= %s, sampling rate=%s, duration=%s", audio_seq_length, model_sr, duration)

    if audio_seq_length > model_dim:
        trimmed_waveform, indexes = librosa.effects.trim(waveform, top_db=35, frame_length=256, hop_length=64)
        trimmed_signal_length = indexes[1] - indexes[0]

        current_app.logger.debug("audio sequence longer than model input dimension... Trimming audio signal to dim: %s", trimmed_waveform.shape)

        if trimmed_signal_length < model_dim:
            int(trimmed_signal_length / 2)
            # audio_sequence[start_idx: start_idx+trimmed_signal_length] = trimmed_waveform
            audio_sequence[:trimmed_signal_length] = trimmed_waveform
            current_app.logger.debug("Trimmed signal shorter than model input dimension... centering signal.")
        else:
            current_app.logger.debug("Trimmed signal still longer than model input dimension... signal will be truncated.")
            audio_sequence = trimmed_waveform[:model_dim]
    else:
        current_app.logger.debug("Audio signal shorter than model input dimension... centering signal.")
        int(audio_seq_length / 2)
        # audio_sequence[start_idx: start_idx+audio_seq_length]  = waveform
        audio_sequence[:audio_seq_length] = waveform
    current_app.logger.debug("Audio_sequence adjusted to model input layer shape %s", audio_sequence.shape)

    return audio_sequence


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


def is_valid_filename(request_object: complex, allow_webm: bool = False) -> bool:
    """Check filename extension

    Args:
        request_object: Flask file request object
        allow_webm: If True, accept both .wav and .webm extensions. If False, only accept .wav.

    Returns:
        bool: True if filename is valid, False otherwise
    """
    current_app.logger.info("Check filename extension")
    if request_object.filename == "":
        current_app.logger.error("No filename selected.")
        return False

    ext = pathlib.Path(request_object.filename).suffix.lower()
    allowed_exts = {".wav", ".webm"} if allow_webm else {".wav"}

    if ext not in allowed_exts:
        current_app.logger.warning("Wrong file extension. Expected %s, got %s", allowed_exts, ext)
        return False

    current_app.logger.debug("Correct file extension detected: %s", ext)
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


def is_valid_audio_file(audio_filename: str, upload_path: str, allow_webm: bool = False) -> bool:
    """Check audio file format

    Args:
        audio_filename (str): audio filename
        upload_path (str): Upload folder path on backend server
        allow_webm (bool): If True, accept both WAV and WebM formats. If False, only WAV.

    Returns:
        bool: True if file is a valid audio format, False otherwise
    """

    current_app.logger.info("Checking audio file format.")

    path = os.path.join(upload_path, audio_filename)
    current_app.logger.debug("Selected path: %s", path)

    # For WebM files, librosa.load will handle them via audioread backend
    # For WAV files, verify with soundfile
    if allow_webm and audio_filename.lower().endswith(".webm"):
        try:
            # Quick validation: try to open with librosa
            librosa.get_duration(path=path)
            current_app.logger.info("Detected WebM audio format.")
            return True
        except Exception as e:
            current_app.logger.warning("Cannot open WebM audio file: %s", str(e))
            backend_file_delete(audio_filename, upload_path)
            return False

    # Standard WAV validation
    try:
        s = sf.info(path)
    except RuntimeError:
        current_app.logger.warning("Cannot open audio file. Selected file is not an audio file. File deleted.")
        backend_file_delete(audio_filename, upload_path)
        return False

    if s.format.lower() == "wav":
        current_app.logger.info("Detected WAV audio format.")
        return True
    else:
        current_app.logger.warning("Selected file is not a WAV audio format.")
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
    current_app.logger.debug("Loading waveform %s of type: %s , shape: %s and sampling rate: %s", filename, type(waveform), waveform.shape, sr_read)
    return waveform, sr_read


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
    """Load tensorflow SavedModel serving signature for inference

    Args:
        model_path (str, optional): ML model folder path on backend server. Defaults to "/ML_model/audio_MNIST_v1.tf".

    Returns:
        tensorflow SavedModel concrete function: ML model to be used for prediction
    """
    current_app.logger.info("===== load_ML_model =====")
    path = current_app.config["APP_FOLDER"] + model_path
    current_app.logger.debug("model path: %s", path)

    tensorflow.get_logger().setLevel("ERROR")
    # Load only the serving graph, avoiding the optimizer state loading issue
    import tensorflow as tf
    from tensorflow.python.saved_model import loader
    from tensorflow.python.saved_model import tag_constants

    # Use the low-level loader to load only the serving graph
    sess = tf.compat.v1.Session()
    metagraph = loader.load(sess, [tag_constants.SERVING], path)
    # Get the serving signature
    signature = metagraph.signature_def[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]

    # Create a callable that uses this session and signature
    class SignatureModel:
        def __init__(self, sess, sig, tag, model_path):
            self.sess = sess
            self.sig = sig
            self.input_key = list(sig.inputs.keys())[0]
            self.output_key = list(sig.outputs.keys())[0]
            # Extract model name from path (e.g., "v2.3.0" → "functional_1", "v2.7.0" → "model")
            self.name = "functional_1" if "v2.3.0" in model_path else "model"

        def __call__(self, input_tensor):
            input_name = self.sig.inputs[self.input_key].name
            output_name = self.sig.outputs[self.output_key].name
            result = self.sess.run(output_name, {input_name: input_tensor.numpy()})
            return tf.constant(result)

    model = SignatureModel(sess, signature, tag_constants.SERVING, path)
    current_app.logger.debug("ML model loaded via serving signature.")

    return model


def make_prediction(audio_sequence, model=load_ML_model, model_input_dim: str = 8000) -> int:
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

    import tensorflow as tf
    input_tensor = tf.constant(audio_sequence.reshape(1, model_input_dim, 1), dtype=tf.float32)

    # Call the model (which is a SignatureModel wrapper around a TF1 session graph)
    prediction_proba = model(input_tensor)

    # Convert to numpy if needed
    if hasattr(prediction_proba, 'numpy'):
        prediction_proba = prediction_proba.numpy()

    current_app.logger.warning("Taking argmax of prediction probability.")
    prediction = np.argmax(prediction_proba)

    current_app.logger.info("Prediction: %s", prediction)

    return prediction


@views.route("/hello")
def helloworld() -> str:
    return "Hello world !"
