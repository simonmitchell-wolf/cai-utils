"""Function to build CCAI Platform-compatible button payloads."""


def build_ccaip_buttons(request) -> dict:
    """Builds a CCAI Platform-compatible payload to render chat buttons.

    This function takes an HTTP webhook request from Dialogflow CX and
    constructs a payload containing button information. The payload is designed
    to be compatible with the CCAI (Contact Center AI) Platform and will render
    the buttons on the front end without setting an additional payload in
    Dialogflow.

    Args:
        request: A flask.Request received from Dialogflow CX.

    Returns:
        A response dict, parsable by Dialogflow, containing the button
        payload as a fulfillment response.

    Raises:
        - KeyError: If the required parameters are missing from the request.
        - ValueError: If an invalid button type is provided.

    Notes:
        - The function expects the request to have the following parameters:
            - fulfillmentInfo.tag:
                The type of button to be rendered. One of {'inline', 'sticky'}.
            - sessionInfo.parameters.buttonsToBuild:
                A list of either strings or objects/dicts that become buttons.
            - sessionInfo.parameters.buttonsMainTitle:
                The title of the whole button block.
            - sessionInfo.parameters.buttonsTitleTemplate:
                If buttonsToBuild is a list of dicts, a string suitable for use
                with str.format() where the template fields correspond to keys
                in the buttonsToBuild objects.

        - The function iterates over the buttonsToBuild list and constructs a
            button_list containing dictionaries with the button title and
            action.

        - If the button object has a "button_action" key, it will be used as the
            action for the button. Otherwise, the action will be set to
            "quick_reply".

        - The button_type is determined based on the tag parameter. If tag is
            "inline", the button_type will be set to "inline_button". If tag is
            "sticky", the button_type will be set to "sticky_button".

        - The response is constructed as a fulfillmentResponse message with the
            button payload. This means that the buttons will be rendered by the
            front end without having to include an additional payload in the
            Dialogflow UI.

    References:
      - WebhookResponse documentation:
            https://cloud.google.com/dialogflow/cx/docs/reference/rpc/google.cloud.dialogflow.cx.v3#webhookresponse
    """

    # Extract request JSON and important mappings
    request_json: dict = request.get_json()
    fulfillment_info: dict = request_json.get("fulfillmentInfo", {})
    session_info: dict = request_json.get("sessionInfo", {})
    session_params: dict = session_info.get("parameters", {})

    # Extract required parameters from request
    try:
        tag: str = fulfillment_info["tag"]
        main_title: str = session_params["buttonsMainTitle"]
        buttons_data: list[str] | list[dict] = session_params["buttonsToBuild"]
        title_template: str = session_params.get("buttonsTitleTemplate", None)
    except KeyError as exc:
        raise KeyError(f"Missing required parameter: {exc}") from exc

    # Check consistency of buttons data type
    if not is_buttons_data_consistent(buttons_data):
        raise ValueError(
            "Buttons data must be a list of either strings or dictionaries."
        )

    # Build button_list
    button_list: list[dict] = build_button_list(buttons_data, title_template)

    # Determine button_type based on tag
    button_type: str = build_button_type(tag)

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


def is_buttons_data_consistent(buttons_data: list[str] | list[dict]) -> bool:
    """Validates that the buttons data is consistent.
    Args:
        buttons_data: A list of strings or dictionaries representing buttons.
    Returns:
        True if all elements are strings or all elements are dictionaries.
        Otherwise, False.
    """

    data_is_consistent: bool = all(isinstance(obj, str) for obj in buttons_data) or all(
        isinstance(obj, dict) for obj in buttons_data
    )

    return data_is_consistent


def build_button_title(details: str | dict, template: str | None = None) -> str:
    """Builds the title of a button based on details and an optional template.

    Args:
        details:
            The details used to build the button title. It can be either a
            string or a dictionary.
        template (optional):
            The optional template used to format the button title. Defaults to
            None.

    Returns:
        str: The title/label of the button.

    Raises:
        ValueError: If complex details are passed without a template.

    Notes:
        - If the details parameter is a string, it is returned as is since
            buttons can be used as titles.
        - If the template parameter is None, a ValueError is raised as a
            template is required when complex details are passed.
        - The template is formatted using the details dictionary. If any key in
            the template is not found in the details dictionary, a KeyError is
            raised.

    Examples:
        >>> build_button_title("Click me")
        'Click me'

        >>> build_button_title(
            details={"city": "Rome", "state": "GA"},
            template="{city}, {state}"
        )
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


def build_button_list(
    data: list[str] | list[dict], template: str | None = None
) -> list[dict]:
    """Builds a list of button dictionaries based on the data and template.
    Args:
        data: A list of strings or dictionaries representing buttons.
        template (optional): A string suitable for use with str.format().
            Defaults to None.
    Returns:
        A list of dictionaries containing the button title and action.
    """

    button_list: list[dict] = []

    for obj in data:
        button_title: str = build_button_title(details=obj, template=template)

        button_action: str = "quick_reply"
        if isinstance(obj, dict) and "button_action" in obj:
            button_action = obj["button_action"]
        button: dict = {"title": button_title, "action": button_action}
        button_list.append(button)
    return button_list


def build_button_type(tag: str) -> str:
    """Builds the button type based on the tag passed in with the request.
    Args:
        tag: The type of buttons to be rendered.
            One of {'inline','sticky'}.
    Returns:
        The type of button to be rendered.
        One of {'inline_button', 'sticky_button'}.
    Raises:
        ValueError: If an invalid button type is provided.
    """
    if tag == "inline":
        button_type: str = "inline_button"
    elif tag == "sticky":
        button_type = "sticky_button"
    else:
        raise ValueError("Invalid button type. Must be one of {'inline', 'sticky'}.")
    return button_type
