from numpy import ndarray, result_type
from src_api.views import *
import shutil
import os

def folder_files_basics():
    """
    Sets the Basic Folder/Files for Testing.

    Returns:
        tuple: filenames and folder.
    """
    folder_name = os.path.join(app.config["APP_FOLDER"], "tests", "testfiles")
    file_name = "test_file.wav"
    file_name_copy = "test_file_copy.wav"
    return folder_name,file_name,file_name_copy


def files_basics_copy():
    """
    Creates Copies of the Files from TestBasics() for Testing.
    
    Returns:
        tuple:  filenames and folder.
    
    """
    folder_name, file_name, file_name_copy = files_basics_copy()
    shutil.copyfile(os.path.join(folder_name,file_name), os.path.join(folder_name,file_name_copy))
    return folder_name,file_name_copy


def test_predict_from_file():
    print()


def test_backend_save_request_object():
    """
    filetype?
    """
    print()


def test_backend_rawfile_load():
    print()
    

def test_backend_file_load():
    print()


def test_get_duration():
    print()


def test_get_sampling_rate():
    """
    Checks if the the Returned Sampling Rate of def_sampling_rate is 8000.
    """
    
    folder_name, file_name_copy = files_basics_copy()
    result = get_sampling_rate(file_name_copy,folder_name)
    assert result == 8000


def test_load_audio_sequence():
    """
    Checks if the shape of the Output of def load_audio_sequence is (8000,)
    """
    
    sampling_rate = 8000
    max_seq_length = 8000
    
    folder_name, file_name_copy = files_basics_copy()
    result = load_audio_sequence(file_name_copy, sampling_rate, max_seq_length, folder_name)
    assert result.shape == (8000,)


def test_play_sound():
    print()


def test_load_ML_model():
    print()


def test_make_prediction():
    print()


def test_backend_file_delete():
    """
    Checks if the file passed to the def backend_file_delete is deleted from the folder at the end.
    The original file is copied for the test and the original file is left inside the 
    original folder after the function has been executed.
    This needs to be the last executed test, which deletes the Testfile. Therefor run tests>pytest -v -W ignore
    """

    folder_name, file_name_copy = files_basics_copy()
    backend_file_delete(file_name_copy,folder_name)
    assert os.path.exists(os.path.join(folder_name, file_name_copy)) == 0
