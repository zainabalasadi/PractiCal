import bcrypt
from flask import Flask, render_template, url_for, request, session, redirect, Blueprint, flash
from flask_login import login_user, logout_user, login_required, current_user
import dialogflow_v2
from google.api_core.exceptions import InvalidArgument
import requests

from templates.code.PractiCalManager import PractiCalManager
from templates.code.User import User

DIALOGFLOW_PROJECT_ID = 'practical-proueq'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = 'googlekey.json'
sessionClient = dialogflow_v2.SessionsClient()

index_blueprint = Blueprint('index', __name__)

PCM = PractiCalManager('practiCal_db', 'localhost', 'admin', 'password')


@index_blueprint.route('/', methods=['GET', 'POST'])
@index_blueprint.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = PCM.loginUser(email, password)

        if not user:
            flash('Please check your login details and try again.')
            return redirect(url_for('index.index'))

        login_user(user, remember=True)
        return redirect(url_for('index.calendar'))

    return render_template('/index.html')

@index_blueprint.route('/logout')
@login_required
def logout():
    PCM.logoutUser(current_user.getID())
    logout_user()
    return redirect(url_for('index.index'))

@index_blueprint.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form.get('email')
        # TODO insert code to send reset password email
        flash('Password reset has been sent to your email.')
        return redirect(url_for('index.index'))

    return render_template('/forgot.html')

@index_blueprint.route('/createEvent', methods=['POST'])
def createEvent():
	if request.method == 'POST':
		userId = current_user.getID()
		name = request.form.get('eventName')
		desc = request.form.get('description')
		startDate = request.form.get('startDate')
		endDate = request.form.get('endDate')
		cal = current_user.getCalendarByName(request.form.get('calendar'))
		invitees = request.form.get('invitees')
		groups = request.form.get('groups')
		if (cal != None):
			event = PCM.addEvent(eventId, currentUser, name, desc, startDate, endDate)
			cal.addEvent(event)

			return jsonify({"success":"True"})
		
		return jsonify({"success":"False"})
	
@index_blueprint.route('/editEvent', methods=['POST'])
def editEvent():
	if request.method == 'POST':
		event = current_user.getEventById(request.form.get('id'))
		if (event != None):
			name = request.form.get('eventName')
			desc = request.form.get('description')
			startDate = request.form.get('startDate')
			endDate = request.form.get('endDate')
			newCalendar = request.form.get('calendar')
			if (current_user.updateEvent(event, name, desc, startDate, endDate, newCalendar) == True):
				return jsonify({"success":"True"})
		
		return jsonify({"success":"False"})

@index_blueprint.route('/deleteEvent', methods=['POST'])
def deleteEvent():
	if request.method == 'POST':
		event = current_user.getEventById(request.form.get('id'))
		if (event != None):
			userId = current_user.deleteEvent(event)
			
		return jsonify({"success":"True"})
	
@index_blueprint.route('/getEvents', methods=['POST'])
def getEvents():
	ret = []
	for cal in current_user.getCalendars():
		calObj = {}
		calObj['name'] = cal.getName()
		calObj['colour'] = cal.getColour()
		calObj['user'] = cal.getUser().firstName()
		eventList = []
		for event in cal.getEvents():
			eventDict = {}
			eventDict['creator'] = event.getUser().firstName()
			eventDict['name'] = event.getName()
			eventDict['eventId'] = event.getID()
			eventDict['description'] = event.getDescription()
			eventDict['startDateTime'] = event.getStartDateTime()
			eventDict['endDateTime'] = event.getEndDateTime()
			eventDict['category'] = event.getCategory()
			eventDict['comments'] = event.getComments()
			eventDict['invitees'] = event.getInvitees()
			eventDict['groups'] = event.getGroups()
			eventList.append(eventDict)
		calObj['events'] = eventList
		ret.append(calObj)
	return jsonify(ret)
		
@index_blueprint.route('/searchEvents', methods=['POST'])
def searchEvents():
	if request.method == 'POST':
		return jsonify(current_user.getEventsByQuery(request.form.get('queryString')))
	

@index_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password')

        # hash user password and then add user to database
        hashpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        if PCM.createUser(firstName, lastName, email, hashpw) is False:
            flash('Email address already exists.')
            return redirect(url_for('index.register'))

        return redirect(url_for('index.index'))

    return render_template('/register.html')

@index_blueprint.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    return render_template('/calendar.html', name=current_user.getFirstName())

post_blueprint = Blueprint('post',__name__)
@post_blueprint.route("/getIntent", methods=['POST'])
def getIntent():
    textMsg = request.form.get['message']

    SESSION_ID = current_user.getId() #needs to be replaced with the logged in users id
    session = sessionClient.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    textInput = dialogflow_v2.types.TextInput(text="Make an event for today at 10pm", language_code=DIALOGFLOW_LANGUAGE_CODE)
    queryInput = dialogflow_v2.types.QueryInput(text=textInput)

    response = sessionClient.detect_intent(session=session, query_input=queryInput)
    if (response.query_result.intent.display_name == "Event scheduling"):
        return jsonify({"date" : response.query_result.parameters.fields["date"].string_value,
                        "timeStart" : response.query_result.parameters.fields["timeStart"].string_value,
                        "timeEnd" : response.query_result.parameters.fields["timeEnd"].string_value
        })


@index_blueprint.route('/sendInvite', methods=['GET', 'POST'])
def sendInvite():
    if request.method == 'POST':
        eventID = request.form('eventID')
        sender = current_user.getID()
        invitees = request.form('invitees')
        PCM.sendInvite(eventID, sender, invitees)

