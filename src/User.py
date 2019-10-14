# Implementation of User class
# Completed by Zainab Alasadi
# Started 13/10/19

class User():
    def __init__(self, userId, firstName, lastName, email, password):
        self._id = userId
        self._firstName = firstName
        self._lastName = lastName
        self._email = email
        self._password = password
        self._category = []
    
    def get_id(self):
        return str(self.id)

    def get_firstName(self):
        return self._firstName

    def get_email(self):
        return self._email

    def get_password(self):
        return self._password
    
    def get_events(self):
        return self._events
    
    def get_categories(self):
        return self._calendars

    def add_categories(self, newCalendar):
        self._calendars.append(newCalendar)

    # Validate if provided password matches user password
    def validate(self, password):
        return self._password == password
