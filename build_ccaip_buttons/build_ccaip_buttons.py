"""Cloud Function for building CCAI Platform-compatible payloads to render chat buttons."""

from typing import Union


def build_ccaip_buttons(request):
    """Builds a CCAI Platform-compatible payload to render chat buttons.

    This function takes an HTTP webhook request from Dialogflow CX and constructs a payload
    containing button information. The payload is designed to be compatible with the CCAI
    (Contact Center AI) Platform and will render the buttons on the front end without setting
    an additional payload in Dialogflow.

    Args:
        request (flask.Request):
            The HTTP request object received from Dialogflow CX.

    Returns:
        A response dict, parsable by Dialogflow, containing the button payload as a fulfillment
        response.

    Raises:
        KeyError: If the required parameters are missing from the request.

    Notes:
        - The function expects the request to have the following parameters:
            - fulfillmentInfo.tag:
                The type of button to be rendered. One of {'inline', 'sticky'}.
            - sessionInfo.parameters.buttonsToBuild:
                A list of either strings or objects/dicts that should become buttons.
            - sessionInfo.parameters.buttonsMainTitle:
                The title of the whole button block.
            - sessionInfo.parameters.buttonsTitleTemplate:
                If buttonsToBuild is a list of dicts, a string suitable for use with str.format()
                where the template fields correspond to keys in the buttonsToBuild objects.

        - The function iterates over the buttonsToBuild list and constructs a button_list containing
          dictionaries with the button title and action.

        - If the button object has a "button_action" key, it will be used as the action for the
          button. Otherwise, the action will be set to "quick_reply".

        - The button_type is determined based on the tag parameter. If tag is "inline", the
          button_type will be set to "inline_button". If tag is "sticky", the button_type will be
          set to "sticky_button".

        - The response is constructed as a fulfillmentResponse message with the button payload. This
          means that the buttons will be rendered by the front end without having to include an
          additional payload in the Dialogflow UI.

    References:
        - WebhookResponse documentation:
          https://cloud.google.com/dialogflow/cx/docs/reference/rpc/google.cloud.dialogflow.cx.v3#webhookresponse
    """

    # Extract request JSON and important mappings
    request_json: dict = request.get_json()
    fulfillment_info: dict = request_json.get("fulfillmentInfo", {})
    session_parameters: dict = request_json.get("sessionInfo", {}).get("parameters", {})

    # Extract required parameters from request
    try:
        buttons_type: str = fulfillment_info["tag"]
        main_title: str = session_parameters["buttonsMainTitle"]
        buttons_data: list[str] | list[dict] = session_parameters["buttonsToBuild"]
        title_template: str = session_parameters.get("buttonsTitleTemplate", None)
    except KeyError as exc:
        raise KeyError(f"Missing required parameter: {exc}") from exc
    if title_template is None and any(isinstance(obj, dict) for obj in buttons_data):
        raise KeyError("Template is required when complex details are passed.")

    # Initialize button_list
    button_list: list[dict] = []

    # Iterate over buttonsToBuild and construct button_list
    for obj in buttons_data:

        button_title: str = build_button_title(details=obj, template=title_template)

        if isinstance(obj, dict) and "button_action" in obj:
            button_list.append({"title": button_title, "action": obj["button_action"]})
            continue

        button_list.append({"title": button_title, "action": "quick_reply"})

    # Determine button_type based on tag
    if buttons_type == "inline":
        button_type: str = "inline_button"
    elif buttons_type == "sticky":
        button_type = "sticky_button"
    else:
        raise ValueError("Invalid button type. Must be one of {'inline', 'sticky'}.")

    # Construct response payload
    response: dict = {
        "fulfillmentResponse": {
            "messages": [
                {
                    "payload": {
                        "ujet": {
                            "type": button_type,
                            "title": main_title,
                            "buttons": button_list,
                        }
                    }
                }
            ]
        }
    }

    # Return response as JSON
    return response


def build_button_title(
    details: Union[str, dict], template: Union[str, None] = None
) -> str:
    """Builds the title of a button based on details and an optional template.

    Args:
        details (Union[str, dict]):
            The details used to build the button title. It can be either a string
            or a dictionary.
        template (Union[str, None], optional):
            The optional template used to format the button title. Defaults to None.

    Returns:
        str: The title/label of the button.

    Raises:
        ValueError: If complex details are passed without a template.

    Note:
        - If the details parameter is a string, it is returned as is since buttons can
          be used as titles.
        - If the template parameter is None, a ValueError is raised as a template is
          required when complex details are passed.
        - The template is formatted using the details dictionary. If any key in the
          template is not found in the details dictionary, a KeyError is raised.

    Examples:
        >>> build_button_title("Click me")
        'Click me'

        >>> build_button_title({"city": "Atlanta", "state": "GA"}, "{city}, {state}")
        'Atlanta, GA'
    """

    title: str = ""

    # Bare strings are passed as buttons are used as the titles
    if isinstance(details, str):
        return details

    if template is None and isinstance(details, dict):
        raise ValueError("Template is required when complex details are passed.")

    # Process template
    try:
        title = template.format(**details)
    except KeyError as exc:
        raise KeyError("Template key not found in details dictionary.") from exc

    return title
