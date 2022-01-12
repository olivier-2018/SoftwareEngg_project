import pytest
from src_api import create_app
from src_api.models import User
from werkzeug.security import generate_password_hash


flask_app = create_app()


@pytest.mark.parametrize(
    "username, email, firstname, lastname, password",
    [
        ("olivier", "olivier@gmail.com", "olivier", "OLIVIER", "olivierolivier"),
        ("angelo", "angelo@gmail.com", "angelo", "ANGELO", "angeloangelo"),
    ],
)
def test_new_user(username, email, firstname, lastname, password) -> bool:
    """
    Test the creation of new users
    """
    with flask_app.app_context():
        user = User(
            user_name=username, email=email, first_name=firstname, last_name=lastname, password=generate_password_hash(password, method="sha256")
        )

        assert user.user_name == username
        assert user.email == email
        assert user.first_name == firstname
        assert user.last_name == lastname
        assert user.password != password


def test_home():
    """
    Test the GET request for route /home returns a status code 200 and some know text
    """
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get("/home")
        assert response.status_code == 200
        assert b"Welcome to the" in response.data

        response = test_client.get("/")
        assert response.status_code == 200
        assert b"Welcome to the" in response.data


def test_about():
    """
    Test the GET request for route /home returns a status code 200 and some know text
    """
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get("/about")
        assert response.status_code == 200
        assert b"Authors:" in response.data
