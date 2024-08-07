# Extract DFCX Session ID to a Session Parameter

> [!WARNING]
> This function is no longer strictly necessary due to the session ID now being available as a [request-scoped parameter](https://cloud.google.com/dialogflow/cx/docs/concept/parameter#request-scoped): `request.session-id`.

> [!NOTE]
> Function should be accessed via a standard Dialogflow webhook as it pulls the session ID from the standard webhook request.

## Functionality

Sets the current Dialogflow session ID (just the UUID, not the whole path string) as a session parameter called `$session.params.sessionId`.

## Problem Solved

The session ID is not exposed directly to the DFCX session logic by default. This can be a problem if one needs to pass the session ID into a CRM ticket, attach it to logging outside of Dialogflow, or communicate it to the user.

## Instructions

Just create a standard webhook to call the function. The session ID value will be stored in session context after the response. A `tag` value is not used for this function.
