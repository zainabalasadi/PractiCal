import bcrypt
from flask import Flask, render_template, url_for, request, session, redirect, Blueprint, flash, jsonify
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
@login_required
def createEvent():
    if request.method == 'POST':
        r = request.get_json()
        userId = current_user.getID()
        name = r['name']
        desc = r['desc']
        startDate = r['startDate']
        endDate = r['endDate']
        cal = current_user.getCalendarByName("default")
        invitees = None
        if 'invitees' in r:
            invitees = r['invitees']
        groups = None
        if 'groups' in r:
            groups = r['groups']
        if (cal != None):
            event = PCM.addEvent(userId, name, desc, startDate, endDate,
                calendarName=cal.getName())
            cal.addEvent(event)

            return jsonify({"success":"True"})
        
        return jsonify({"success":"False"})

@index_blueprint.route('/editEvent', methods=['POST'])
@login_required
def editEvent():
    if request.method == 'POST':
        r = request.get_json()
        #print(r)
        event = current_user.getEventById(request.form.get('id'))
        if event is not None:
            if (event.getName() != r['eventName']):
                event.setName = r['eventName']
            if (event.getDescription() != r['description']):
                event.setDescription = r['description']
            if (event.getStartDateTime() != r['startDate']):
                event.setStartDateTime = r['startDate']
            if (event.getEndDateTime() != r['endDate']):
                event.setEndDateTime = r['endDate']
            current_user.moveEvent(event, r['calendar'])
            # TODO: Need PCM fn to update db entries
            PCM.addToUpdateQueue(current_user.getID(), event,
                PCM.DBUpdate.DB_UPDATE_EVENT,
                current_user.getCalendarByName(r['calendar']))
            PCM.sendNotification(event.getID(), current_user.getID(),
                event.getInvitees(), Notification.NOTIF_EVENTCHANGE)
            return jsonify({"success": "True"})

        return jsonify({"success": "False"})


@index_blueprint.route('/deleteEvent', methods=['POST'])
@login_required
def deleteEvent():
    if request.method == 'POST':
        r = request.get_json()
        event = current_user.getEventById(r['id'])
        if event:
            # TODO: Need PCM fn to update db entries
            userId = current_user.deleteEvent(event)

        return jsonify({"success": "True"})


@index_blueprint.route('/getEvents', methods=['POST'])
@login_required
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
        return jsonify({"calendars": ret})


@index_blueprint.route('/searchEvents', methods=['POST'])
@login_required
def searchEvents():
        if request.method == 'POST':
                r = request.get_json()
                eventList = []
                for event in current_user.getEventsByQuery(r['queryString']):
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
                return jsonify({"results": eventList})
        
@index_blueprint.route('/inviteResponse', methods=['POST'])
@login_required
def respondToInvite():
    if request.method == 'POST':
        r = request.get_json()
        eID = r['eventID']
        resp = r["response"]
        PCM.respondToInvite(eID, current_user.getID(), resp)
        return jsonify({'success': 'true'})
    return jsonify({'success': 'false'})


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


@index_blueprint.route("/getIntent", methods=['POST'])
@login_required
def getIntent():
    #r = request.get_json()
    textMsg = "Make an event for tomorrow at 9am" #r['message']

    SESSION_ID = 1010 # current_user.getId()  # needs to be replaced with the logged in users id
    session = sessionClient.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    textInput = dialogflow_v2.types.TextInput(text=textMsg,
                                              language_code=DIALOGFLOW_LANGUAGE_CODE)
    queryInput = dialogflow_v2.types.QueryInput(text=textInput)

    response = sessionClient.detect_intent(session=session, query_input=queryInput)

    print(response.query_result.parameters.fields["date"].string_value)
    if response.query_result.intent.display_name == "Event scheduling":
        return jsonify({"date": response.query_result.parameters.fields["date"].string_value,
                        "timeStart": response.query_result.parameters.fields["timeStart"].string_value,
                        "timeEnd": response.query_result.parameters.fields["timeEnd"].string_value
                        })

@index_blueprint.route('/sendInvite', methods=['GET', 'POST'])
@login_required
def sendInvite():
    if request.method == 'POST':
        r = request.get_json()
        eventID = r['eventID']
        sender = current_user.getID()
        invitees = r['invitees']
        PCM.sendInvite(eventID, sender, invitees)
        return jsonify({'success': 'true'})
    return jsonify({'success': 'false'})


@index_blueprint.route('/getNotifs', methods=['POST'])
@login_required
def getNotifs():
    notifList = []
    for notif in current_user.getNotifications():
        notifObj = {}
        notifObj['title'] = notif.getEvent().getTitle()
        notifObj['type'] = notif.getNotifType()
        notifObj['sender'] = notif.getSenderID()
        notifObj['start'] = notif.getEvent().getStartDateTime()

        notifList.append(notifObj)
    return jsonify(notifList)


@index_blueprint.route('/getCategoryHours', methods=['GET', 'POST'])
@login_required
def getCategoryHours():
    if request.method == 'POST':
        category = request.form.get('category')
        week = request.form.get('week')

        return current_user.calculateHoursCategory(category, week)
