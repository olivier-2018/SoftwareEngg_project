from src_api.views import *
import pytest


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


def test_sampling_rate():
    print()


def test_audio_sequence():
    print()


def test_backend_file_delete():
    '''
    Checks if the file passed to the function is deleted from the folder at the end.
    The original file is copied for the test and the original file is left inside the 
    original folder after the function has been executed.    
    '''
    import shutil
    folder_name = "..\\tests\\testfiles"
    file_name = "test_file.wav"
    file_name_copy = "test_file_copy.wav"
    shutil.copyfile(f"{folder_name}\{file_name}", f"{folder_name}\{file_name_copy}")
    result = backend_file_delete(file_name_copy,folder_name)
    assert os.path.exists(os.path.join(folder_name, file_name_copy)) == 0


def test_play_sound():
    print()


def test_load_ML_model():
    print()


def test_make_prediction():
    print()


def test_helloworld():
    assert helloworld() == "Hello world !"
