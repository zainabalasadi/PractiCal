# Implementation of Calendar class
# Completed by Zainab Alasadi
# Started 13/10/19

from templates.code.Event import Event
from templates.code.User import User

class Calendar():
    def __init__(self, name, colour, user):
        self._name = name
        self._colour = colour
        self._events = []
        self._user = user

    def getName(self):
        return self._name

    def getColour(self):
        return str(self._colour)

    def getEvents(self):
        return self._events

    # Adds an event to a user's calendar
    # Returns true if addition is successful, false if not
    def addEvent(self, event):
        if event not in self.getEvents():
            self._events.append(event)
            return True
        return False

    # Removes a given event from a user's calendar
    # Returns true if removal is successful, false if not
    def deleteEvent(self, event):
        # TODO
        # If the event is shared, remove from everyone's calendar

        if event.getUser() == self._user:
            for invitee in event.getInvitees():
                for calendar in invitee.getCalendars():
                    if event in calendar.getEvents():
                        calendar.deleteEvent(event)

        if event in self.getEvents():
            self._events.remove(event)
            return True
        return False
