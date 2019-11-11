# Implementation of User class
# Started by Zainab Alasadi
# Started 13/10/19
# Edited by Egene Oletu
# Last modified 06/11/19

from flask_login import UserMixin
from templates.code.Notification import Notification

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
        return self._calendars

    def getContacts(self):
        return self._contacts

    def getGroups(self):
        return self._groups

    def getNotifications(self):
        return self._notifications

    def getMaybeEvents(self):
        return self._maybe_events

    def getInvites(self):
        return self._invites

    #
    # Adders
    #
    def addCalendar(self, newCalendar):
        if newCalendar not in self._calendars:
            for calendar in self._calendars:
                if calendar.getName() == newCalendar.getName():
                    return False
            self._calendars.append(newCalendar)
            return True
        return False

    def addContact(self, contact):
        if contact not in self._contacts:
            self._contacts.append(contact)

    def addContactByNameEmail(self, contactInfo):
        #for contact in db
            #if contactInfo in email.db
                #addContact(contact)
                #return True
            #if contactInfo in name.db
                #addContact(contact)
                #return True
        return False

    def addGroup(self, group):
        if group not in self._groups:
            self._groups.append(group)

    def addNotification(self, notif):
        if notif not in self._notifications:
            self._notifications.append(notif)

    def addMaybeEvent(self, event):
        if event not in self._maybeEvents:
            self._maybeEvents.append(event)

    def addInvite(self, event):
        if event not in self._invites:
            self._invites.append(event)

    #
    # Setters
    #
    def changeCalendarName(self, calendar, name):
        if calendar in self.getCalendars():
            calendar.setName(name)

    def changeCalendarColour(self, calendar, colour):
        if calendar in self.getCalendars():
            calendar.setColour(colour)

    def updateEvent(self, event, name, desc, startDateTime, endDateTime, calendar, category):
        # save existing event details
        oldName = event.getName()
        oldDesc = event.getDescription()
        oldStartDateTime = event.getStartDateTime()
        oldEndDateTime = event.getEndDateTime()
        oldCalendar = event.getCalendar()
        oldCategory = event.getCategory()

        event.editEvent(name, desc, startDateTime, endDateTime, calendar, category)

        notifDesc = []

        # check if updated event details are different to existing
        if event.getName() != oldName:
            notifDesc.append('name updated')
        if event.getDescription() != oldDesc:
            notifDesc.append('description updated')
        if event.getStartDateTime() != oldStartDateTime:
            notifDesc.append('start updated')
        if event.getEndDateTime() != oldEndDateTime:
            notifDesc.append('end updated')
        if event.getCalendar() != oldCalendar:
            notifDesc.append('calendar updated')
        if event.getCategory() != oldCategory:
            notifDesc.append('category updated')

        # send notifications to invitees on updated details
        for invitee in event.getInvitees():
            newNotif = Notification(event, 'updated_event', self, invitee, notifDesc)
            invitee.addNotification(newNotif)

        #TODO
        #update groups

    #
    # Removers
    #
    def deleteCalendar(self, calendar):
        if calendar in self._calendars:
            self._calendars.remove(calendar)

    def removeNotification(self, notif):
        if notif in self.getNotifications():
            self._notifications.remove(notif)

    def removeContact(self, contact):
        if contact in self._contacts:
            self._contacts.remove(contact)

    # remove from all calendars
    def deleteEvent(self, event):

        for calendar in self._calendars:
            calendar.deleteEvent(event)

        # TODO
        # update groups

    #remove from one calendar
    def deleteEventOneCalendar(self, event):
        calendar = event.getCalendar()

        if calendar is None:
            return False

        if calendar.deleteEvent(event):
            return True
        else:
            return False

    #
    # Invite response methods
    #
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
