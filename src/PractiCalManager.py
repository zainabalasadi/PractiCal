# Implementation of PractiCalManager class
# Completed by Michael Ho
# Started 15/10/19
from src.User import User


class PractiCalManager():
    def __init__(self):
        self._users = []

    def get_users(self):
        return self._users

    # Returns true if new user is successfully created
    def createUser(self, userId, firstName, lastName, email, password):
        if self.searchUserEmail() is None:
            new_user = User(userId, firstName, lastName, email, password)
            self._users.append(new_user)
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
        for user in self.users:
            if user.get_email() == email:
                return user
        return None
