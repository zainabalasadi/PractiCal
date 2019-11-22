# Implementation of User class
# Started by Zainab Alasadi
# Started 13/10/19
# Edited by Egene Oletu
# Last modified 06/11/19

from flask_login import UserMixin
from templates.code.Group import Group
from templates.code.Notification import Notification
from templates.code.Calendar import Calendar

import datetime


class User(UserMixin):
    def __init__(self, userID, firstName, lastName, email,
            preferences=None):
        self._id = userID
        self._firstName = firstName
        self._lastName = lastName
        self._email = email
        if preferences:
            self._preferences = preferences
        else:
            self._preferences = {
                'default_colour': '#566EE9',
                'calendars': {
                    'Default': {
                        'colour': '#566EE9'
                    }
                }
            }
        self._calendars = dict()
        for cal in self._preferences['calendars'].keys():
            self._calendars[cal] = Calendar(cal,
                self._preferences['calendars'][cal]['colour'])
        self._contacts = dict()
        self._groups = dict()
        self._notifications = dict()
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
        except:
            cal = None
        return cal

    def getContacts(self):
        contacts = []
        for email in self._contacts.keys():
            contacts.append((email, self._contacts[email][firstName],
                self._contacts[email][lastName],
                [grp.getName() for grp in self._contacts[email]['groups']]))
        return contacts

    def getGroups(self):
        return list(self._groups.values())

    def getNotifications(self):
        return list(self._notifications.values())

    def getPreferences(self):
        return self._preferences

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
            self._preferences['calendars'][newCalName] = \
                {'colour': newCalendar.getColour()}
            return True

    def addContact(self, email, firstName="", lastName="", groupName=None):
        try:
            mem = self._contacts[email]
        except:
            mem = self._contacts[email] = {
                'firstName': firstName,
                'lastName': lastName,
                'groups': []}

        if not groupName: return
        try:
            grp = self._groups[groupName]
        except:
            grp = self._groups[groupName] = Group(groupName)
        grp.addMember(email, mem['firstName'], mem['lastName'])
        if grp not in mem['groups']:
            self._contacts[email]['groups'].append(grp)

    def addGroup(self, group):
        try:
            grp = self._groups[group.getName()]
            return
        except:
            self._groups[group.getName()] = group

    def addNotification(self, event, notifType, senderEmail):
        for notif in self._notifications.values():
            if notif.getEvent() == event and notif.getNotifType() == notifType:
                return
        if notifType < Notification.NOTIF_EVENTCHANGE or \
                notifType > Notification.NOTIF_INVITERESP_NONE:
            return
        ids = list(self._notifications.keys())
        ids.sort()
        newID = ids[-1] + 1 if ids else 1
        self._notifications[newID] = Notification(
            newID, event, notifType, senderEmail)

    # Adds new invite to default calendar
    def addInvite(self, event):
        self._calendars['Default'].addInvite(event)

    #
    # Setters
    #
    def changeCalendarName(self, calendar, newName):
        try:
            # Update calendar
            oldName = calendar.getName()
            del self._calendars[oldName]
            calendar.setName(newName)
            self._calendars[newName] = calendar

            # Update user preferences
            calPref = self._preferences[oldName]
            del self._preferences['calendars'][oldName]
            self._preferences['calendars'][newName] = calPref
            return True
        except:
            return False

    def changeCalendarColour(self, calendar, colour):
        try:
            calName = calendar.getName()
            self._calendars[calName].setColour(colour)
            self._preferences['calendars'][calName]['colour'] = colour
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
                self._calendars['Default'] = Calendar('Default',
                    calendar.getColour())
            else:
                del self._preferences['calendars'][calendar.getName()]
            return True
        except:
            return False

    def removeNotification(self, notif, notifID=None):
        if not notifID: notifID = notif.getID()
        try:
            del self._notifications[notifID]
        except:
            pass
        return

    # Removes invite from account and related notifications
    def removeInvite(self, event):
        for calendar in self._calendars.values():
            calendar.removeInvite(event)
        for notif in self._notifications:
            if notif.getEvent() == event:
                self._notifications.remove(notif)

    def removeContact(self, email):
        try:
            del self._contacts[email]
            for group in self._groups:
                group.removeMember(email)
        except:
            pass

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
                if title.lower() in event.getName().lower():
                    listOfEvents.append(event)
        return listOfEvents

    #def getEventById(self, ident):
    #    for calendar in self._calendars:
    #        for event in calendar.getEvents():
    #            if event.getID == ident:
    #                return event
    #    return None

    # search through own events by description
    def searchEventsByDescription(self, desc):
        listOfEvents = []
        for calendar in self._calendars:
            for event in self._calendars[calendar].getEvents():
                if desc.lower() in event.getDescription().lower():
                    listOfEvents.append(event)
        return listOfEvents

    def getEventsByQuery(self, queryString):
        return list(set(self.searchEventsByTitle(queryString)) | set(self.searchEventsByDescription(queryString)))
        # + self.searchEventsByHost(queryString)

    def calculateHoursCategory(self):
        l = {"Work": 0,
             "Social": 0,
             "School": 0,
             "Family": 0
             }
        for category in l.keys():
            time = 0
            for calendar in self.getCalendars():
                time += calendar.calculateHoursCategory(category, datetime.datetime.now())
            l[category] = time
        return l

    # MOVED TO views.py because PCM needed
    # search through events by host
    # def searchEventsByHost(self, host):
    #     listOfEvents = []
    #     for calendar in self._calendars:
    #         # self._calendar[calendar]
    #         for event in self._calendars[calendar].getEvents():
    #             userID = event.getUserID()
    #             firstName = PCM.getUserInfo(userID=userID)[0]
    #             lastName = PCM.getUserInfo(userID=userID)[1]
    #             userName = firstName + " " + lastName
    #             if host.lower() in userName.lower():
    #                 listOfEvents.append(event)
    #     return listOfEvents

    #
    # Other
    #
