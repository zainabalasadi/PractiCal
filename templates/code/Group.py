class Group():

    def __init__(self, name):
        self._name = name
        self._members = []
        self._events = []

    def getMembers(self):
        return self._members

    def addMember(self, member):
        if member not in self.getMembers():
            self._members.append(member)

        #TODO
        #send them notif of all events

    def removeMember(self, member):
        if member in self.getMembers():
            self._members.remove(member)

        #TODO
        #also remove their invittations

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getEvents(self):
        return self._events

    def addEvent(self, event):
        if event not in self.getEvents():
            self._events.append(event)

            for user in self.getMembers():
                user.addNotification()

        # TODO
        #also invite everyone in group

    def removeEvent(self, event):
        if event in self.getEvents():
            self._events.remove(event)

            for user in self.getMembers():
                for calendar in user.getCalendars():
                    if event in calendar.getEvents():
                        calendar.deleteEvent(event)

                for notif in user.getNotifications():
                    if notif.getEvent() == event:
                        user.removeNotification(notif)
        #TODO
        #also remove notifs/event in everyone in group

    def updateNotifications(self):
        return