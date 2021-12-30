from src_api.views import helloworld


def test_helloworld():
    assert helloworld() == "Hello world !"
