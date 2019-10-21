# Implementation of PractiCalManager class
# Completed by Michael Ho
# Started 15/10/19

from templates.code.Calendar import Calendar
from templates.code.User import User


class PractiCalManager():
    def __init__(self):
        self._users = []
        self._numUsers = 0

    def getUsers(self):
        return self._users

    # Returns true if new user is successfully created
    def createUser(self, firstName, lastName, email, password):
        if self.searchUserEmail(email) is None:
            self._numUsers += 1
            newUser = User(self._numUsers, firstName, lastName, email, password)
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
            if user.getEmail() == email:
                return user
        return None
