class Group:

    def __init__(self, name):
        self._name = name
        self._members = []

    def getMembers(self):
        return self._members

    def addMember(self, member):
        if member not in self.getMembers():
            self._members.append(member)

    def removeMember(self, member):
        if member in self.getMembers():
            self._members.remove(member)

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
