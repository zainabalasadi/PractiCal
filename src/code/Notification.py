# Implementation of PractiCalManager class
# Completed by Michael Ho
# Started 15/10/19

class Notification():
    def __init__(self, event, notifType, invoker, receiver):
        self._event = event
        self._notifType = notifType
        self._invoker = invoker
        self._receiver = receiver

    def getEvent(self):
        return self._event

    def getNotifType(self):
        return self._notifType

    def getStatus(self):
        return self._status

    def getInvoker(self):
        return self._invoker

    def getReceiver(self):
        return self._receiver
