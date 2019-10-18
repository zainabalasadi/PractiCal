class Comment():

    def __init__(self, user, parent):
        self._user = user
        self._parent = parent
        self._children = []

    def getUser(self):
        return self._user

    def getComment(self):
        return self._parent

    def getReplies(self):
        return self._children

    def replyToComment(self, comment):
        self._children.append(comment)

    def deleteComment(self, comment):
        if comment.getComment() == self.getComment() and comment.getUser() == self.getUser():
            return True
        for comments in self._children:
            if comments.deleteComment(comment):
                self._children.remove(comments)
        return False
