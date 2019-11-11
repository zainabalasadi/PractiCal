import datetime
from templates.code.Comment import Comment
from templates.code.Notification import Notification

class Event():
    INVITESTATUS_NONE = 0
    INVITESTATUS_GOING = 1
    INVITESTATUS_MAYBE = 2
    INVITESTATUS_DECLINED = 3

    def __init__(self, eventID, userID, title, description, startDateTime, 
            endDateTime, category, location):
        self._eventID = eventID
        self._userID = userID
        self._title = title
        self._description = description
        self._startDateTime = startDateTime
        self._endDateTime = endDateTime
        self._category = category
        self._location = location
        self._comments = []
        self._invitees = []
        self._groups = []

    def getUserID(self):
        return self._userID

    def getTitle(self):
        return self._title

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

    def getGroups(self):
        return self._groups

    def setUser(self, user):
        self._user = user

    def setTitle(self, name):
        self._title = name

    def setEventID(self, ID):
        self._eventId = ID

    def setDescription(self, description):
        self._description = description

    def setStartDateTime(self, startDateTime):
        if startDateTime < self._endDataeTime:
            self._startDateTime = startDateTime

    def setEndDateTime(self, endDateTime):
        if endDateTime > self._startDateTime:
            self._endDateTime = endDateTime

    def setCategory(self, category):
        self._category = category

    def setLocation(self, location):
        self._location = location

    def setCategory(self, category):
        self._category = category

    def addComment(self, comment):
        self._comments.append(comment)

    def addInvitee(self, invitee):
        self._invitees.append(invitee)

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
    def editEvent(self, name, desc, startDateTime, endDateTime, category):
        # Update event details

        if startDateTime > endDateTime:
            return False
        self.setCategory(category)
        self.setTitle(name)
        self.setDescription(desc)
        self.setStartDateTime(startDateTime)
        self.setEndDateTime(endDateTime)
        return True

    def removeComment(self, comment):
        for comments in self._comments:
            # if the comment matches, and its the same poster, remove it
            if comment.getComment() == comments.getComment() and comment.getUser() == comments.getUser():
                self._comments.remove(comments)
            #recursion
            comments.deleteComment(comment)

    def calculateHoursCategory(self):
        dateTimeDifference = self.getEndDateTime() - self.getStartDateTime()
        return dateTimeDifference.total_seconds() / 3600
