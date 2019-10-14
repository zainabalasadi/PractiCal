# Implementation of Category class
# Completed by Zainab Alasadi
# Started 13/10/19

class Category():
    def __init__(self, name, colour):
        self._name = name
        self._colour = colour
        self._events = []
    
    def get_name(self):
        return self._name

    def get_colour(self):
        return self._colour

	def get_events(self):
		return self._events

    # Adds an event to a user's calendar
    def add_event(self, event):
        #assert start date < end date
        #try:
            #check_dates
        if event not in self.get_events():
            self._events.append(event)
            return True
        return False

    # Removes a given event from a user's calendar
    def delete_event(self, event):
        #if the thing is shared, remove from everyone's calendar
        if event in self.get_events():
            self._events.remove(event)
            return True
        return False

    # Edits a given event from in a user's calendar
    def edit_event(self, event):
        for old_event in self._events:
            if old_event.get_ID() == event.get_ID():
                if self.add_event(event):
                    self.delete_event(old_event)
                    return True
        return False
