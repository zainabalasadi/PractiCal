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
        self._users = []
        self._db = DatabaseManager(database, host, user, password)

    def getUsers(self):
        return self._users

    # Returns true if new user is successfully created
    def createUser(self, userId, firstName, lastName, email, password):
        if self.searchUserEmail() is None:
            newUser = User(userId, firstName, lastName, email, password)
            defaultCalendar = Calendar('My Calendar', 'Red', 1)
            newUser.addCalendars(defaultCalendar)
            self._users.append(newUser)
            return True
        else:
            return False

    # Return true if user exists and is successfully removed from system
    def removeUser(self, user):
        try:
            self._users.remove(user)
            return True
        except:
            return False

    # Returns list of matching users
    def searchUserName(self, firstName, lastName):
        matchingUsers = []
        for user in self._users:
            if user.getFirstName() == firstName and user.getLastName() == lastName:
                matchingUsers.append(user)
        return matchingUsers

    # Returns matching user if exists
    def searchUserEmail(self, email):
        for user in self._users:
            if user.get_email() == email:
                return user
        return None

    def loadUser(self, email, password):
        user = self._db.getUser(email, password)
        if user == -1:
            return None

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
                #TODO: read calendar colour from settings
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
        #TODO: get user notifications, groups, contacts,...
        u = User(userId=user[0],
                 firstName=user[1],
                 lastName=user[2],
                 email=email,
                 password=password,
                 calendars=cals)

        self._users.append(u)
        return u
