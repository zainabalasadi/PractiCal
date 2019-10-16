from src.Notification import Notification
from src.User import User

class Event():

    def __init__(self, eventId, user, name, description, startDateTime, endDateTime, calendar):
        self._user = user
        self._name = name
        self._eventId = eventId
        self._description = description
        self._startDateTime = startDateTime
        self._endDateTime = endDateTime
        self._calendar = calendar
        self._comments = []
        self._invitees = []
        self._groups = []

    def getUser(self):
        return self._user

    def getName(self):
        return self._name

    def getID(self):
        return self._eventId

    def getDescription(self):
        return self._description

    def getStartDateTime(self):
        return self._startDateTime

    def getEndDateTime(self):
        return self._endDateTime

    def getInvitees(self):
        return self._invitees

    def getCalendar(self):
        return self._calendar

    def setUser(self, user):
        self._user = user

    def setName(self, name):
        self._name = name

    def setEventID(self, ID):
        self._eventId = ID

    def setDescription(self, description):
        self._description = description

    def setStartDateTime(self, startDateTime):
        self._startDateTime = startDateTime

    def setEndDateTime(self, endDateTime):
        self._endDateTime = endDateTime

    def setCalendar(self, calendar):
        self._calendar = calendar

    def addComment(self, comment):
        self._comments.append(comment)

    def addInvitee(self, invitee):
        self._invitees.append(invitee)
        notif = Notification(self, 'invite', self.getUser(), invitee)
        inviteeNotifs = invitee.getNotifications()
        inviteeNotifs.append(notif)

    # Returns true if invitee exists in event and is successfully removed
    def removeInvitee(self, invitee):
        try:
            self._invitees.remove(invitee)
            return True
        except:
            return False

    def addGroup(self, group):
        self._groups.append(group)

    # Returns true if group exists in event and is successfully removed
    def removeGroup(self, group):
        try:
            self._groups.remove(group)
            return True
        except:
            return False

    # Edits an event
    # Returns true if editing is successful, false if not
    def editEvent(self, name, desc, startDateTime, endDateTime, invitees):
        # Update event details

        if startDateTime > endDateTime:
            return False

        self.setName(name)
        self.setDescription(desc)
        self.setStartDateTime(startDateTime)
        self.setEndDateTime(endDateTime)

        return True
        # Add or delete invitees
        # TODO
