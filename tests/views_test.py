from numpy import ndarray, result_type
from src_api.views import *
import pytest
import shutil
import os

def TestBasics():
    """
    Sets the Basic Folder/Files for Testing.

    Returns:
        tuple: filenames and folder.
    """
    folder_name = os.path.join(app.config["APP_FOLDER"], "tests", "testfiles")
    file_name = "test_file.wav"
    file_name_copy = "test_file_copy.wav"
    return folder_name,file_name,file_name_copy


def TestBasicsCopy(shutil):
    """
    Creates Copies of the Files from TestBasics() for Testing.
    
    Returns:
        tuple:  filenames and folder.
    
    """
    folder_name, file_name, file_name_copy = TestBasics()
    shutil.copyfile(f"{folder_name}\{file_name}", f"{folder_name}\{file_name_copy}")
    return folder_name,file_name_copy


def test_predict_from_file():
    print()


def test_backend_save_request_object():
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
    
    folder_name, file_name_copy = TestBasicsCopy(shutil)
    result = get_sampling_rate(file_name_copy,folder_name)
    assert result == 8000


def test_audio_sequence():
    print()


def test_backend_file_delete():
    """
    Checks if the file passed to the def backend_file_delete is deleted from the folder at the end.
    The original file is copied for the test and the original file is left inside the 
    original folder after the function has been executed.
    """

    folder_name, file_name_copy = TestBasicsCopy(shutil)
    backend_file_delete(file_name_copy,folder_name)
    assert os.path.exists(os.path.join(folder_name, file_name_copy)) == 0


def test_play_sound():
    print()


def test_load_ML_model():
    print()


def test_make_prediction():
    print()


def test_helloworld():
    assert helloworld() == "Hello world !"
