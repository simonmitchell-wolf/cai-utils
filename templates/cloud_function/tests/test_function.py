import flask
from functions_framework import create_app
import pytest

@pytest.fixture
def mock_app():
    app = create_app("session_id_to_param", "session_id_to_param/main.py")
    app.testing = True # bubble exceptions
    yield app

@pytest.fixture
def mock_request_data():
    return {"YOUR DATA": "HERE"}

def test_function(mock_app, mock_request_data):
    client = mock_app.test_client()
    res: flask.response = client.post('/', json=mock_request_data)
    assert res.status_code == 200

# Add function-specific tests