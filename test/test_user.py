import datetime
import pytest

from src.code.Calendar import Calendar
from src.code.Event import Event
from src.code.Notification import Notification
from src.code.User import User


class TestUser():
    @pytest.fixture()
    def fixture(self):
        self.user = User(1, "Derrick", "Foo", "derrick@gmail.com", "abc123")
        self.user1 = User(2, "Zainab", "Alasadi", "zainab@gmail.com", "abc123***")

        self.event = Event(1, self.user, "COMP4920 Meeting", "Standup", datetime.datetime.now(), datetime.datetime.now(),
                           "Work")
        self.event1 = Event(2, self.user, "21st Birthday", "Bday party at Sydney", datetime.datetime.now(),
                            datetime.datetime.now(), "Work")
        self.event_edit = Event(1, 1, "COMP4920 Meeting 2.0", "Online", datetime.datetime.now(),
                                datetime.datetime.now(), "Personal")
        self.workCal = Calendar("Work", "red", 1)
        self.personalCal = Calendar("Personal", "blue", 1)

        self.event.addInvitee(self.user1)
        self.workCal.addEvent(self.event)
        self.user1.addCalendars(self.personalCal)

    def test_user(self, fixture):
        assert (self.user.getID() == 1)
        assert (self.user.getFirstName() == "Derrick")
        assert (self.user.getLastName() == "Foo")
        assert (self.user.getEmail() == "derrick@gmail.com")
        assert (self.user.validate("abc123") == True)
        assert (len(self.user.getCalendars()) == 0)
        assert (len(self.user.getContacts()) == 0)
        assert (len(self.user.getGroups()) == 0)

    def test_accept_invite(self, fixture):
        #HELP
        for notif in self.user1.getNotifications():
            self.user1.acceptInvite(notif, self.personalCal)
        assert (len(self.user1.getNotifications()) == 0)
        assert (len(self.personalCal.getEvents()) == 1)

    def test_maybe_invite(self, fixture):
        return

    def test_decline_invite(self, fixture):
        for notif in self.user1.getNotifications():
            self.user1.declineInvite(notif)
        assert (len(self.user1.getNotifications()) == 0)
        assert (len(self.personalCal.getEvents()) == 0)
        assert (len(self.user.getNotifications()) == 1)
