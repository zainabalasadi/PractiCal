from flask import render_template, Blueprint
import dialogflow_v2
from google.api_core.exceptions import InvalidArgument
from protobuf_to_dict import protobuf_to_dict
import requests

DIALOGFLOW_PROJECT_ID = 'practical-proueq'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = 'googlekey.json'
sessionClient = dialogflow_v2.SessionsClient()

index_blueprint = Blueprint('index',__name__)
@index_blueprint.route('/')
@index_blueprint.route('/index')
def index():
 return render_template("index.html")
 
@blueprint.route("/getIntent/", methods=['POST'])
def getIntent():
    textMsg = request.form['message']

    SESSION_ID = "100000"
    session = sessionClient.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    textInput = dialogflow_v2.types.TextInput(text="Make an event for today at 10pm", language_code=DIALOGFLOW_LANGUAGE_CODE)
    queryInput = dialogflow_v2.types.QueryInput(text=textInput)

    response = sessionClient.detect_intent(session=session, query_input=queryInput)
    params = protobuf_to_dict(response.query_result.parameters)
    if (response.query_result.intent.display_name == "Event scheduling"):
        return jsonify(params)
