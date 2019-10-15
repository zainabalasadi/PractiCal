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
        self._categories = []
        self._contacts = []
        self._groups = []
        self._notifications = []
        self._maybe_events = []
    
    def get_id(self):
        return self._id

    def get_firstName(self):
        return self._firstName

    def get_lastName(self):
        return self._lastName

    # Validate if provided password matches user password
    def validate(self, password):
        return self._password == password

    def get_email(self):
        return self._email
    
    def get_categories(self):
        return self._category

    def add_categories(self, newCategory):
        self._calendars.append(newCategory)

    def get_contacts(self):
        return self._contacts

    def add_contacts(self, contact):
        self._contacts.append(contact)

    def get_groups(self):
        return self._groups

    def add_group(self, group):
        self._groups.append(group)

    def get_notifications(self):
        return self._notifications

    def add_notification(self, notif):
        self._notifications.append(notif)

    def remove_notification(self, notif):
        self._notifications.remove(notif)

    def get_maybe_events(self):
        return self._maybe_events

    def add_maybe_event(self, event):
        self._maybe_events.append(event)
 
    def accept_invite(self, notif, category):
        category.add_event(notif.get_event())
        self.remove_notification(notif)

    def decline_invite(self, notif):
        event = notif.get_event()
        inviter = event.get_user()
        new_notif = Notification(event, 'declined_invite', self, inviter)
        inviter.add_notification(new_notif)
        self.remove_notification(notif)

    def maybe_invite(self, notif, category):
        event = notif.get_event()
        inviter = event.get_user()
        new_notif = Notification(event, 'maybe_invite', self, inviter)
        inviter.add_notification(new_notif)
        self.add_maybe_event(event)
        self.remove_notification(notif)
