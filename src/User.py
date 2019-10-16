# Implementation of User class
# Completed by Zainab Alasadi
# Started 13/10/19

class User():
    def __init__(self, userId, firstName, lastName, email, password):
        self._id = userId
        self._firstName = firstName
        self._lastName = lastName
        self._email = email
        self._password = password
        self._calendars = []
        self._contacts = []
        self._groups = []
    
    def getID(self):
        return self._id

    def getFirstName(self):
        return self._firstName

    def getLastName(self):
        return self._lastName

    # Validate if provided password matches user password
    def validate(self, password):
        return self._password == password

    def getEmail(self):
        return self._email
    
    def getCalendars(self):
        return self._calendars

    def addCalendars(self, newCategory):
        self._calendars.append(newCategory)

    def getContacts(self):
        return self._contacts

    def addContact(self, contact):
        self._contacts.append(contact)

    def getGroups(self):
        return self._groups

    def addGroup(self, group):
        self._groups.append(group)