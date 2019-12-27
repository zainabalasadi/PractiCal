import bcrypt
from flask import Flask, render_template, url_for, request, session, redirect, Blueprint, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import dialogflow_v2
from google.api_core.exceptions import InvalidArgument
import requests

from templates.code.Notification import Notification
from templates.code.PractiCalManager import PractiCalManager
from templates.code.User import User
from templates.code.Calendar import Calendar

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


@index_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
        PCM.logoutUser(current_user.getID())
        logout_user()
        return jsonify({"success": "True"})

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
                desc = r['desc'] if 'desc' in r.keys() else ''
                if (len(r['startDate']) == 16):
                    startDate = (r['startDate'])
                    print("START DATE 16")
                elif (len(r['startDate']) == 24):
                    startDate = (r['startDate'][:-8])
                    print("START DATE 24")
                else:
                    print("fucked")
                if (len(r['endDate']) == 16):
                    endDate = (r['endDate'])
                elif (len(r['endDate']) == 24):
                    endDate = (r['endDate'][:-8])
                cal = current_user.getCalendarByName(r['calendar'])
                category = r['category'] if 'category' in r.keys() else None
                invitees = None
                if 'invitees' in r:
                        invitees = r['invitees'].split()
                groups = None
                if 'groups' in r:
                        groups = r['groups']
                if (cal != None):
                        event = PCM.addEvent(userID=userId, title=name,
                            description=desc, startDateTime=startDate,
                            endDateTime=endDate, calendarName=cal.getName(),
                                             category=category, inviteeEmails=invitees)
                        cal.addEvent(event)
                        eventId = event.getID()
                        return jsonify({"success": "True"})

                return jsonify({"success": "False"})


@index_blueprint.route('/editEvent', methods=['GET', 'POST'])
@login_required
def editEvent():
        if request.method == 'POST':
                r = request.get_json()
                event = PCM.getEventByID(r['eventId'])
                if event is not None:
                        if (event.getName() != r['name']):
                                event.setName(r['name'])
                        if event.getDescription() != r['desc']:
                                event.setDescription(r['desc'])
                        if event.getStartDateTime() != r['startDate']:
                                if (len(r['startDate']) == 16):
                                    event.setStartDateTime(r['startDate'])
                                    print(event.getStartDateTime())
                                elif (len(r['startDate']) == 24):
                                    event.setStartDateTime(r['startDate'][:-8])
                                    print(event.getStartDateTime())
                        if event.getEndDateTime() != r['endDate']:
                                if (len(r['endDate']) == 16):
                                    event.setEndDateTime(r['endDate'])
                                    print(event.getEndDateTime())
                                elif (len(r['endDate']) == 24):
                                    event.setEndDateTime(r['endDate'][:-8])
                                    print(event.getEndDateTime())
                        if event.getCategory() != r['category']:
                                event.setCategory(r['category'])
                        current_user.moveEvent(event, r['calendar'])
                        PCM.addToUpdateQueue(current_user.getID(), event,
                                PCM.DBUpdate.DB_UPDATE_EVENT,
                                current_user.getCalendarByName(r['calendar']))
                        PCM.sendNotification(event.getID(),
                                current_user.getID(), event.getInvitees(),
                                Notification.NOTIF_EVENTCHANGE)
                        print("edited")
                        return jsonify({"success": "True"})

                return jsonify({"success": "False"})


@index_blueprint.route('/deleteEvent', methods=['POST'])
@login_required
def deleteEvent():
        if request.method == 'POST':
                r = request.get_json()
                event = PCM.getEventByID(r['eventId'])
                if event is not None:
                        PCM.deleteEvent(event.getID(), current_user.getID())
                return jsonify({"success": "True"})


@index_blueprint.route('/getEvents', methods=['GET', 'POST'])
@login_required
def getEvents():
        ret = []
        for cal in current_user.getCalendars():
                calObj = {}
                calObj['name'] = cal.getName()
                calObj['colour'] = cal.getColour()
                calObj['user'] = current_user.getFirstName()
                eventList = []
                calEvents = cal.getEvents()
                calInvites = [invite[0] for invite in cal.getInvites(status=Calendar.INVITESTATUS_GOING)]
                for event in calEvents + calInvites:
                        eventDict = {}
                        eventDict['creator'] = event.getUserID()
                        eventDict['title'] = event.getName()
                        eventDict['eventId'] = event.getID()
                        eventDict['desc'] = event.getDescription()
                        eventDict['start'] = str(event.getStartDateTime())
                        eventDict['end'] = str(event.getEndDateTime())
                        eventDict['category'] = event.getCategory()
                        eventDict['comments'] = event.getComments()
                        eventDict['invitees'] = list(event.getInvitees())
                        eventDict['calendar'] = cal.getName()
                        eventDict['groups'] = current_user.getGroups()
                        eventList.append(eventDict)
                calObj['events'] = eventList
                ret.append(calObj)
                # break
        return jsonify({"calendars": ret})



