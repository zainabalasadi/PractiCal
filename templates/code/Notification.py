# Implementation of PractiCalManager class
# Completed by Michael Ho
# Started 15/10/19
# Edited by Egene Oletu
# Last Modified 04/11/19


class Notification:
    NOTIF_EVENTCHANGE = 0
    NOTIF_EVENTINVITE = 1
    NOTIF_EVENTDELETE = 2
    NOTIF_INVITERESP_GOING = 3
    NOTIF_INVITERESP_MAYBE = 4
    NOTIF_INVITERESP_DECLINE = 5
    NOTIF_INVITERESP_NONE = 6

    def __init__(self, notifID, event, notifType, senderEmail):
        self._id = notifID
        self._event = event
        self._notifType = notifType
        self._senderEmail = senderEmail

    def getID(self):
        return self._id

    def getEvent(self):
        return self._event

    def getNotifType(self):
        return self._notifType

    def getSenderEmail(self):
        return self._senderEmail
