# Implementation of PractiCalManager class
# Completed by Michael Ho
# Started 15/10/19
# Edited by Egene Oletu

from templates.code.Calendar import Calendar
from templates.code.Comment import Comment
from templates.code.Event import Event
#from templates.code.Group import Group
from templates.code.Notification import Notification
from templates.code.User import User
from templates.code.DatabaseManager import DatabaseManager


class PractiCalManager():
    def __init__(self, database, host, user, password):
        self._users = dict()
        self._events = dict()
        self._db = DatabaseManager(database, host, user, password)
        self._updateQueue = dict()

    class DBUpdate():
        DBUPDATE_CREATE = 0
        DBUPDATE_MODIFY = 1
        DBUPDATE_DELETE = 2

        def __init__(self, obj, updateType):
            self._obj = obj
            self._updateType = updateType

        def getObject(self):
            return self._obj

        def getUpdateType():
            return self._updateType

    # Returns true if new user is successfully created
    def addUser(self, firstName, lastName, email, password):
        userID = self._db.addUser(firstName, lastName, email, password)
        if not userID == -1:
            newUser = User(userID, firstName, lastName, email, password)
            defaultCalendar = Calendar('My Calendar', 'Red', 1)
            newUser.addCalendars(defaultCalendar)
            self._users[userID] = newUser
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
        if user == -1:
            return None
        userID = u[0]
        userFName = u[1]
        userLName = u[2]
        user = User(userId=userID,
                    firstName=userFName,
                    lastName=userLName,
                    email=email,
                    password=password)
        self._users[userID] = user

        # Get events from database
        events = self._db.getUserEvents(userID)
        if events == -1 or not events: events = []

        calendars = dict()
        for e in events:
            # Load calendar if not already loaded
            if not e[6] in calendars.keys():
                calendars[e[6]] = Calendar(e[6], 'BLUE', user)

            # Load event if not already loaded
            if not e[0] in self._events.keys():
                self._events[e[0]] = Event(
                                        eventID=e[0],
                                        userID=userID,
                                        title=e[2],
                                        description=e[3],
                                        startDateTime=e[4],
                                        endDateTime=e[5])
            if not self._events[e[0]] in calendars[e[6]].getEvents():
                calendars[e[6]].addEvent(self._events[e[0]]

        # Load invites
        invites = self._db.getInvites(userID)
        if invites == -1 or nor invites: invites = []

        for i in invites:
            if not i[0] in self._events.keys():
                e = self._db.getEvent(i[0])
                self._events[e[0]] = Event(
                                        eventID=e[0],
                                        userID=userID,
                                        title=e[2],
                                        description=e[3],
                                        startDateTime=e[4],
                                        endDateTime=e[5])
            event = self._events[i[0]]
            if i[2] == Event.INVITESTATUS_NONE:
                user.addInvite(event)
            elif i[2] == Event.INVITESTATUS_GOING:
                if not i[3] in calendars.keys():
                    calendar[i[3]] = Calendar(i[3], 'BLUE', user)
                if not self._events[e[0]] in calendars[i[3]].getEvents():
                    calendars[i[3]].addEvent(self._events[e[0]]
            elif i[2] == Event.INVITESTATUS_MAYBE:
                user.addMaybeEvent(event)

        # Get notifications from database
        notifs = self._db.getNotfications(user[0])
        if notifs == -1 or not notifs: notifs = []

        for n in notifs:
            # Load event if not already loaded
            if not n[0] in self._events.keys():
                e = self._db.getEvent(n[0])
                self._events[e[0]] = Event(
                                        eventId=e[0],
                                        user=userID,
                                        name=e[2],
                                        description=e[3],
                                        startDateTime=e[4],
                                        endDateTime=e[5])

            user.addNotification(
                Notification(
                    event=self._events[n[0]],
                    notifType=n[3],
                    senderID=n[1])
                 
        for c in calendars.values():
            user.addCalendars(c)

        user.setAuthenticated()
        return user

    # Logs user out of system
    def logoutUser(self, userID):
        if not userID in self._users.keys(): return False

        self._users[userID].setAuthenicated(False)
        del self._users[userID]

        if userID in self._updateQueue.keys():
            self._updateDatabase(self._updateQueue[userID])
            del self._updateQueue[userID]
            
        return True

    # Sends event invites to list of users if event exists in manager
    def sendInvite(self, eventID, senderID, receiverEmails)
        # Check event is loaded
        if not eventID in self._events.keys(): return

        for email in receiverEmails:
            # Check user exists
            receiverID = self._db.checkEmailExists(email)
            if not receiver > 0: continue

            # Send invite to user if logged in else send to database
            if receiverID in self._users.keys():
                self._users[receiverID].addNotification(
                    Notification(self._events[eventID],
                        Notification.NOTIF_EVENTINVITE, senderID))
                self._users[receiverID].addInvite(self._events[eventID])
            else:
                self._db.addNotification(eventID, senderID, receiverID,
                    Notification.NOTIF_EVENTINVITE)
                self._db.addInvite(eventID, receiverID, Event.INVITESTATUS_NONE)
                
    # Updates invite status for user and sends response notification to
    # event owner
    def respondToInvite(self, eventID, userID, response):
        # Check event loaded
        if not eventID in self._events.keys(): return
        # Check user was invited to event
        if not userID in self._events[eventID].getInvitees(): return
        # Check response is valid
        if not response == Notification.NOTIF_INVITERESP_GOING and \
                not response == Notification.NOTIF_INVITERESP_MAYBE and \
                not response == Notification.NOTIF_INVITERESP_DECLINE:
            return

        eventOwnerID = self._events[eventID].getUserID()
        if eventOwnerID in self._users.keys():
            eventOwner = self._users[eventOwnerID]
            event = self._events[eventID]
            eventOwner.addNotification(Notification(event, response, userID)
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
            
            # Add notification to database
            self._db.addNotification(eventID, userID, eventOwnerID, response)

    # Sends notification to list of users
    def sendNotification(self, eventID, userIDs, notif_type):
        #TODO
        pass

    # Adds object to queue of database updates to be done once user has
    # logged out
    def addToUpdateQueue(self, obj, updateType):
        if type(obj) == User:
            uid = obj.getID()

        if type(obj) == Event:
            uid = obj.getUser().getID()

        update = DBUpdate(obj, updateType)
        if not uid in self._updateQueue.keys():
            self._updateQueue[uid] = []

        # Skip if obj already in queue
        if obj in self._updateQueue[uid]:
            return
        self._updateQueue[uid].append(update)

    # Applies changes to database corresponding to list of objects given
    def updateDatabase(self, updates):
        try:
            for update in updates:
                updateType = update.getUpdateType()
                updateObject = update.getObject()

                if updateType == DBUpdate.DBUPDATE_CREATE:
                    if type(updateObject) == Event:
                        self._db.addEvent(
                            updateObject.getUser().getID(),
                            updateObject.getName(),
                            updateObject.getDescription(),
                            updateObject.getCalendar().getName(),
                            updateObject.getStartDateTime(),
                            updateObject.getEndDateTime())

                    elif type(updateObject) == Calendar:
                        event_updates = [
                            self.DBUpdate(event, self.DBUpdate.DBUPDATE_CREATE)
                            for event in updateObject.getEvents()]
                        self.updateDatabase(event_updates)

                elif updateType == DBUpdate.DBUPDATE_MODIFY:
                    if type(updateObject) == User:
                        self._db.setUser(
                            updateObject.getID(),
                            updateObject.getFirstName(),
                            updateObject.getLastName(),
                            updateObject.getEmail(),
                            updateObject.getPassword())

                    elif type(updateObject) == Event:
                        self._db.setEvent(
                            updateObject.getID(),
                            updateObject.getName(),
                            updateObject.getDescription(),
                            updateObject.getStartDateTime(),
                            updateObject.getEndDateTime(),
                            updateObject.getCalendar().getName())

                elif updateType == DBUpdate.DBUPDATE_DELETE:
                    if type(updateObject) == User:
                        self._db.deleteUser(updateObject.getID())

                    elif type(updateObject) == Event:
                        self._db.deleteEvent(updateObject.getID())

                    elif type(updateObject) == Calendar:
                        for event in updateObject.getEvents():
                            self._db.deleteEvent(event.getID())
                            del event

                    del updateObject

                del update

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