@index_blueprint.route('/searchEvents', methods=['POST'])
@login_required
def searchEvents():
        if request.method == 'POST':
                r = request.get_json()
                eventsByTitle = current_user.getEventsByQuery(r['queryString'])
                eventsByHost = []
                for calendar in current_user.getCalendars():
                        # self._calendar[calendar]
                        for event in calendar.getEvents():
                                userID = event.getUserID()
                                firstName = PCM.getUserInfo(userID=userID)[0]
                                lastName = PCM.getUserInfo(userID=userID)[1]
                                userName = firstName + " " + lastName
                                if r['queryString'].lower() in userName.lower():
                                    eventsByHost.append(event)
                listOfEvents = list(set(eventsByTitle) | set(eventsByHost))
                resultList = []
                for event in listOfEvents:
                        eventDict = {}
                        userID = event.getUserID()
                        firstName = PCM.getUserInfo(userID=userID)[0]
                        lastName = PCM.getUserInfo(userID=userID)[1]
                        eventDict['creator'] = firstName + " " + lastName
                        eventDict['title'] = event.getName()
                        eventDict['eventId'] = event.getID()
                        eventDict['desc'] = event.getDescription()
                        eventDict['start'] = event.getStartDateTime()
                        eventDict['end'] = event.getEndDateTime()
                        eventDict['category'] = event.getCategory()
                        eventDict['comments'] = event.getComments()
                        eventDict['invitees'] = event.getInvitees()
                        # eventDict['groups'] = event.getGroups()
                        resultList.append(eventDict)
                return jsonify(resultList)


@index_blueprint.route('/inviteResponse', methods=['POST'])
@login_required
def respondToInvite():
    if request.method == 'POST':
        r = request.get_json()
        print(r)
        eID = r['id']
        resp = r["response"]
        if resp == "going":
            userResp = Calendar.INVITESTATUS_GOING
            pcmResp = Notification.NOTIF_INVITERESP_GOING
        elif resp == "decline":
            userResp = Calendar.INVITESTATUS_DECLINE
            pcmResp = Calendar.NOTIF_INVITERESP_DECLINE
        current_user.respondToInvite(PCM.getEventByID(eID), userResp)
        PCM.respondToInvite(eID, current_user.getID(), pcmResp)
        return jsonify({"success": "True"})
    return jsonify({"success": "False"})


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
@login_required
def calendar():
        return render_template('/calendar.html', name=current_user.getFirstName())


post_blueprint = Blueprint('post', __name__)


