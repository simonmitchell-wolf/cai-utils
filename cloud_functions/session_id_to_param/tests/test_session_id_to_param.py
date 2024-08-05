import flask
from session_id_to_param.main import session_id_to_param # type: ignore
from functions_framework import create_app
import pytest

@pytest.fixture
def mock_app():
    app = create_app("session_id_to_param", "session_id_to_param/main.py")
    app.testing = True # bubble exceptions
    yield app

@pytest.fixture
def mock_full_session_id():
    return "projects/123456/locations/global/agents/123456/flows/123456/sessions/123456"

@pytest.fixture
def mock_request_data(mock_full_session_id):
    return {
        "fulfillmentInfo": {"tag": "string"},
        "sessionInfo": {
            "session": mock_full_session_id,
        }
    }

def test_function(mock_app, mock_request_data):
    client = mock_app.test_client()
    res: flask.response = client.post('/', json=mock_request_data)
    assert res.status_code == 200

def test_build_ccaip_buttons(mock_app, mock_request_data):
    with mock_app.test_request_context(json=mock_request_data):
        response = session_id_to_param(flask.request)
        assert isinstance(response, dict)
        assert "sessionInfo" in response
        assert "parameters" in response["sessionInfo"]
        assert "sessionId" in response["sessionInfo"]["parameters"]
        assert response["sessionInfo"]["parameters"]["sessionId"] == "123456"