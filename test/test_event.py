import datetime
import pytest

from src.code.Calendar import Calendar
from src.code.Comment import Comment
from src.code.User import User
from src.code.Event import Event


class TestEvent():
    @pytest.fixture()
    def fixture(self):
        self.user = User(1, "Derrick", "Foo", "derrick@gmail.com", "abc123")
        self.event = Event(1, 1, "COMP4920 Meeting", "Standup", datetime.datetime.now(),
                           datetime.datetime.now(), "Work")
        self.event1 = Event(2, 1, "21st Birthday", "Bday party at Sydnney", 
                            datetime.datetime.now(), datetime.datetime.now(), "Work")
        self.event_edit = Event(1, 1, "COMP4920 Meeting 2.0", "Online", datetime.datetime.now(),
                                datetime.datetime.now(), "Personal")
        self.workCal = Calendar("Work", "red", 1)
        self.workPersonal = Calendar("Personal", "blue", 1)
        self.user.addCalendars(self.workCal)

        self.comment = Comment("Derrick", "So excited people!")
        self.comment1 = Comment("Derrick", "6pm don't be late!")
        self.commentReply = Comment("Zainab", "Cool")
        self.commentReply1 = Comment("Michael", "Me too!")

    def test_event(self, fixture):
        assert (self.event.getUser() == 1)
        assert (self.event.getCalendar() == "Work")
        assert (self.event.getDescription() == "Standup")
        assert (self.event.getName() == "COMP4920 Meeting")
        assert (self.event.getID() == 1)
        assert (self.event.getStartDateTime() <= self.event.getEndDateTime())

    def test_edit_event(self, fixture):
        self.workCal.addEvent(self.event)
        self.event.editEvent("COMP4920 Meeting 2.0", "Online", datetime.datetime.now(), datetime.datetime.now(),
                             self.event.getInvitees())
        for event in self.workCal.getEvents():
            assert (event.getName() == "COMP4920 Meeting 2.0")
        assert (len(self.workCal.getEvents()) == 1)

    def test_bad_date_edit_event(self, fixture):
        self.workCal.addEvent(self.event)
        self.event.editEvent("COMP4920 Meeting 2.0", "Online", datetime.date(2012, 12, 31), datetime.date(2001, 12, 31)
                              , self.event.getInvitees())
        for event in self.workCal.getEvents():
            assert (event.getName() == "COMP4920 Meeting")
        assert (len(self.workCal.getEvents()) == 1)

    def test_add_comment(self, fixture):
        self.event.addComment("So excited people!")
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
