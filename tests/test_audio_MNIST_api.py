import pytest
import sys
sys.path.append('api_src')
from audio_MNIST_api import index

def test_index():
    assert index() == "Hello world !"


