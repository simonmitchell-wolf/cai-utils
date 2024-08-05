# build_ccaip_buttons.py

> [!NOTE]
> Function should be accessed via a standard Dialogflow webhook uses the standard webhook response functionality to create a fulfillment message.

## Functionality

Allows for dynamic construction of CCAI Platform-compatible payloads to render chat buttons. Intended to be run as a Cloud Function and called from a standard Dialogflow CX webhook. **Function returns a fulfillment message, so it will directly render the buttons without requiring an additional payload to be set in Dialogflow.**

## Problems Solved

1. This can be helpful for cases when it's desirable to present multiple buttons to a user but the number of buttons is dynamic or dependent on other logic or data. Because custom payloads can't be used in concert with conditional responses, the alternative in these cases in to build out (and maintain) a bunch of conditional routes and/or pages to render any possible number of buttons. This can work but it adds a lot of complexity and overhead.

2. Another problem area is re-rendering buttons for parameter reprompting. A hardcoded payload has to be recreated in each reprompt route while a webhook call can be configured once and then just recalled in any route in the scope.

## Instructions
Basic use case in Dialogflow is to set the configuration parameters (see below) in either the initial prompt route of a parameter (if focusing only on entity extraction) or the initial fulfillment of a page (if looking for full intent input). Then enable the webhook wherever you want the buttons and set the `tag` value based on the desired button type. Importantly, it's best to try and null out the config parameters after you're done using the webhook, which is likely on every outgoing route from the page _unless_ you want to intentionally redisplay the same buttons elsewhere.

After enabling the webhook on a route, the tag should be set to "inline" or "sticky" to set the type of button, and a few parameters should also be set as configuration:
- `buttonsToBuild`: array = List of either strings or objects that represent buttons to be built. If strings are passed they'll be the button titles. Button actions default to "quick_reply" unless a "button_action" key is passed in an object in this list.
- `buttonsMainTitle`: str = Main title of the button block
- `buttonsTitleTemplate`: str = A string defining what the button title will be when complex info is passed in the buttonsToBuild array. A simple example is "{name}" if each object in the array has a "name" attribute. Values drawn from the array must be wrapped in curly braces.

## Limitations

- Currently hardcoded to CCAI-P button payloads, though it would be easy enough to modify.
- Treats every button the same in terms of labeling. Can handle buttons with different actions by passing in `button_action` key in the list objects, but can't really add a different "Escalate" button on the end at the moment, for example.

## Examples

### Simple text buttons

1. Set configuration
   - `buttonsToBuild` = ["Oranges", "Tomatoes", "Tortillas"]
   - `buttonsMainTitle` = "Pick a fruit:"
   - `buttonsTitleTemplate` = ""
2. Enable webhook
3. Set tag to "inline"
4. Button payload looks like:

```json
{
    "ujet": {
        "type": "inline_button",
        "title": "Pick a fruit:",
        "buttons": [
            {
                "title": "Oranges",
                "action": "quick_reply"
            },
            {
                "title": "Tomatoes",
                "action": "quick_reply"
            },
            {
                "title": "Tortillas",
                "action": "quick_reply"
            }
        ]
    }
}
```

### Buttons from more complex list

1. Set configuration
   - `buttonsToBuild` = [{"name": "Jeff", "city": "Townsville"}, {"name": "Tristán", "city": "Trenton"}, {"name": "Ayesha", "city": Cityburg"}]
   - `buttonsMainTitle` = "Who would you like to meet?"
   - `buttonsTitleTemplate` = "{name} in {city}"
2. Enable webhook
3. Set tag to "inline"
4. Button payload looks like:

```json
{
    "ujet": {
        "type": "inline_button",
        "title": "Who would you like to meet?",
        "buttons": [
            {
                "title": "Jeff in Townsville",
                "action": "quick_reply"
            },
            {
                "title": "Tristán in Trenton",
                "action": "quick_reply"
            },
            {
                "title": "Ayesha in Cityburg",
                "action": "quick_reply"
            }
        ]
    }
}
```
