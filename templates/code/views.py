from flask import render_template, Blueprint
import requests

index_blueprint = Blueprint('index',__name__)
@index_blueprint.route('/')
@index_blueprint.route('/index')
def index():
 return render_template("index.html")
 
@blueprint.route("/getIntent/", methods=['POST'])
def getIntent():
    textMsg = request.form['message']
    
    url = 'https://dialogflow.googleapis.com/v2/{session=projects/practical-proueq/agent/sessions/defaultsessionid}:detectIntent'
    query = {"queryInput": { "text": textMsg }}
    
    result = requests.post(url, data = query)
    
    mode = result.form['queryResult']['intent']['displayName']
    
    if (mode == "Event scheduling"):
        date = result.form['queryResult']['parameters']['date']
        time = result.form['queryResult']['parameters']['time']
        duration = time + 1
        
    #need event creation functions in pcal manager
    
    return
    
    
@blueprint.route("/createEvent/", methods=['POST'])
def createEvent():
    user = current_user.get_id()
    startTime = request.form['start']
    endTime = request.form['end']
    name =  request.form['name']
    desc = request.form['desc']
    eventId = 1
    
    #need event creation functions in pcal manager
    
    return
