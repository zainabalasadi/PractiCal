# Implementation of PractiCalManager class
# Completed by Michael Ho
# Started 15/10/19
# Edited by Egene Oletu
# Last Modified 04/11/19


class Notification():
    NOTIF_EVENTCHANGE = 0
    NOTIF_EVENTINVITE = 1
    NOTIF_INVITERESP_GOING = 2
    NOTIF_INVITERESP_MAYBE = 3
    NOTIF_INVITERESP_DECLINE = 4
    NOTIF_INVITERESP_NONE = 5

    def __init__(self, event, notifType, senderID):
        self._event = event
        self._notifType = notifType
        self._senderID = senderID

    def getEvent(self):
        return self._event

    def getNotifType(self):
        return self._notifType

    def getSenderID(self):
        return self._senderID
