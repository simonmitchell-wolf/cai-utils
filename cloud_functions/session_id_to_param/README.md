# Extract DFCX Session ID to a Session Parameter

> [!NOTE]
> Function intended to be accessed via a Standard Dialogflow webhook.

## Functionality

Sets the current Dialogflow session ID (just the UUID, not the whole path string) as a session parameter called `$session.params.sessionId`.

## Problem Solved

The session ID is not exposed directly to the DFCX session logic by default. This can be a problem if one needs to pass the session ID into a CRM ticket, attach it to logging outside of Dialogflow, or communicate it to the user.

## Instructions

Just create a standard webhook to call the function. The session ID value will be stored in session context after the response. A `tag` value is not used for this function.