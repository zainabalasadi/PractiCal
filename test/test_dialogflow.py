import dialogflow_v2
from google.api_core.exceptions import InvalidArgument
import requests

DIALOGFLOW_PROJECT_ID = 'practical-proueq'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = './googlekey.json'
SESSION_ID = "100000"
sessionClient = dialogflow_v2.SessionsClient()
session = sessionClient.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)



textInput = dialogflow_v2.types.TextInput(text="Make an event for today at 10pm", language_code=DIALOGFLOW_LANGUAGE_CODE)
queryInput = dialogflow_v2.types.QueryInput(text=textInput)


response = sessionClient.detect_intent(session=session, query_input=queryInput)
print("Detected intent:", response.query_result.parameters.fields)