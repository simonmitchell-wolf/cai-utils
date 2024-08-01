import flask
from functions_framework import create_app
import pytest
from build_ccaip_buttons.main import (
    build_ccaip_buttons,
    is_buttons_data_consistent,
    build_button_title,
    build_button_list,
    build_button_type,
)

@pytest.fixture
def test_app():
    app = create_app("build_ccaip_buttons", "build_ccaip_buttons/main.py")
    app.testing = True # bubble exceptions
    yield app

@pytest.fixture
def test_request_data():
    return {
        "fulfillmentInfo": {"tag": "inline"},
        "sessionInfo": {
            "parameters": {
                "buttonsMainTitle": "Main Title",
                "buttonsToBuild": ["Button 1", "Button 2"],
                "buttonsTitleTemplate": None,
            }
        }
    }

def test_function(test_app, test_request_data):
    client = test_app.test_client()
    res: flask.response = client.post('/', json=test_request_data)
    assert res.status_code == 200

def test_build_ccaip_buttons(test_app, test_request_data):
    with test_app.test_request_context(json=test_request_data):
        response = build_ccaip_buttons(flask.request)
        assert isinstance(response, dict)
        assert "fulfillmentResponse" in response
        assert "messages" in response["fulfillmentResponse"]
        assert len(response["fulfillmentResponse"]["messages"]) == 1
        assert "payload" in response["fulfillmentResponse"]["messages"][0]
        assert "ujet" in response["fulfillmentResponse"]["messages"][0]["payload"]
        assert "type" in response["fulfillmentResponse"]["messages"][0]["payload"]["ujet"]
        assert "title" in response["fulfillmentResponse"]["messages"][0]["payload"]["ujet"]
        assert (
            "buttons" in response["fulfillmentResponse"]["messages"][0]["payload"]["ujet"]
        )


def test_is_buttons_data_consistent():
    assert is_buttons_data_consistent(["Button 1", "Button 2"])
    assert (
        is_buttons_data_consistent([{"title": "Button 1"}, {"title": "Button 2"}])
    )
    assert not is_buttons_data_consistent(["Button 1", {"title": "Button 2"}]) # type: ignore[arg-type]


def test_build_button_title():
    assert build_button_title("Click me") == "Click me"
    assert (
        build_button_title({"city": "Rome", "state": "GA"}, "{city}, {state}")
        == "Rome, GA"
    )
    with pytest.raises(ValueError):
        build_button_title({"city": "Rome", "state": "GA"})


def test_build_button_list_simple():
    data = ["Button 1", "Button 2"]
    template = None
    button_list = build_button_list(data, template)
    assert len(button_list) == 2
    assert button_list[0]["title"] == "Button 1"
    assert button_list[0]["action"] == "quick_reply"
    assert button_list[1]["title"] == "Button 2"
    assert button_list[1]["action"] == "quick_reply"

def test_build_button_list_complex():
    data = [
        {"title": "Button 1"},
        {"title": "Button 2", "button_action": "custom_action"},
    ]
    template = "{title}"
    button_list = build_button_list(data, template)
    assert len(button_list) == 2
    assert button_list[0]["title"] == "Button 1"
    assert button_list[0]["action"] == "quick_reply"
    assert button_list[1]["title"] == "Button 2"
    assert button_list[1]["action"] == "custom_action"


def test_build_button_type():
    assert build_button_type("inline") == "inline_button"
    assert build_button_type("sticky") == "sticky_button"
    with pytest.raises(ValueError):
        build_button_type("invalid_type")
