import datetime
import pytest

from templates.code.Calendar import Calendar
from templates.code.Event import Event
from templates.code.Notification import Notification
from templates.code.User import User


class TestUser():
    @pytest.fixture()
    def fixture(self):
        self.user = User(1, "Derrick", "Foo", "derrick@gmail.com", "abc123")
        self.user1 = User(2, "Zainab", "Alasadi", "zainab@gmail.com", "abc123***")

        self.event = Event(1, self.user, "COMP4920 Meeting", "Standup", datetime.datetime(2017, 11, 28, 22, 45),
                           datetime.datetime(2017, 11, 28, 23, 45), "Work", "Work")
        self.event1 = Event(2, self.user, "21st Birthday", "Bday party at Sydney",
                            datetime.datetime(2017, 11, 28, 22, 45), datetime.datetime(2017, 11, 28, 23, 45), "Work",
                            "Work")
        self.event_edit = Event(1, self.user, "COMP4920 Meeting 2.0", "Online", datetime.datetime.now(),
                                datetime.datetime.now(), "Personal", "Work")
        self.workCal = Calendar("Work", "red", self.user)
        self.personalCal = Calendar("Personal", "blue", self.user1)

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

    def test_category_hours(self, fixture):
        self.user.addCalendars(self.workCal)
        assert (self.user.calculateHoursCategory("Work") == 1)

    def test_category_hours_multiple_calendars(self, fixture):
        self.user.addCalendars(self.workCal)
        self.personalCal.addEvent(self.event1)
        self.user.addCalendars(self.personalCal)
        assert (self.user.calculateHoursCategory("Work") == 2)
