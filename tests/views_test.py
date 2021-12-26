from api_src.views import index


def test_index():
    assert index() == "Hello world !"
