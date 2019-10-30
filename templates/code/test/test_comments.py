import datetime
import pytest

from templates.code.Calendar import Calendar
from templates.code.Comment import Comment
from templates.code.User import User
from templates.code.Event import Event


class TestComments():
    @pytest.fixture()
    def fixture(self):
        self.user = User(1, "Derrick", "Foo", "derrick@gmail.com", "abc123")
        self.user1 = User(2, "Zainab", "Alasadi", "zainab@gmail.com", "abc123***")
        self.event = Event(1, self.user, "COMP4920 Meeting", "Standup", datetime.datetime.now(),
                           datetime.datetime.now(),
                           "Work", "Work")
        self.event1 = Event(2, self.user, "21st Birthday", "Bday party at Sydney", datetime.datetime.now(),
                            datetime.datetime.now(), "Work", "Work")
        self.event_edit = Event(1, self.user, "COMP4920 Meeting 2.0", "Online", datetime.datetime.now(),
                                datetime.datetime.now(), "Personal", "Work")
        self.workCal = Calendar("Work", "red", self.user)
        self.workPersonal = Calendar("Personal", "blue", self.user)
        self.user.addCalendars(self.workCal)

        self.comment = Comment("Derrick", "So excited people!")
        self.comment1 = Comment("Derrick", "6pm don't be late!")
        self.commentReply = Comment("Zainab", "Cool")
        self.commentReply1 = Comment("Michael", "Me too!")

    def test_add_comment(self, fixture):
        self.event.addComment(self.comment)
        assert (len(self.event.getComments()) == 1)

    def test_add_two_parent_comments(self, fixture):
        self.event.addComment(self.comment)
        assert (len(self.event.getComments()) == 1)
        self.event.addComment(self.comment1)
        assert (len(self.event.getComments()) == 2)

    def test_add_nested_comments(self, fixture):
        self.event.addComment(self.comment)
        assert (len(self.event.getComments()) == 1)
        for comment in self.event.getComments():
            comment.replyToComment(self.commentReply)
            assert (len(comment.getReplies()) == 1)
        assert (len(self.event.getComments()) == 1)

    def test_remove_comment(self, fixture):
        self.event.addComment(self.comment)
        assert (len(self.event.getComments()) == 1)
        self.event.removeComment(self.comment)
        assert (len(self.event.getComments()) == 0)

    def test_remove_child_comment(self, fixture):
        self.event.addComment(self.comment)
        for comment in self.event.getComments():
            comment.replyToComment(self.commentReply)
            assert (len(comment.getReplies()) == 1)
        self.event.removeComment(self.commentReply)

        assert (len(self.event.getComments()) == 1)

        for comment in self.event.getComments():
            assert (len(comment.getReplies()) == 0)

    def test_remove_parent_with_children(self, fixture):
        self.event.addComment(self.comment)
        for comment in self.event.getComments():
            comment.replyToComment(self.commentReply)
        self.event.removeComment(self.comment)
        assert(len(self.event.getComments()) == 0)
