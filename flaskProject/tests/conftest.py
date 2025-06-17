import pytest
from flaskProject import create_app
from ..config import Config

config = Config()

@pytest.fixture
def app():
    app = create_app(config)
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test"
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()
