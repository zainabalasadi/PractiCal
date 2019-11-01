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

    # TODO: Search database for users by name or email

    # Returns True if user with matching email exists
    def searchUserByEmail(self, email):
        for user in self._users.values():
            if user.get_email() == email:
                return True
        if self._db.checkEmailExists(email) == 1:
                return True
        return False

    # Logs user into system
    #TODO: get user notifications, groups, contacts,...
    #TODO: read calendar colour from settings
    def loginUser(self, email, password):
        # Get user from database. Return None is user doesnt exist
        user = self._db.getUser(email, password)
        if user == -1:
            return None

        # Load events created by user
        events = self._db.getUserEvents(user[0])
        if events == -1:
            events = []

        cals = dict()
        for e in events:
            e_cal = None
            calName = e[6]
            if calName in cals.keys():
                e_cal = cals[calName]
            else:
                # Create new calendar is not already defined
                e_cal = Calendar(calName, 'blue', e[1])
                cals[calName] = e_cal

            event = Event(eventId=e[0],
                          user=e[1],
                          name=e[2],
                          description=e[3],
                          startDateTime=e[4],
                          endDateTime=e[5],
                          calendar=e_cal)
            cals[calName].addEvent(event)
        cals = list(cals.values())
        
        u = User(userId=user[0],
                 firstName=user[1],
                 lastName=user[2],
                 email=email,
                 password=password)
        for c in cals:
            u.addCalendars(c)
        u.setAuthenticated()

        self._users[user[0]] = u
        return u

    # Logs user out of system
    def logoutUser(self, userID):
        if not userID in self._users.keys():
            return False

        self._users[userID].setAuthenicated(False)
        del self._users[userID]

        if userID in self._updateQueue.keys():
            self._updateDatabase(self._updateQueue[userID])
            del self._updateQueue[userID]
            
        return True

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
