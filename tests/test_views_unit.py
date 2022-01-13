import pytest
import os
from src_api import create_app
from src_api.views import backend_file_delete, get_sampling_rate, is_valid_audio_file, load_ML_model, load_audio_sequence
import shutil


flask_app = create_app()


@pytest.mark.parametrize(
    "filename, testfile_path, expected_sr",
    [
        ("one_16000.wav", "testfiles", 16000),
        ("two_22050.wav", "testfiles", 22050),
        ("three_8000.wav", "testfiles", 8000),
        ("three_96000.wav", "testfiles", 96000),
    ],
)
def test_get_sampling_rate(filename: str, testfile_path: str, expected_sr: int) -> bool:
    """
    Tests sampling rate is read correctly
    """
    with flask_app.app_context():
        testfile_path_full = os.path.join(flask_app.config["APP_FOLDER"], "tests", "testfiles")

        assert get_sampling_rate(filename, testfile_path_full) == expected_sr


@pytest.mark.parametrize(
    "filename, testfile_path, dimension",
    [
        ("one_16000.wav", "testfiles", 8000),
        ("two_22050.wav", "testfiles", 8000),
        ("three_8000.wav", "testfiles", 8000),
        ("three_96000.wav", "testfiles", 8000),
    ],
)
def test_load_audio_sequence(filename: str, testfile_path: str, dimension: int) -> bool:
    """
    Checks if the shape of the Output of def load_audio_sequence is (8000,)
    """
    with flask_app.app_context():
        testfile_path_full = os.path.join(flask_app.config["APP_FOLDER"], "tests", "testfiles")
        audio_sequence = load_audio_sequence(filename, testfile_path_full, sampling_rate=8000, max_seq_length=8000)

        assert audio_sequence.shape == (dimension,)


@pytest.mark.parametrize(
    "filename, testfile_path",
    [
        ("one_16000.wav", "testfiles"),
        ("two_22050.wav", "testfiles"),
        ("three_8000.wav", "testfiles"),
        ("three_96000.wav", "testfiles"),
    ],
)
def test_backend_file_delete(filename: str, testfile_path: str) -> bool:
    """
    Makes a copy of a given file, uses the fcn to delete and checks if file was correctly deleted
    """
    with flask_app.app_context():
        copyfile = "copy_" + filename
        testfile_path_full = os.path.join(flask_app.config["APP_FOLDER"], "tests", "testfiles")
        shutil.copyfile(os.path.join(testfile_path_full, filename), os.path.join(testfile_path_full, copyfile))
        backend_file_delete(copyfile, testfile_path_full)

        assert os.path.exists(os.path.join(testfile_path, copyfile)) == 0


@pytest.mark.parametrize(
    "filename, testfile_path, audio_format",
    [
        ("one_16000.wav", "testfiles", True),
        ("two_22050.wav", "testfiles", True),
        (
            "three_8000.wav",
            "testfiles",
            True,
        ),
        (
            "three_96000.wav",
            "testfiles",
            True,
        ),
    ],
)
def test_is_valid_audio_file(filename: str, testfile_path: str, audio_format: bool) -> bool:
    """
    Test if files have an audio wav format
    """
    with flask_app.app_context():
        testfile_path_full = os.path.join(flask_app.config["APP_FOLDER"], "tests", "testfiles")
        assert is_valid_audio_file(filename, testfile_path_full) == audio_format


@pytest.mark.parametrize(
    "TF_version, model_name",
    [
        ("v2.3.0", "functional_1"),
        ("v2.7.0", "model"),
    ],
)
def test_load_ML_model(TF_version: str, model_name: str) -> bool:
    """
    Test if TF model loads correctly
    """
    with flask_app.app_context():
        model_path = "/ML_model/audio_MNIST_v3-TF_" + TF_version + ".tf"
        model = load_ML_model(model_path)

        assert model.name == model_name
