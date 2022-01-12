import pytest
import os
from src_api import create_app
from src_api.views import load_audio_sequence, make_prediction, load_ML_model
import tensorflow as tf


flask_app = create_app()


@pytest.mark.xfail
@pytest.mark.skipif(tf.__version__ != "2.7.0", reason="Tensorflow v2.7.0 only available with pip (not conda)")
@pytest.mark.parametrize(
    "filename, testfile_path, model_prediction",
    [
        ("one_16000.wav", "testfiles", 1),
        ("two_22050.wav", "testfiles", 2),
        (
            "three_8000.wav",
            "testfiles",
            3,
        ),
        (
            "three_96000.wav",
            "testfiles",
            3,
        ),
    ],
)
def test_load_ML_model_1(filename: str, testfile_path: str, model_prediction: int) -> bool:
    """
    Test if model prediction is correct
    """
    with flask_app.app_context():
        model_path = "/ML_model/audio_MNIST_v3-TF_v2.7.0.tf"
        model = load_ML_model(model_path)
        testfile_path_full = os.path.join(flask_app.config["APP_FOLDER"], "tests", "testfiles")
        audio_sequence = load_audio_sequence(filename, testfile_path_full, sampling_rate=8000, max_seq_length=8000)
        prediction = make_prediction(model, audio_sequence, model_input_dim=8000)

        assert prediction == model_prediction


@pytest.mark.xfail
@pytest.mark.skipif(tf.__version__ != "2.3.0", reason="Tensorflow v2.3.0 only available with conda")
@pytest.mark.parametrize(
    "filename, testfile_path, model_prediction",
    [
        ("one_16000.wav", "testfiles", 1),
        ("two_22050.wav", "testfiles", 2),
        (
            "three_8000.wav",
            "testfiles",
            3,
        ),
        (
            "three_96000.wav",
            "testfiles",
            3,
        ),
    ],
)
def test_load_ML_model_2(filename: str, testfile_path: str, model_prediction: int) -> bool:
    """
    Test if model prediction is correct
    """
    with flask_app.app_context():
        model_path = "/ML_model/audio_MNIST_v3-TF_v2.3.0.tf"
        model = load_ML_model(model_path)
        testfile_path_full = os.path.join(flask_app.config["APP_FOLDER"], "tests", "testfiles")
        audio_sequence = load_audio_sequence(filename, testfile_path_full, sampling_rate=8000, max_seq_length=8000)
        prediction = make_prediction(model, audio_sequence, model_input_dim=8000)

        assert prediction == model_prediction
