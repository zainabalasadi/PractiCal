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
        self._calendars = {'Default': Calendar('Default', 'blue')}
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

    def getCalendars(self):
        return list(self._calendars.values())

    def getCalendarByName(self, name):
        try:
            cal = self._calendars[name]
            print ("got calendar" + name)
        except:
            cal = None
            print ("didnt get cal")
        return cal

    def getContacts(self):
        return self._contacts

    def getGroups(self):
        return self._groups

    def getNotifications(self):
        return self._notifications

    #
    # Adders
    #
    def addCalendar(self, newCalendar):
        newCalName = newCalendar.getName()
        try:
            cal = self._calendars[newCalName]
            return False
        except:
            self._calendars[newCalName] = newCalendar
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
        self._calendars['Default'].addInvite(event)

    #
    # Setters
    #
    def changeCalendarName(self, calendar, name):
        try:
            self._calendars[calendar.getName()].setName(name)
            return True
        except:
            return False

    def changeCalendarColour(self, calendar, colour):
        try:
            self._calendars[calendar.getName()].setColour(colour)
            return True
        except:
            return False

    def moveEvent(self, event, calName):
        cal = self.getCalendarByName(calName)
        if event not in cal.getEvents():
            self.deleteEvent(event)
            cal.addEvent(event)

    #
    # Removers
    #
    def deleteCalendar(self, calendar):
        try:
            del self._calendars[calendar.getName()]
            if calendar.getName() == 'Default':
                self._calendars['Default'] = Calendar('Default', 'blue')
            return True
        except:
            return False

    def removeNotification(self, notif):
        if notif in self.getNotifications():
            self._notifications.remove(notif)

    # Removes invite from account and related notifications
    def removeInvite(self, event):
        for calendar in self._calendars.values():
            calendar.removeInvite(event)
        for notif in self._notifications:
            if notif.getEvent() == event:
                self._notifications.remove(notif)

    def removeContact(self, contact):
        if contact in self._contacts:
            self._contacts.remove(contact)

    # remove from all calendars
    def deleteEvent(self, event):
        for calendar in self._calendars.values():
            calendar.deleteEvent(event)

    #
    # Invite response methods
    #
    def respondToInvite(self, event, status=Calendar.INVITESTATUS_GOING,
            calendar=None):
        # Check user invited to event
        if self._email not in event.getInvitee(): return
        # Check calendar belongs to user
        if calendar and calendar not in self._calendars.values(): return
        # Check status code is valid
        if status < Calendar.INVITESTATUS_GOING or \
                status > Calendar.INVITESTATUS_DECLINE: return

        # Remove existing existing invite from all calendars
        for cal in self._calendars.values():
            cal.removeInvite(event)

        # Add invite to calendar
        calendar.addInvite(event, status)

    #
    # Search
    #

    # search through own events by title
    def searchEventsByTitle(self, title):
        listOfEvents = []
        for calendar in self._calendars:
            for event in self._calendars[calendar].getEvents():
                print("NEW COMPARISON")
                print(event.getName().lower())
                print(title.lower())
                if title.lower() in event.getName().lower():
                    print("added")
                    listOfEvents.append(event)
        print(listOfEvents)
        return listOfEvents

    #def getEventById(self, ident):
    #    for calendar in self._calendars:
    #        for event in calendar.getEvents():
    #            if event.getID == ident:
    #                return event
    #    return None

    def getEventsByQuery(self, queryString):
        return self.searchEventsByTitle(queryString)
        # + self.searchEventsByHost(queryString)

    # search through events by host
    def searchEventsByHost(self, host):
        listOfEvents = []
        for calendar in self._calendars:
            # self._calendar[calendar]
            for event in self._calendars[calendar].getEvents():
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
