import re

import functions_framework


@functions_framework.http
def session_id_to_param(request):
    """Webhook will log session id corresponding to request."""

    req = request.get_json()
    # You can read more about SessionInfo at https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/SessionInfo
    # Use a regex pattern to get the session ID
    session_id_regex = r".+\/sessions\/(.+)"
    full_session_id = req["sessionInfo"]["session"]
    regex_match = re.search(session_id_regex, full_session_id)
    session_id = None
    if regex_match is not None:
        session_id = regex_match.group(1)

    # Instead of printing, you could use the logging tools available to you
    print(f"Debug Node: session ID = {session_id}")

    # Return a generic response
    res = {
        "sessionInfo": {
            "parameters": {
                "sessionId": session_id,
            },
        },
    }

    # Returns json
    return res
