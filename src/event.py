class Event():

    def __init__(self, user, name, ID, description, startDateTime, endDateTime, category):
        self._user = user
        self._name = name
        self._ID = ID
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
        return self._ID
        
    def get_description(self):
        return self._description
    
    def get_startDateTime(self):
        return self._startDateTime
        
    def get_endDateTime(self):
        return self._endDateTime
    
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

    def add_invitees(self, invitee):
        self._invitees.append(invitee)

    def remove_invitees(self, invitee):
        # TODO
        return true

    def add_group(self, group):
        self._groups.append(group)

    def remove_group(self, invitee):
        # TODO
        return true

    # Edits an event
    # Returns true if editing is successful, false if not
    def edit_event(self, name, desc, startDateTime, endDateTime, invitees):
        # Update event details
        self.setName(name) 
        self.set_description(desc) 
        self.set_startDateTime(startDateTime) 
        self.set_endDateTime(endDateTime)
        # Add or delete invitees
        # TODO

