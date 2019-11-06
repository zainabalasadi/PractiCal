# Implementation of PractiCalManager class
# Completed by Michael Ho
# Started 15/10/19
# Edited by Egene Oletu
# Last modified 06/11/19

from Calendar import Calendar
from Comment import Comment
from Event import Event
#from templates.code.Group import Group
from Notification import Notification
from User import User
from DatabaseManager import DatabaseManager


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

        def getUpdateType():
            return self._updateType

    # Returns true if new user is successfully created
    def addUser(self, firstName, lastName, email, password):
        userID = self._db.addUser(firstName, lastName, email, password)
        if userID != -1:
            newUser = User(userID, firstName, lastName, email, password)
            defaultCalendar = Calendar('My Calendar', 'Red', 1)
            newUser.addCalendar(defaultCalendar)
            return True
        else:
            return False

    # Search database for users with name or email partial or full matches
    # to query string
    def searchUser(self, query):
        return self._db.searchUser(query)

    # Returns True if user with matching email exists
    def searchUserByEmail(self, email):
        for user in self._users.values():
            if user.get_email() == email:
                return True
        if self._db.checkEmailExists(email) == 1:
                return True
        return False

    # Logs user into system
    #TODO: get user groups
    #TODO: get user contacts
    #TODO: read calendar colour from settings
    def loginUser(self, email, password):
        # Get user from database and load into manager
        # Return None is user doesnt exist
        u = self._db.getUser(email, password)
        if u == -1:
            return None
        userID = u[0]
        userFName = u[1]
        userLName = u[2]
        user = User(userID, userFName, userLName, email, password)
        self._users[userID] = user

        # Get events from database
        events = self._db.getUserEvents(userID)
        if events == -1 or not events: events = []

        calendars = dict()
        for e in events:
            # Load calendar if not already loaded
            if e[6] not in calendars.keys():
                calendars[e[6]] = Calendar(e[6], 'BLUE', user)

            # Load event if not already loaded
            if e[0] not in self._events.keys():
                self._events[e[0]] = Event(eventID=e[0], userID=userID,
                    title=e[2], description=e[3], startDateTime=e[4],
                    endDateTime=e[5], category=e[7], location=e[8])
            if self._events[e[0]] not in calendars[e[6]].getEvents():
                calendars[e[6]].addEvent(self._events[e[0]])

        # Load invites
        invites = self._db.getInvites(userID)
        if invites == -1 or not invites: invites = []

        for i in invites:
            if i[0] not in self._events.keys():
                e = self._db.getEvent(i[0])
                self._events[e[0]] = Event(eventID=e[0], userID=userID,
                    title=e[2], description=e[3], startDateTime=e[4],
                    endDateTime=e[5], category=e[7], location=e[8])

            event = self._events[i[0]]
            if i[2] == Event.INVITESTATUS_NONE:
                user.addInvite(event)
            elif i[2] == Event.INVITESTATUS_GOING:
                if i[3] not in calendars.keys():
                    calendar[i[3]] = Calendar(i[3], 'BLUE', user)
                if self._events[e[0]] not in calendars[i[3]].getEvents():
                    calendars[i[3]].addEvent(self._events[e[0]])
            elif i[2] == Event.INVITESTATUS_MAYBE:
                user.addMaybeEvent(event)

        # Get notifications from database
        notifs = self._db.getNotifications(userID)
        if notifs == -1 or not notifs: notifs = []

        for n in notifs:
            # Load event if not already loaded
            if n[0] not in self._events.keys():
                e = self._db.getEvent(n[0])
                self._events[e[0]] = Event(eventId=e[0], user=userID,
                    name=e[2], description=e[3], startDateTime=e[4],
                    endDateTime=e[5], category=e[7], location=e[8])

            user.addNotification(Notification(event=self._events[n[0]],
                notifType=n[3], senderID=n[1]))

            # Delete notification from database
            self._db.deleteNotification(n[0], n[1], n[2], n[3])
                 
        for c in calendars.values():
            user.addCalendar(c)

        user.setAuthenticated()
        return user

    # Logs user out of system
    # TODO: remove user events from system that arent used by other users (invitees)
    # TODO: garbage cleanup
    def logoutUser(self, userID):
        if userID not in self._users.keys(): return False

        self._users[userID].setAuthenticated(False)

        # Save notifications to database
        for notif in self._users[userID].getNotifications():
            self._db.addNotification(notif.getEvent().getID(),
                notif.getSenderID(), userID, notif.getNotifType())

        del self._users[userID]

        if userID in self._updateQueue.keys():
            self._updateDatabase(self._updateQueue[userID])
            del self._updateQueue[userID]
            
        return True

    # Add a new event to manager and database. Returns new event object
    def addEvent(self, userID, title, description, calendar,
            startDateTime, endDateTime=None, category=None, location=None):
        eventID = self._db.addEvent(userID, title, description, calendar,
            category, startDateTime, endDateTime, location)
        if eventID == -1: return None

        event = Event(eventID, userID, title, description, startDateTime,
            endDateTime, category, location)
        self._events[eventID] = event
        return event    

    # Sends event invites to list of users if event exists in manager
    def sendInvite(self, eventID, senderID, receiverEmails):
        # Check event is loaded
        if eventID not in self._events.keys(): return
        event = self._events[eventID]

        # Check sender is logged in and owner of event
        if not (senderID in self._users.keys() and \
                senderID == event.getUserID()):
            return

        emailsToNotify = receiverEmails
        for email in receiverEmails:
            # Check user exists
            receiverID = self._db.checkEmailExists(email)
            if not receiverID > 0:
                emailsToNotify.remove(email)
                continue

            # Send invite to user if logged in else send to database
            if receiverID in self._users.keys():
                self._users[receiverID].addInvite(self._events[eventID])
            else:
                self._db.addInvite(eventID, receiverID, Event.INVITESTATUS_NONE)

        self.sendNotification(eventID, senderID, emailsToNotify, 
            Notification.NOTIF_EVENTINVITE)
                
    # Updates invite status for user and sends response notification to
    # event owner
    def respondToInvite(self, eventID, userID, response):
        # Check event loaded
        if eventID not in self._events.keys(): return
        # Check user was invited to event
        if userID not in self._events[eventID].getInvitees(): return
        # Check response is valid
        if response != Notification.NOTIF_INVITERESP_GOING and \
                response != Notification.NOTIF_INVITERESP_MAYBE and \
                response != Notification.NOTIF_INVITERESP_DECLINE:
            return

        eventOwnerID = self._events[eventID].getUserID()
        if eventOwnerID in self._users.keys():
            eventOwner = self._users[eventOwnerID]
            event = self._events[eventID]
            # Remove old response notification if there is one
            for notif in eventOwner.getNotifications():
                if notif.getEvent() == event and notif.getSenderID() == userID:
                    eventOwner.removeNotification(notif)
                    break
        else:
            # Remove any old responses
            self._db.deleteNotification(eventID, userID, eventOwnerID,
                Notification.NOTIF_INVITERESP_GOING)
            self._db.deleteNotification(eventID, userID, eventOwnerID,
                Notification.NOTIF_INVITERESP_MAYBE)
            self._db.deleteNotification(eventID, userID, eventOwnerID,
                Notification.NOTIF_INVITERESP_DECLINE)
 
        # Send notification to event owner
        self.sendNotification(eventID, userID, eventOwnerID, response)

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
            receiverID = self._db.checkEmailExists(email)
            if not receiverID > 0: continue
            
            # Send notification to user if logged in else save to database
            if receiverID in self._users.keys():
                self._users[receiverID].addNotification(
                    Notification(event, notifType, senderID))
            else:
                self._db.addNotification(eventID, senderID, receiverID,
                    Notification.NOTIF_EVENTINVITE)
            

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

        self._updateQueue[uid].append(DBUpdate(userID, obj, calendar,
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
                    self._db.setUser(
                        updateObject.getID(),
                        updateObject.getFirstName(),
                        updateObject.getLastName(),
                        updateObject.getEmail(),
                        updateObject.getPassword())
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
