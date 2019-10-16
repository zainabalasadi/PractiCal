# Implementation of User class
# Completed by Zainab Alasadi
# Started 13/10/19

from src.Notification import Notification
from src.Event import Event
from src.Category import Category

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
        self._notifications = []
        self._maybe_events = []
    
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

    def getNotifications(self):
        return self._notifications

    def addNotification(self, notif):
        self._notifications.append(notif)

    def removeNotification(self, notif):
        self._notifications.remove(notif)

    def getMaybeEvents(self):
        return self._maybe_events

    def addMaybeEvent(self, event):
        self._maybe_events.append(event)
 
    def acceptInvite(self, notif, category):
        category.add_event(notif.get_event())
        self.remove_notification(notif)

    def declineInvite(self, notif):
        event = notif.get_event()
        inviter = event.get_user()
        new_notif = Notification(event, 'declined_invite', self, inviter)
        inviter.add_notification(new_notif)
        self.remove_notification(notif)

    def maybeInvite(self, notif, category):
        event = notif.get_event()
        inviter = event.get_user()
        new_notif = Notification(event, 'maybe_invite', self, inviter)
        inviter.add_notification(new_notif)
        category.add_event(event)
        self.add_maybe_event(event)
        self.remove_notification(notif)