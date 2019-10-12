class User():

    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._events = []
    
    def get_events(self):
        return self._events

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    # adds a given event to a users calendar
    def add_event(self, event):
        #assert start date < end date
        #try:
            #check_dates
        if event not in self.get_events():
            self._events.append(event)
            return True
        return False

    # removes a given event from a users calendar
    def delete_event(self, event):
        #if the thing is shared, remove from everyone's calendar
        if event in self.get_events():
            self._events.remove(event)
            return True
        return False

    #edits a given event from a users calendar
    def edit_event(self, event):
        for old_event in self._events:
            if old_event.get_ID() == event.get_ID():
                if self.add_event(event):
                    self.delete_event(old_event)
                    return True
        return False
