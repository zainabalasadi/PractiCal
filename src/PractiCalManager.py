# Implementation of PractiCalManager class
# Completed by Michael Ho
# Started 15/10/19

from src.User import User
from src.Category import Category

class PractiCalManager():
	def __init__(self):
		self._users = []
		
	def get_users(self):
		return self._users

	# Returns true if new user is successfully created
	def create_user(self, userId, firstName, lastName, email, password):
		if self.search_user_email() == None:
			new_user = User(userId, firstName, lastName, email, password)
			default_category = Category('My Calendar', 'Red')
			new_user.add_categories(default_category)
			self._users.append(new_user)
			return True
		else:
			return False

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

	# Returns matching user if exists
	def search_user_email(self, email):
		for user in self.users:
			if user.get_email() == email:
				return user
		return None