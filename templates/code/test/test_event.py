import datetime
import pytest

from templates.code.Calendar import Calendar
from templates.code.Comment import Comment
from templates.code.User import User
from templates.code.Event import Event


class TestEvent():
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
        self.personalCal = Calendar("Personal", "blue", self.user)
        self.user.addCalendars(self.workCal)

        self.event.setCalendar(self.workCal)

        self.comment = Comment("Derrick", "So excited people!")
        self.comment1 = Comment("Derrick", "6pm don't be late!")
        self.commentReply = Comment("Zainab", "Cool")
        self.commentReply1 = Comment("Michael", "Me too!")

    def test_event(self, fixture):
        assert (self.event.getUser() == self.user)
        assert (self.event.getCalendar() == self.workCal)
        assert (self.event.getDescription() == "Standup")
        assert (self.event.getName() == "COMP4920 Meeting")
        assert (self.event.getID() == 1)
        assert (self.event.getStartDateTime() <= self.event.getEndDateTime())

    def test_edit_event(self, fixture):
        self.workCal.addEvent(self.event)
        self.event.editEvent("COMP4920 Meeting 2.0", "Online", datetime.datetime.now(), datetime.datetime.now(),
                             self.workCal, "Work")
        for event in self.workCal.getEvents():
            assert (event.getName() == "COMP4920 Meeting 2.0")
        assert (len(self.workCal.getEvents()) == 1)

    def test_edit_event_change_calendar(self, fixture):
        self.workCal.addEvent(self.event)
        self.event.editEvent("COMP4920 Meeting 2.0", "Online", datetime.datetime.now(), datetime.datetime.now(),
                             self.personalCal, "Work")

        assert (len(self.workCal.getEvents()) == 0)
        assert (len(self.personalCal.getEvents()) == 1)

    def test_bad_date_edit_event(self, fixture):
        self.workCal.addEvent(self.event)
        self.event.editEvent("COMP4920 Meeting 2.0", "Online", datetime.date(2012, 12, 31), datetime.date(2001, 12, 31)
                             , self.workCal, "Work")
        for event in self.workCal.getEvents():
            assert (event.getName() == "COMP4920 Meeting")
        assert (len(self.workCal.getEvents()) == 1)

    def test_add_invitee(self, fixture):
        self.event.addInvitee(self.user1)
        assert (len(self.user1.getNotifications()) == 1)
        for notif in self.user1.getNotifications():
            assert (notif.getNotifType() == 'invite')

    def test_remove_invitee_has_not_accepted(self, fixture):
        self.event.addInvitee(self.user1)
        self.event.removeInvitee(self.user1)

        assert (len(self.user1.getNotifications()) == 0)

    def test_remove_invitee_who_has_accepted(self, fixture):
        self.event.addInvitee(self.user1)

        self.workCal1 = Calendar("Work", "red", self.user1)
        self.user1.addCalendars(self.workCal1)

        for notif in self.user1.getNotifications():
            self.user1.acceptInvite(notif, self.workCal1)

        assert (len(self.workCal1.getEvents()) == 1)

        self.event.removeInvitee(self.user1)

        assert (len(self.workCal1.getEvents()) == 0)
        assert (len(self.user1.getNotifications()) == 0)
