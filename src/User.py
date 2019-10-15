# Implementation of User class
# Completed by Zainab Alasadi
# Started 13/10/19

import Notification, Event, Category

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
    
    def get_id(self):
        return str(self._id)

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
 
    def accept_invite(self, notif, category):
        # TODO

    def decline_invite(self, event):
        # TODO

