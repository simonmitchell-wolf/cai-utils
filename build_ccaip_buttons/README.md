# build_ccaip_buttons.py

## Functionality

Allows for dynamic construction of CCAI Platform-compatible payloads to render chat buttons. Intended to be run as a Cloud Function and called from a standard Dialogflow CX webhook.

This can be helpful for cases when it's desirable to present multiple buttons to a user but the number of buttons is dynamic or dependent on other logic or data. Because custom payloads can't be used in concert with conditional responses, the alternative in these cases in to build out (and maintain) a bunch of conditional routes and/or pages to render any possible number of buttons. This can work but it adds a lot of complexity and overhead.

Another problem area is re-rendering buttons for parameter reprompting. A hardcoded payload has to be recreated in each reprompt route while a webhook call can be configured once and then just recalled in any route in the scope
.
## Instructions

After enabling the webhook on a route in Dialogflow, the tag should be set to "inline" or "sticky" to set the type of button, and a few parameters should also be set as configuration:
- `buttonsToBuild`: array = List of either strings or objects that represent buttons to be built. If strings are passed they'll be the button titles. Button actions default to "quick_reply" unless a "button_action" key is passed in an object in this list.
- `buttonsMainTitle`: str = Main title of the button block
- `buttonsTitleTemplate`: str = A string defining what the button title will be when complex info is passed in the buttonsToBuild array. A simple example is "{name}" if each object in the array has a "name" attribute. Values drawn from the array must be wrapped in curly braces.

Try to null out config parameters after you're done using the webhook.
