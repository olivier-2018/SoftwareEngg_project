import pytest
import sys
sys.path.append('src_api')
from audio_MNIST_api import index

def test_index():
    assert index() == "Hello world !"


