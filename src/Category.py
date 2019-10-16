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
        return str(self._colour)

    def get_events(self):
        return self._events

    # Adds an event to a user's calendar
    # Returns true if addition is successful, false if not
    def add_event(self, event):
        if event not in self.get_events():
            self._events.append(event)
            return True
        return False

    # Removes a given event from a user's calendar
    # Returns true if removal is successful, false if not
    def delete_event(self, event):
        # TODO
        # If the event is shared, remove from everyone's calendar
        if event in self.get_events():
            self._events.remove(event)
            return True
        return False
