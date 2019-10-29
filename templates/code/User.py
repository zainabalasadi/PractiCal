# Implementation of User class
# Completed by Zainab Alasadi
# Started 13/10/19
from flask_login import UserMixin

from templates.code.Event import Event
from templates.code.Notification import Notification
from templates.code.Calendar import Calendar


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
        self._maybe_events = []

    # UserMixin required method - don't change name
    def get_id(self):
        try:
            return self._id
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

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

    def addCalendars(self, newCalendar):
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
        self._maybe_events.append(event)

    def acceptInvite(self, notif, calendar):
        calendar.addEvent(notif.getEvent())
        self.removeNotification(notif)

    def declineInvite(self, notif):
        event = notif.getEvent()
        inviter = event.getUser()
        newNotif = Notification(event, 'declined_invite', self, inviter, '')
        inviter.addNotification(newNotif)
        self.removeNotification(notif)

    def maybeInvite(self, notif, calendar):
        event = notif.getEvent()
        inviter = event.getUser()
        newNotif = Notification(event, 'maybe_invite', self, inviter, '')
        inviter.addNotification(newNotif)
        calendar.addEvent(event)
        self.addMaybeEvent(event)
        self.removeNotification(notif)

    def updateEvent(self, event, name, desc, startDateTime, endDateTime):
        # save existing event details
        oldName = event.getName()
        oldDesc = event. getDescription()
        oldStartDateTime = event.getStartDateTime()
        oldEndDateTime = event.getEndDateTime()

        event.editEvent(name, desc, startDateTime, endDateTime)
        
        # check if updated event details are different to existing
        if event.getName() != oldName:
            notifDesc = ['name updated']
        if event.getDescription() != oldDesc:
            notifDesc.append('description updated')
        if event.getStartDateTime() != oldStartDateTime:
            notifDesc.append('start updated')
        if event.getEndDateTime() != oldEndDateTime:
            notifDesc.append('end updated')

        # send notifications to invitees on updated details
        for invitee in event.getInvitees():
            newNotif = Notification(event, 'updated_event', self, invitee, notifDesc)
            invitee.addNotification(newNotif)

    # return true if event successfully deleted
    def deleteEvent(self, event):
        calendar = event.getCalendar()
        if calendar.deleteEvent(event):
            return True
        else:
            return False