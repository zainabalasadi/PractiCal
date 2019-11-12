# Implementation of Calendar class
# Completed by Zainab Alasadi
# Started 13/10/19
import datetime

from templates.code.Notification import Notification

class Calendar():
    INVITESTATUS_NONE = 0
    INVITESTATUS_GOING = 1
    INVITESTATUS_MAYBE = 2
    INVITESTATUS_DECLINE = 3

    def __init__(self, name, colour, events=[]):
        self._name = name
        self._colour = colour
        self._events = events
        self._invites = {
            self.INVITESTATUS_NONE: [],
            self.INVITESTATUS_GOING: [],
            self.INVITESTATUS_MAYBE: [],
            self.INVITESTATUS_DECLINE: []}

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getColour(self):
        return str(self._colour)

    def setColour(self, colour):
        self._colour = colour

    def getEvents(self):
        return self._events

    # Adds an event to a user's calendar
    # Returns true if addition is successful, false if not
    def addEvent(self, event):
        if event not in self._events:
            self._events.append(event)
            return True
        return False
    
    # Add invite to calendar. If invite already in calendar,
    # changes existing status to one provided
    def addInvite(self, event, status=None):
        if not status: status = self.IVITESTATUS_NONE
        if not (status >= self.INVITESTATUS_NONE and \
                status <= self.INVITESTATUS_DECLINE):
            return
        self.removeInvite(event)
        self._invites[status].append(event)

    # Remove invite from calendar
    def removeInvite(self, event):
        for events in self._invites.keys():
            if event in events:
                self._invites[events].remove(event)
                return 

    # Return list of tuples of the form (event, status). If status
    # not provided, list will contain all invites. Returns None if invalid
    # status given
    def getInvites(self, status=None):
        if status and status >= self.INVITESTATUS_NONE and \
                status <= self.INVITESTATUS_DECLINE:
            return [(e, status) for e in self._invites[status]]
        elif not status:
            invites = []
            for status in self._invites.keys():
                invites += [(e, status) for e in self._invites[status]]
            return invites
        return None

    def moveDelete(self, event):
        self._events.remove(event)

    # Removes a given event from a user's calendar
    def deleteEvent(self, event):
        if event in self._events:
            self._events.remove(event)

    def calculateHoursCategory(self, category, week):
        time = 0

        week = datetime.datetime(week.year, week.month, week.day, 0, 0)

        while week.weekday() != 0:
            week = week - datetime.timedelta(days=1)

        weekend = week + datetime.timedelta(days=7)

        for event in self._events:
            if event.getCategory() == category and \
                    event.getStartDateTime() > week and \
                    event.getEndDateTime() < weekend:
                time += event.calculateHoursCategory()
        return time
