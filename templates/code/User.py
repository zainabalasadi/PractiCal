# Implementation of User class
# Started by Zainab Alasadi
# Started 13/10/19
# Edited by Egene Oletu
# Last modified 06/11/19

from flask_login import UserMixin
from templates.code.Group import Group
from templates.code.Notification import Notification
from templates.code.Calendar import Calendar


class User(UserMixin):
    def __init__(self, userID, firstName, lastName, email, password):
        self._id = userID
        self._firstName = firstName
        self._lastName = lastName
        self._email = email
        self._password = password
        self._defaultCalendar = Calendar('default', 'blue')
        self._calendars = []
        self._calendars.append(self._defaultCalendar)
        self._contacts = []
        self._groups = []
        self._notifications = []
        self._isAuthenticated = False
        self._isActive = True

    #
    # Flask login functions
    #
    def get_id(self):
        try:
            return str(self._id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def is_authenticated(self):
        return self._isAuthenticated

    def setAuthenticated(self, isAuthenticated=True):
        self._isAuthenticated = isAuthenticated

    def is_active(self):
        return self._isActive

    # Validate if provided password matches user password
    def validate(self, password):
        return self._password == password

    #
    # Getters
    #
    def getID(self):
        return self._id

    def getFirstName(self):
        return self._firstName

    def getLastName(self):
        return self._lastName

    def getEmail(self):
        return self._email

    def getCalendars(self, calendar=None):
        if not calendar:
            return [self._defaultCalendar] + self._calendars
        if calendar == 'default':
            return self._defaultCalendar
        for cal in self._calendars:
            if cal.getName() == calendar: return cal
        return None

    def getCalendarByName(self, name):
        for cal in self._calendars:
            if cal.getName() == name:
                return cal
        return None

    def getContacts(self):
        return self._contacts

    def getGroups(self):
        return self._groups

    def getNotifications(self):
        return self._notifications
    
    def updateEvent(event, name, desc, startDate)

    #
    # Adders
    #
    def addCalendar(self, newCalendar):
        newCalName = newCalendar.getName()
        if newCalName == 'default':
            self._defaultCalendar = newCalendar
            return True
        for cal in self._calendars:
            if cal.getName() == newCalName:
                return False

        self._calendars.append(newCalendar)
        return True

    def addContact(self, contact):
        if contact not in self._contacts:
            self._contacts.append(contact)

    def addContactByNameEmail(self, contactInfo):
        # for contact in db
        # if contactInfo in email.db
        # addContact(contact)
        # return True
        # if contactInfo in name.db
        # addContact(contact)
        # return True
        return

    def addGroup(self, group):
        if group not in self._groups:
            self._groups.append(group)

    def addNotification(self, notif):
        if notif not in self._notifications:
            self._notifications.append(notif)

    # Adds new invite to default calendar
    def addInvite(self, event):
        self.defaultCalendar.addInvite(event)

    #
    # Setters
    #
    def changeCalendarName(self, calendar, name):
        if calendar in self.getCalendars():
            calendar.setName(name)

    def changeCalendarColour(self, calendar, colour):
        if calendar in self.getCalendars():
            calendar.setColour(colour)

    def moveEvent(self, event, calName):
        cal = self.getCalendarByName(calName)
        if (event not in cal.getEvents()):
            self.deleteEvent(event)
            cal.addEvent(event)

    #
    # Removers
    #
    def deleteCalendar(self, calendar):
        if calendar in self._calendars:
            self._calendars.remove(calendar)

    def removeNotification(self, notif):
        if notif in self.getNotifications():
            self._notifications.remove(notif)

    # Removes invite from account and related notifications
    def removeInvite(self, eventID):
        self._defaultCalendar.removeInvite(event)
        for calendar in self._calendars:
            calendar.removeInvite(event)
        for notif in self._notifications:
            if notif.getEvent() == event:
                self._notifications.remove(notif)

    def removeContact(self, contact):
        if contact in self._contacts:
            self._contacts.remove(contact)

    # remove from all calendars
    def deleteEvent(self, event):
        self._defaultCalendar.deleteEvent(event)
        for calendar in self._calendars:
            calendar.deleteEvent(event)

    #
    # Invite response methods
    #
    def acceptInvite(self, event, calendar):
        # Check user invited to event
        if self._email not in event.getInvitee():
            return
        # Check calendar belongs to user
        if calendar not in self._calendars:
            return

        # If event in invites or maybe events, remove it, else exit
        if event in self._invites:
            self._invites.remove(event)
        elif event in self._maybeEvents:
            self._maybeEvents.remove(event)
        else:
            return

        # Add event to calendar
        calendar.addEvent(event)

    def declineInvite(self, event):
        # Check user invited to event
        if self._email not in event.getInvitee():
            return

        # If event in invites or maybe events, remove it, else exit
        if event in self._invites:
            self._invites.remove(event)
        elif event in self._maybeEvents:
            self._maybeEvents.remove(event)

    def maybeInvite(self, event):
        # Check user invited to event
        if self._email not in event.getInvitee():
            return

        # If event in invites, remove it
        if event in self._invites:
            self._invites.remove(event)

        self.addMaybeEvent(event)

    #
    # Search
    #

    # search through own events by title
    def searchEventsByTitle(self, title):
        listOfEvents = []
        for calendar in self._calendars:
            for event in calendar.getEvents():
                if event.getName().lower() in title.lower():
                    listOfEvents.append(event)
        return listOfEvents

    def getEventById(self, ident):
        for calendar in self._calendars:
            for event in calendar.getEvents():
                if event.getID == ident:
                    return event
        return None

    def getEventsByQuery(self, queryString):
        return self.searchEventsByHost(queryString) + self.searchEventsByHost(queryString)

    # search through events by host
    def searchEventsByHost(self, host):
        listOfEvents = []
        for calendar in self._calendars:
            for event in calendar.getEvents():
                user = event.getUser()
                userName = user.getFirstName() + user.getLastName()
                if userName.lower() in host.lower():
                    listOfEvents.append(event)
        return listOfEvents

    #
    # Other
    #
    def calculateHoursCategory(self, category, week):
        time = 0

        for calendar in self._calendars:
            time += calendar.calculateHoursCategory(category, week)
        return time

    def createGroup(self, name, members):
        group = Group(name)
        for user in members:
            group.addMember(user)
        self._groups.append(group)

    def addUserToGroup(self, user, group):
        if group in self._groups:
            group.addMember(user)

    def removeUserFromGroup(self, user, group):
        if group in self._groups:
            group.removeMember(user)