@index_blueprint.route("/getIntent", methods=['GET', 'POST'])
@login_required
def getIntent():
        r = request.get_json()
        textMsg = r['nlpText']
        print(textMsg)

        SESSION_ID = current_user.getID()  # needs to be replaced with the logged in users id
        session = sessionClient.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

        textInput = dialogflow_v2.types.TextInput(text=textMsg,
                                                                                          language_code=DIALOGFLOW_LANGUAGE_CODE)
        queryInput = dialogflow_v2.types.QueryInput(text=textInput)

        response = sessionClient.detect_intent(session=session, query_input=queryInput)
        if response.query_result.intent.display_name == "Event scheduling" or response.query_result.intent.display_name == "Event Scheduling Shorthand":
                print(response.query_result.parameters.fields["date"].string_value + "               " +
                          response.query_result.parameters.fields["timeStart"].string_value + "               " +
                          response.query_result.parameters.fields["timeEnd"].string_value)

                return jsonify({"date": response.query_result.parameters.fields["date"].string_value,
                                                "timeStart": response.query_result.parameters.fields["timeStart"].string_value,
                                                "timeEnd": response.query_result.parameters.fields["timeEnd"].string_value,
                                                "eventName": response.query_result.parameters.fields["eventName"].string_value
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


@index_blueprint.route('/getNotifs', methods=['GET', 'POST'])
@login_required
def getNotifs():
        notifList = []
        # for notif in current_user.getNotifications():
        for notif in current_user.getNotifications():
            sender = PCM.getUserInfo(userEmail=notif.getSenderEmail())
            notifType = notif.getNotifType()
            strType = ""
            senderName = "{} {}".format(sender[0], sender[1])
            eventName = notif.getEvent().getName()
            if notifType == Notification.NOTIF_EVENTCHANGE:
                message = "{sender} has updated the event '{event}'".format(sender=senderName, event=eventName)
                strType = "EVENTCHANGE"
            elif notifType == Notification.NOTIF_EVENTINVITE:
                message = "{sender} has invited you to the event '{event}'".format(sender=senderName, event=eventName)
                strType = "EVENTINVITE"
            elif notifType == Notification.NOTIF_EVENTDELETE:
                message = "{sender} has cancelled the event '{event}'".format(sender=senderName, event=eventName)
                strType = "EVENTDELETE"
            elif notifType == Notification.NOTIF_INVITERESP_GOING:
                message = ("{sender} has changed their status to 'going' "
                           "for event '{event}'").format(sender=senderName, event=eventName)
                strType = "INVITERESP"
            elif notifType == Notification.NOTIF_INVITERESP_MAYBE:
                message = ("{sender} has changed their status to 'maybe' "
                           "for event '{event}'").format(sender=senderName, event=eventName)
                strType = "INVITERESP"
            elif notifType == Notification.NOTIF_INVITERESP_DECLINE:
                message = ("{sender} has changed their status to 'not going' "
                           "for event '{event}'").format(sender=senderName, event=eventName)
                strType = "INVITERESP"
            else:
                continue
            notifObject = {
                'id': notif.getID(),
                'eid': notif.getEvent().getID(),
                'eTitle': notif.getEvent().getName(),
                'eStart': notif.getEvent().getStartDateTime(),
                'eEnd': notif.getEvent().getEndDateTime(),
                'type': strType,
                'message': message
            }
            notifList.append(notifObject)
        return jsonify(notifList)

@index_blueprint.route('/deleteNotif', methods=['POST'])
@login_required
def deleteNotif():
    if request.method == 'POST':
        r = request.get_json()
        current_user.removeNotification(notifID=int(r['id']))
        return jsonify({"success": "True"})
    return jsonify({"success": "False"})

@index_blueprint.route('/getCategoryHours', methods=['GET', 'POST'])
@login_required
def getCategoryHours():
        # return "HI"
        item = (current_user.calculateHoursCategory())
        print(item['Family'])
        print(item["Work"])
        print(item['School'])
        print(item['Social'])
        print(item['Miscellaneous'])

        # if request.method == 'GET':
        return jsonify(item)


@index_blueprint.route('/getName', methods=['GET', 'POST'])
@login_required
def getName():
    return jsonify(current_user.getFirstName())


@index_blueprint.route('/createCalendar', methods=['POST'])
@login_required
def createCalendar():
    if request.method == 'POST':
        r = request.get_json()
        userId = current_user.getID()
        name = r['name']
        colour = r['colour']
        if (current_user.getCalendarByName(name) == None):
            newCalendar = Calendar(name, colour)
            current_user.addCalendar(newCalendar)
            PCM.addToUpdateQueue(userId, current_user, PCM.DBUpdate.DB_UPDATE_USER)
            return jsonify({"success": "True"})
        return jsonify({"success": "False"})


@index_blueprint.route('/deleteCalendar', methods=['POST'])
@login_required
def deleteCalendar():
    if request.method == 'POST':
        r = request.get_json()
        name = r['name']
        calendar = current_user.getCalendarByName(name)
        if calendar is not None:
            for event in calendar.getEvents():
                PCM.deleteEvent(event.getID(), current_user.getID())
            current_user.deleteCalendar(calendar)
            PCM.addToUpdateQueue(current_user.getID(), current_user, PCM.DBUpdate.DB_UPDATE_USER)
            return jsonify({"success": "True"})
    return jsonify({"success": "False"})


@index_blueprint.route('/editCalendar', methods=['POST'])
@login_required
def editCalendar():
    if request.method == 'POST':
        r = request.get_json()
        oldName = r['oldName']
        name = r['name']
        colour = r['colour']
        oldCalendar = current_user.getCalendarByName(oldName)
        if oldCalendar is not None:
            current_user.changeCalendarName(oldCalendar, name)
            current_user.changeCalendarColour(oldCalendar, colour)
            PCM.addToUpdateQueue(current_user.getID(), current_user, PCM.DBUpdate.DB_UPDATE_USER)
            for event in oldCalendar.getEvents():
                PCM.addToUpdateQueue(current_user.getID(), event, PCM.DBUpdate.DB_UPDATE_EVENT, oldCalendar)
            return jsonify({"success": "True"})
    return jsonify({"success": "False"})


@index_blueprint.route('/addContact', methods=['POST'])
@login_required
def addContact():
    if request.method == 'POST':
        r = request.get_json()
        email = r['email']
        name = r['name']
        current_user.addContact(email, name)
        PCM.addToUpdateQueue(current_user.getID(), current_user, PCM.DBUpdate.DB_UPDATE_USER)
        return jsonify({"success": "True"})

@index_blueprint.route('/getContacts', methods=['POST'])
@login_required
def getContacts():
    if request.method == 'POST':
        contacts = current_user.getContacts()
        return jsonify({"data": contacts})
