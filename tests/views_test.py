from re import sub
from src_api.views import *
import shutil
import os
from tests.test_views import list_of_files, list_of_files_item


TEST_FOLDER_NAME = os.path.join(app.config["APP_FOLDER"], "tests", "testfiles")


def folder_files_basics(file_name: str):
    """
    Sets the Basic Filename for Testing.

    Returns:
        String: Filename.
    """

    file_name_copy = f"copy_of_{file_name}"
    return file_name_copy


def files_basics_copy(file_name: str):
    """
    Copies the Files from TestBasics() for Testing.
    
    Returns:
        None.
    """

    file_name_copy = folder_files_basics(file_name)
    shutil.copyfile(os.path.join(TEST_FOLDER_NAME,file_name), os.path.join(TEST_FOLDER_NAME,file_name_copy))
    return file_name_copy


for file_name in os.listdir(TEST_FOLDER_NAME):

    i = 1
    if file_name.endswith("wav"):

        def test_get_sampling_rate():
            """
            Checks if the the Returned Sampling Rate of def_sampling_rate corresponds to the one recorded.
            Example: "one_16000.wav" has sampling rate of 16000.
            """
            file_name_list_item = list_of_files_item(i)[0]
            result = get_sampling_rate(file_name_list_item,TEST_FOLDER_NAME)
            assert result == int(file_name_list_item[file_name_list_item.find("_")+1:-4])
    else:
    
        continue
    i = 1 + 1


def test_load_audio_sequence():
    """
    Checks if the shape of the Output of def load_audio_sequence is (8000,)
    """
    
    sampling_rate = 8000
    max_seq_length = 8000
    
    result = load_audio_sequence(list_of_files_item(1)[0], sampling_rate, max_seq_length, TEST_FOLDER_NAME)
    assert result.shape == (8000,)



def test_backend_file_delete():
    """
    Checks if the file passed to the def backend_file_delete is deleted from the folder at the end.
    The original file is copied for the test and the original file is left inside the 
    original folder after the function has been executed.
    """

    for file_name in os.listdir(TEST_FOLDER_NAME):
        if file_name.endswith("wav"):
            file_name_copy = files_basics_copy(file_name)
            backend_file_delete(file_name_copy,TEST_FOLDER_NAME)
            assert os.path.exists(os.path.join(TEST_FOLDER_NAME, file_name_copy)) == 0
        else:
            continue
    return None
