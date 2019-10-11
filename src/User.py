class User():

    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._events = []
    
    # adds a given event to a users calendar
    def add_event(self, event):
        self._events.append(event)

    # removes a given event from a users calendar
    def delete_event(self, event):
        self._events.remove(event)

    #edits a given event from a users calendar
    def edit_event(self, event):
        for old_event in self._events:
            if old_event.ID == event.ID:
                delete_event(old_event)
                add_event(event)
                return true
        return false
