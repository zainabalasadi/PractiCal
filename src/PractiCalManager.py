# Implementation of PractiCalManager class
# Completed by Michael Ho
# Started 15/10/19
import User

class PractiCalManager():
	def __init__():
		self._users = []
		
	def get_users(self):
		return self._users

	def create_user(self, userId, firstName, lastName, email, password):
		new_user = User(userId, firstName, lastName, email, password)
		self._users.append(new_user)

	# Return true if user exists and is successfully removed from system	
	def remove_user(self, user):
		try:
			self._users.remove(user)
			return True
		except:
			return False

	# Returns list of matching users
	def search_user_name(self, firstName, lastName):
		matching_users = []
		for user in self._users:
			if user.get_firstName() == firstName and user.get_lastName() == lastName:
				matching_users.append(user)
		return matching_users

	# Returns list of matching users
	def search_user_email(self, email):
		matching_users = []
		for user in self.users:
			if user.get_email() == email:
				matching_users.append(user)
		return matching_users