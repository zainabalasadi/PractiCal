# Implementation of PractiCalManager class
# Completed by Michael Ho
# Started 15/10/19

class Notification():
	def __init__(self, event, notifType):
		self._event = event
		self._notifType = notifType
		self._status = 'Sent'
		self._invoker = _invoke
		self._receiver = _receiver

	def get_event(self):
		return self._event

	def get_notifType(self):
		return self._notifType

	def get_status(self):
		return self._status

	def get._invoker(self):
		return self._invoker

	def get._receiver(self):
		return self._receiver

	# Status values: 'Sent', 'Seen'
	def set_status(self, new_status):
		self._status = new_status
