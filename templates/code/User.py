# Implementation of User class
# Started by Zainab Alasadi
# Started 13/10/19
# Edited by Egene Oletu
# Last modified 06/11/19

from flask_login import UserMixin

from Notification import Notification


class User(UserMixin):
    def __init__(self, userID, firstName, lastName, email, password):
        self._id = userID
        self._firstName = firstName
        self._lastName = lastName
        self._email = email
        self._password = password
        self._calendars = []
        self._contacts = []
        self._groups = []
        self._notifications = []
        self._maybeEvents = []
        self._invites = []
        self._isAuthenticated = False
        self._isActive = True

    # UserMixin required method - don't change name
    def get_id(self):
        try:
            return unicode(self._id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def is_authenticated(self):
        return self._isAuthenticated

    def setAuthenticated(self, isAuthenticated=True):
        self._isAuthenticated = isAuthenticated

    def is_active(self):
        return self._isActive

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

    def addCalendar(self, newCalendar):
        if newCalendar not in self._calendars:
            self._calendars.append(newCalendar)

    def getContacts(self):
        return self._contacts

    def addContact(self, contact):
        self._contacts.append(contact)

    def getGroups(self):
        return self._groups

    def addGroup(self, group):
        self._groups.append(group)

    def getNotifications(self):
        return self._notifications

    def addNotification(self, notif):
        self._notifications.append(notif)

    def removeNotification(self, notif):
        if notif in self.getNotifications():
            self._notifications.remove(notif)

    def getMaybeEvents(self):
        return self._maybe_events

    def addMaybeEvent(self, event):
        self._maybeEvents.append(event)

    def getInvites(self):
        return self._invites

    def addInvite(self, event):
        self._invites.append(event)

    def acceptInvite(self, event, calendar):
        # Check user invited to event
        if not self._email in event.getInvitee(): return
        # Check calendar belongs to user
        if not calendar in self._calendars: return

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
        if not self._email in event.getInvitee(): return
        
        # If event in invites or maybe events, remove it, else exit
        if event in self._invites:
            self._invites.remove(event)
        elif event in self._maybeEvents:
            self._maybeEvents.remove(event)
        
    def maybeInvite(self, event):
        # Check user invited to event
        if not self._email in event.getInvitee(): return
 
        # If event in invites, remove it
        if event in self._invites:
            self._invites.remove(event)

        self.addMaybeEvent(event)
