import datetime
from templates.code.Comment import Comment
from templates.code.Notification import Notification

class Event():
    def __init__(self, eventID, userID, name, description, startDateTime,
            endDateTime, category, location=None, invitees=dict()):
        self._eventID = eventID
        self._userID = userID
        self._name = name
        self._description = description
        self._startDateTime = startDateTime
        self._endDateTime = endDateTime
        self._category = category
        self._location = location
        self._comments = []
        self._invitees = invitees

    def getUserID(self):
        return self._userID

    def getName(self):
        return self._name

    def getID(self):
        return self._eventID

    def getComments(self):
        return self._comments

    def getDescription(self):
        return self._description

    def getStartDateTime(self):
        return self._startDateTime

    def getEndDateTime(self):
        return self._endDateTime

    def getCategory(self):
        return self._category

    def getLocation(self):
        return self._location

    def getInvitees(self):
        return self._invitees

    def setUser(self, user):
        self._userID = user

    def setName(self, name):
        self._name = name

    def setEventID(self, ID):
        self._eventID = ID

    def setDescription(self, description):
        self._description = description

    def setStartDateTime(self, startDateTime):
        # if startDateTime < self._endDateTime:
        self._startDateTime = startDateTime

    def setEndDateTime(self, endDateTime):
        if endDateTime > self._startDateTime:
            self._endDateTime = endDateTime

    def setCategory(self, category):
        self._category = category

    def setLocation(self, location):
        self._location = location

    def addComment(self, comment):
        self._comments.append(comment)

    def addInvitees(self, invitee):
        for invitee in invitees:
            if not invitee in self._invitees:
                self._invitees.append(invitee)

    # Edits an event
    # Returns true if editing is successful, false if not
    def editEvent(self, name, desc, startDateTime, endDateTime, category):
        # Update event details

        if startDateTime > endDateTime:
            return False
        self.setCategory(category)
        self.setName(name)
        self.setDescription(desc)
        self.setStartDateTime(startDateTime)
        self.setEndDateTime(endDateTime)
        return True

    def removeComment(self, comment):
        for comments in self._comments:
            # if the comment matches, and its the same poster, remove it
            if comment.getComment() == comments.getComment() and \
                    comment.getUser() == comments.getUser():
                self._comments.remove(comments)
            # recursion
            comments.deleteComment(comment)

    def calculateHoursCategory(self):
        dateTimeDifference = datetime.datetime.strptime(self.getEndDateTime(), "%Y-%m-%dT%H:%M:%S") - datetime.datetime.strptime(self.getStartDateTime(), "%Y-%m-%dT%H:%M:%S")
        return dateTimeDifference.total_seconds() / 3600
