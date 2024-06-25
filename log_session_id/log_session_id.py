import re

import functions_framework


@functions_framework.http
def log_session_id(request):
    """Webhook will log session id corresponding to request."""

    req = request.get_json()
    # You can read more about SessionInfo at https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/SessionInfo
    # Use a regex pattern to get the session ID
    session_id_regex = r".+\/sessions\/(.+)"
    session = req["sessionInfo"]["session"]
    regex_match = re.search(session_id_regex, session)
    session_id = regex_match.group(1)

    # Instead of printing, use the logging tools available to you
    print(f"Debug Node: session ID = {session_id}")

    # Return a generic response
    res = {
        "fulfillment_response": {
            "messages": [{"text": {"text": [f"Request Session ID: {session_id}"]}}]
        },
        "sessionInfo": {
            "parameters": {
                # Set session parameter to None if the form parameter is 'INVALID' and your agent needs to reprompt the user
                "ccaipSessionId": session_id,
            },
        },
    }

    # Returns json
    return res
