class Group:

    def __init__(self, name):
        self._name = name
        self._members = dict()

    def getMembers(self):
        ret = []
        for email in self._members.keys():
            ret.append((email, self._members[email]['firstName'],
                self._members[email]['lastName']))
        return ret

    def addMember(self, email, name):
        try:
            mem = self._members[email]
            return
        except:
            self._members[email] = {'name': name}

    def removeMember(self, email):
        try:
            del self._members[email]
        except:
            pass

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
