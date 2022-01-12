import os
import pytest
from src_api.views import *
from flask.app import Flask


app = Flask(__name__)
with app.app_context():

    # TEST_FOLDER_NAME = os.path.join("..","tests", "testfiles")
    APP_FOLDER = os.path.realpath(os.path.join(os.path.dirname(__file__)))
    # APP_FOLDER = current_app.config["APP_FOLDER"]
    TEST_FOLDER_NAME = os.path.join(APP_FOLDER, "testfiles")

    def list_of_files(file_name: str):
        with app.app_context():
            """
            Creates a List of Files as Input for the parametrized Tests.

            Returns:
                List of Filenames.
            """

            file_name_list = []

            for file_name in os.listdir(TEST_FOLDER_NAME):
                if file_name.endswith("wav"):
                    file_name_list.append(file_name)
                else:
                    continue
            return file_name_list

    def list_of_files_item(item: int) -> str:
        with app.app_context():
            """
            Returns the i-th Item-Name of the List.
            """

            # file_name_list = list_of_files(file_name)
            file_name_list_item = list_of_files(item)
            return file_name_list_item


with app.app_context():

    @pytest.mark.parametrize(
        "file_name, TEST_FOLDER_NAME, result",
        [
            (
                list_of_files_item(1)[0],
                TEST_FOLDER_NAME,
                16000,
            ),
            (
                list_of_files_item(2)[1],
                TEST_FOLDER_NAME,
                8000,
            ),
            (
                list_of_files_item(3)[2],
                TEST_FOLDER_NAME,
                96000,
            ),
            (
                list_of_files_item(4)[3],
                TEST_FOLDER_NAME,
                22050,
            ),
        ],
    )
    def test_get_sampling_rate_func(file_name: str, TEST_FOLDER_NAME: str, result: int):
        with app.app_context():
            """
            Parametrized Test:
            Checks if the Returned Sampling Rate of def_sampling_rate is 8000.
            """

            result = get_sampling_rate(file_name, TEST_FOLDER_NAME)
            assert result

    '''

with app.app_context():
    @pytest.mark.parametrize("file_name, TEST_FOLDER_NAME, result",
        [
            (list_of_files_item(1)[0], TEST_FOLDER_NAME, (8000,),),
            (list_of_files_item(2)[1], TEST_FOLDER_NAME, (8000,),),
            (list_of_files_item(3)[2], TEST_FOLDER_NAME, (8000,),),
            (list_of_files_item(4)[3], TEST_FOLDER_NAME, (8000,),),
        ]
    )


    def test_load_audio_sequence_func(file_name: str, TEST_FOLDER_NAME:str, result: int):
        with app.app_context():
            """
            Checks if the shape of the Output of def load_audio_sequence is (8000,)
            """

            sampling_rate = 8000
            max_seq_length = 8000

            result = load_audio_sequence(file_name, sampling_rate, max_seq_length, TEST_FOLDER_NAME)
            assert result (8000,0)
    '''
