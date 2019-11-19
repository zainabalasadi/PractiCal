# Implementation of PractiCalManager class
# Completed by Michael Ho
# Started 15/10/19
# Edited by Egene Oletu
# Last modified 13/11/19

from templates.code.Calendar import Calendar
from templates.code.Comment import Comment
from templates.code.Event import Event
from templates.code.Group import Group
from templates.code.Notification import Notification
from templates.code.User import User
from templates.code.DatabaseManager import DatabaseManager
import json

class PractiCalManager():
    def __init__(self, database, host, user, password):
        self._users = dict()
        self._events = dict()
        self._db = DatabaseManager(database, host, user, password)
        self._updateQueue = dict()

    class DBUpdate():
        DB_UPDATE_EVENT = 0
        DB_UPDATE_USER = 1
        DB_UPDATE_INVITE_GOING = 2
        DB_UPDATE_INVITE_MAYBE = 3
        DB_UPDATE_INVITE_DECLINE = 4
        DB_DELETE_EVENT = 5
        DB_DELETE_USER = 6

        def __init__(self, userID, obj, calendar, updateType):
            self._userID = userID
            self._obj = obj
            self._calendar = calendar
            self._updateType = updateType

        def getUserID(self):
            return self._userID

        def getObject(self):
            return self._obj

        def getCalendar(self):
            return self._calendar

        def getUpdateType(self):
            return self._updateType

    # Returns user object if logged in
    def getUserByID(self, userID):
        uid = int(userID)
        if uid in self._users.keys():
            return self._users[uid]
        return None

    def getEventByID(self, eventID):
        eid = int(eventID)
        if eid in self._events.keys():
            return self._events[eid]
        return None

    def getUserDetails(self, userID=None, userEmail=None):
        if not userID and not userEmail: return None
        _, fn, ln, email, _ = self.getUser(userID, userEmail)
        return (fn, ln, email)

    # Returns tuple containing user information in the form
    # (first name, last name, email)
    def getUserInfo(self, userID=None, email=None):
        if userID and email: return None
        user = self._db.getUser(userID=userID) if userID else \
            self._db.getUser(email=email)
        return tuple(user[1:]) if user else None

    # Returns true if new user is successfully created
    def createUser(self, firstName, lastName, email, password):
        userID = self._db.addUser(firstName, lastName, email, password)
        if userID != -1:
            newUser = User(userID, firstName, lastName, email, password)
            return True
        else:
            return False

    # Search database for users with name or email partial or full matches
    # to query string
    def searchUser(self, query):
        return self._db.searchUser(query)

    # Logs user into system
    #TODO: read calendar colour from settings
    def loginUser(self, email, password):
        # Get user from database and load into manager
        # Return None is user doesnt exist
        userID = self._db.checkUserCred(email, password, use_bcrypt=True)
        if not userID > 0:
            return None
        try:
            _, userFN, userLN, email, contacts, prefs = \
                self._db.getUser(userID=userID)
        except:
            return None

        # Load preferences
        prefs = json.loads(prefs) if prefs else None
        user = User(userID, userFN, userLN, email, password, prefs)
        prefs = user.getPreferences()
        self._users[userID] = user

        # Add contacts to users
        try:
            contacts = json.loads(contacts)
            for email in contacts.keys():
                _, contactFN, contactLN, _ = self._db.getUser(email=email)
                for group in contacts[email]:
                    user.addContact(email, contactFN, contactLN, group)
        except:
            pass


        # Get events from database
        events = self._db.getUserEvents(userID)
        if events == -1 or not events: events = []

        calendars = {cal.getName(): cal for cal in user.getCalendars()}
        for e in events:
            eventID = e[0]
            cal = e[6]
            # Load calendar if not already loaded
            if cal not in calendars.keys():
                calendars[cal] = Calendar(cal, prefs['default_colour'])

            # Load event
            if eventID not in self._events.keys():
                if not self.loadEvent(eventID): continue
            calendars[cal].addEvent(self._events[eventID])

        # Load invites
        invites = self._db.getInvitesByUser(userID)
        if invites == -1 or not invites: invites = []

        for i in invites:
            eventID, _, status, cal = i
            if eventID not in self._events.keys():
                eventID = e[0]
                cal = e[6]
                # Load calendar if not already loaded
                if cal not in calendars.keys():
                    calendars[cal] = Calendar(cal, prefs['default_colour'])

                # Load event
                if eventID not in self._events.keys():
                    if not self.loadEvent(eventID): continue
                calendars[cal].addInvite(self._events[eventID], status)

        # Get notifications from database
        notifs = self._db.getNotifications(userID)
        if notifs == -1 or not notifs: notifs = []

        for n in notifs:
            eventID, senderID, notifType = n
            # Load event if not already loaded
            if eventID not in self._events.keys():
                if not self.loadEvent(eventID): continue

            senderEmail = ""
            if senderID in self._users.keys():
                senderEmail = self._users[senderID].getEmail()
            else:
                sender = self._db.getUser(userID=senderID)
                if sender and sender != -1: senderEmail = sender[3]

            if senderEmail:
                user.addNotification(Notification(event=self._events[eventID],
                    notifType=notifType, senderEmail=senderEmail))

            # Delete notification from database
            self._db.deleteNotification(eventID, senderID, userID, notifType)

        for c in calendars.values():
            user.addCalendar(c)

        user.setAuthenticated()
        return user

    # Logs user out of system
    # TODO: remove user events from system that arent used by other users (invitees)
    # TODO: garbage cleanup
    def logoutUser(self, userID):
        if userID not in self._users.keys():
            return False
        self._users[userID].setAuthenticated(False)

        # Save notifications to database
        for notif in self._users[userID].getNotifications():
            sender = self._db.getUser(email=notif.getSenderEmail())
            if not sender or sender == -1: continue

            self._db.addNotification(notif.getEvent().getID(),
                sender[0], userID, notif.getNotifType())

        del self._users[userID]

        if userID in self._updateQueue.keys():
            self.updateDatabase(self._updateQueue[userID])
            del self._updateQueue[userID]

        return True

    # Add a new event to manager and database. Returns new event object
    def addEvent(self, userID, title, startDateTime, description=None,
            endDateTime=None, calendarName=None , category=None, location=None,
            inviteeEmails=None):

        eventID = self._db.addEvent(userID, title, description, calendarName,
            category, startDateTime, endDateTime, location)
        if eventID == -1: return None

        event = Event(eventID, userID, title, description, startDateTime,
            endDateTime, category, location)
        self._events[eventID] = event
        if inviteeEmails:
            self.sendInvite(eventID, userID, inviteeEmails)
        return event

    # Load event into manager if not already loaded
    def loadEvent(self, eventID):
        if eventID not in self._events.keys():
            event = self._db.getEvent(eventID)
            if not event or event == -1: return False
            eventID, userID, title, descr, startDT, endDT, _, cat, loc = event

            # Get event invitees
            invites = self._db.getInvitesByEvent(eventID)
            if invites == -1 or not invites: invites = []
            invitees = dict()
            for i in invites:
                _, inviteeID, status = i
                _, _, _, inviteeEmail = self._getUser(userID=inviteeID)
                invitees[inviteeEmail] = status

            self._events[eventID] = Event(
                eventID=eventID,
                userID=userID,
                name=title,
                description=descr,
                startDateTime=startDT,
                endDateTime=endDT,
                category=cat,
                location=loc,
                invitees=invitees)
            return True
        return False

    # Delete event from system and remove it from invited users accounts
    def deleteEvent(self, eventID, userID):
        # Check event is in system
        if eventID not in self._events.keys(): return False

        # Check user is the owner of the event
        event = self._events[eventID]
        if userID != event.getUserID(): return False

        # Remove invite from invitees calendars if theyre logged in, else
        # remove invite from database
        inviteeIDs = [self._db.getUser(email=invitee)[0] for invitee in \
                event.getInvitees()]
        for invitee in inviteeIDs:
            if invitee in self._users.keys():
                self._users[invitee].removeInvite(event)
            else:
                self._db.deleteInvite(eventID, invitee)

        self.sendNotification(eventID, userID, event.getInvitees(),
            Notification.NOTIF_EVENTDELETE)
        self._db.deleteEvent(eventID)
        del self._events[eventID]
        return True

    # Sends event invites to list of users if event exists in manager
    def sendInvite(self, eventID, senderID, receiverEmails, checkExisting=True):
        # Check receiverEmails not empty
        if not receiverEmails: return

        # Check event is loaded
        if eventID not in self._events.keys(): return
        event = self._events[eventID]

        # Check sender is logged in and owner of event
        if not (senderID in self._users.keys() and \
                senderID == event.getUserID()):
            return

        emailsToNotify = receiverEmails
        existingInvitees = self._events[eventID].getInvitees()
        for email in receiverEmails:
            # Check user exists
            user = self._db.getUser(email=email)
            receiverID = user[0] if user and user != -1 else -1
            if not receiverID > 0:
                emailsToNotify.remove(email)
                continue
            if checkExisting and email in existingInvitees:
                emailsToNotify.remove(email)
                continue

            # Send invite to user if logged in else send to database
            if receiverID in self._users.keys():
                self._users[receiverID].addInvite(self._events[eventID])
            else:
                self._db.addInvite(eventID, receiverID, Event.INVITESTATUS_NONE)
            self._events[eventID].addInvitees([email])

        self.sendNotification(eventID, senderID, emailsToNotify,
            Notification.NOTIF_EVENTINVITE)

    # Updates invite status for user and sends response notification to
    # event owner
    def respondToInvite(self, eventID, userID, response):
        # Check event loaded
        if eventID not in self._events.keys(): return
        # Check user is logged in
        if userID not in self._users.keys(): return
        # Check user was invited to event
        userEmail = self._users[userID].getEmail()
        if userEmail not in self._events[eventID].getInvitees(): return
        # Check response is valid
        if response != Notification.NOTIF_INVITERESP_GOING and \
                response != Notification.NOTIF_INVITERESP_MAYBE and \
                response != Notification.NOTIF_INVITERESP_DECLINE:
            return

        eventOwnerID = self._events[eventID].getUserID()
        eventOwnerEmail = ""
        if eventOwnerID in self._users.keys():
            eventOwner = self._users[eventOwnerID]
            eventOwnerEmail = eventOwner.getEmail()
            event = self._events[eventID]
            # Remove old response notification if there is one
            for notif in eventOwner.getNotifications():
                if notif.getEvent() == event and notif.getSenderID() == userID:
                    eventOwner.removeNotification(notif)
                    break
        else:
            # Remove any old responses
            eventOwner = self._db.getUser(userID=eventOwnerID)
            if eventOwner and eventOwner != -1: eventOwnerEmail = eventOwner[3]
            self._db.deleteNotification(eventID, userID, eventOwnerID,
                Notification.NOTIF_INVITERESP_GOING)
            self._db.deleteNotification(eventID, userID, eventOwnerID,
                Notification.NOTIF_INVITERESP_MAYBE)
            self._db.deleteNotification(eventID, userID, eventOwnerID,
                Notification.NOTIF_INVITERESP_DECLINE)

        # Send notification to event owner
        if eventOwnerEmail:
            self.sendNotification(eventID, userID, [eventOwnerEmail], response)

    # Sends notification to list of users
    def sendNotification(self, eventID, senderID, receiverEmails, notifType):
        # Check event loaded
        if eventID not in self._events.keys(): return
        # Check sender logged in
        if senderID not in self._users.keys(): return
        # Check response is valid
        if not (notifType >= Notification.NOTIF_EVENTCHANGE and \
                notifType <= Notification.NOTIF_INVITERESP_NONE):
            return

        event = self._events[eventID]
        for email in receiverEmails:
            receiver = self._db.getUser(email=email)
            receiverID = receiver[0] if receiver and receiver != -1 else 0
            if not receiverID > 0: continue

            # Send notification to user if logged in else save to database
            if receiverID in self._users.keys():
                self._users[receiverID].addNotification(
                    Notification(event, notifType, senderID))
            else:
                self._db.addNotification(eventID, senderID, receiverID,
                    notifType)


    # Adds object to queue of database updates to be done once user has
    # logged out. Add calendar object if object is an event
    def addToUpdateQueue(self, userID, obj, updateType, calendar=None):
        # Check user logged in
        if userID not in self._users.keys(): return
        # If user object, check userID matches id in the object
        if type(obj) == User and userID != obj.getID(): return
        # If modifying or deleting event object, check user is the owner
        if (updateType == self.DBUpdate.DB_UPDATE_EVENT or \
            updateType == self.DBUpdate.DB_DELETE_EVENT) and \
            type(obj) == Event and userID != obj.getUserID(): return
        # Check updateType is valid
        if updateType < self.DBUpdate.DB_UPDATE_EVENT or\
                updateType > self.DBUpdate.DB_DELETE_USER: return

        if userID not in self._updateQueue.keys():
            self._updateQueue[userID] = []

        inviteTypes = [self.DBUpdate.DB_UPDATE_INVITE_GOING,
            self.DBUpdate.DB_UPDATE_INVITE_MAYBE,
            self.DBUpdate.DB_UPDATE_INVITE_DECLINE]

        # Check if update for same object in queue already. If so delete it
        for exUpdate in self._updateQueue[userID]:
            if exUpdate.getObject() == obj:
                exType = exUpdate.getUpdateType()
                # Remove existing update if it and new update are invite
                # updates or if both arent invite updates
                if (updateType in inviteTypes and exType in inviteTypes) or \
                        (exType not in inviteTypes and updateType not in \
                        inviteTypes):
                    self._updateQueue[userID].remove(exUpdate)

        self._updateQueue[userID].append(self.DBUpdate(userID, obj, calendar,
            updateType))

    # Applies changes to database corresponding to list of objects given
    def updateDatabase(self, updates):
        try:
            for update in updates:
                updateType = update.getUpdateType()
                updateObject = update.getObject()

                if updateType == self.DBUpdate.DB_UPDATE_EVENT:
                    self._db.setEvent(
                        updateObject.getID(),
                        updateObject.getName(),
                        updateObject.getDescription(),
                        updateObject.getStartDateTime(),
                        updateObject.getEndDateTime(),
                        update.getCalendar().getName(),
                        updateObject.getCategory(),
                        updateObject.getLocation())
                elif updateType == self.DBUpdate.DB_UPDATE_USER:
                    contacts = {email: groups for email, _, _, groups \
                            in updateObject.getContacts()}
                    self._db.setUser(
                        updateObject.getID(),
                        updateObject.getFirstName(),
                        updateObject.getLastName(),
                        updateObject.getEmail(),
                        updateObject.getPassword(),
                        contacts,
                        json.dumps(updateObject.getPreferences()))
                elif updateType == self.DBUpdate.DB_UPDATE_INVITE_GOING:
                    self._db.setInvite(
                        updatedObject.getID(),
                        update.getUserID(),
                        Event.INVITESTATUS_GOING,
                        update.getCalendar().getName())
                elif updateType == self.DBUpdate.DB_UPDATE_INVITE_MAYBE:
                    self._db.setInvite(
                        updatedObject.getID(),
                        update.getUserID(),
                        Event.INVITESTATUS_MAYBE,
                        None)
                elif updateType == self.DBUpdate.DB_UPDATE_INVITE_DECLINE:
                    self._db.setInvite(
                        updatedObject.getID(),
                        update.getUserID(),
                        Event.INVITESTATUS_DECLINE,
                        None)
                elif updateType == self.DBUpdate.DB_DELETE_EVENT:
                    self._db.deleteEvent(updateObject.getID())
                elif updateType == self.DBUpdate.DB_DELETE_USER:
                    self._db.deleteUser(updateObject.getID())

        except Exception as e:
            print(("Error encountered while trying to update database.\n"
                   "The following error was raised:\n\n{}".format(e)))

    def close(self):
        for userID in self._users.keys():
            self.logoutUser(userID)

        for eventID in self._events.keys():
            del self._events[eventID]

        # Complete remaining updates
        updates = []
        for userUpdates in self._updateQueue.values():
            updates.extend(userUpdates)
        self.updateDatabase(updates)
