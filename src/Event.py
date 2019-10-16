class Event():

    def __init__(self, eventId, user, name, description, startDateTime, endDateTime, category):
        self._user = user
        self._name = name
        self._eventId = eventId
        self._description = description
        self._startDateTime = startDateTime
        self._endDateTime = endDateTime
        self._category = category
        self._comments = []
        self._invitees = []
        self._groups = []

    def get_user(self):
        return self._user

    def get_name(self):
        return self._name

    def get_ID(self):
        return self._eventId

    def get_description(self):
        return self._description

    def get_startDateTime(self):
        return self._startDateTime

    def get_endDateTime(self):
        return self._endDateTime

    def get_invitees(self):
        return self._invitees

    def get_category(self):
        return self._category

    def set_user(self, user):
        self._user = user

    def set_name(self, name):
        self._name = name

    def set_ID(self, ID):
        self._ID = ID

    def set_description(self, description):
        self._description = description

    def set_startDateTime(self, startDateTime):
        self._startDateTime = startDateTime

    def set_endDateTime(self, endDateTime):
        self._endDateTime = endDateTime

    def set_category(self, category):
        self._category = category

    def add_comment(self, comment):
        self._comments.append(comment)

    def add_invitee(self, invitee):
        self._invitees.append(invitee)

    # Returns true if invitee exists in event and is successfully removed
    def remove_invitee(self, invitee):
        try:
            self._invitees.remove(invitee)
            return True
        except:
            return False

    def add_group(self, group):
        self._groups.append(group)

    # Returns true if group exists in event and is successfully removed
    def remove_group(self, group):
        try:
            self._groups.remove(group)
            return True
        except:
            return False

    # Edits an event
    # Returns true if editing is successful, false if not
    def edit_event(self, name, desc, startDateTime, endDateTime, invitees):
        # Update event details

        if startDateTime > endDateTime:
            return False

        self.set_name(name)
        self.set_description(desc)
        self.set_startDateTime(startDateTime)
        self.set_endDateTime(endDateTime)

        return True
        # Add or delete invitees
        # TODO

