# Implementation of Calendar class
# Completed by Zainab Alasadi
# Started 13/10/19
import datetime

from templates.code.Notification import Notification


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
        # If the event is shared, remove from everyone's calendar
        if event.getUser() == self._user:
            for invitee in event.getInvitees():
                for calendar in invitee.getCalendars():
                    if event in calendar.getEvents():
                        newNotif = Notification(event, 'deleted_event', event.getUser(), invitee, '')
                        invitee.addNotification(newNotif)
                        calendar.deleteEvent(event)
                        # NOTIFY THEM IT WAS DELETED

        if event in self.getEvents():
            self._events.remove(event)
            return True
        return False

    def calculateHoursCategory(self, category, week):
        time = 0

        week = datetime.datetime(week.year, week.month, week.day, 0, 0)

        while week.weekday() != 0:
            week = week - datetime.timedelta(days=1)

        weekend = week + datetime.timedelta(days=7)

        for event in self._events:
            if event.getCategory() == category and event.getStartDateTime() > week and event.getEndDateTime() < weekend:
                time += event.calculateHoursCategory()
        return time
