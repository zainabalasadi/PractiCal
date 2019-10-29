import datetime
import pytest

from templates.code.Calendar import Calendar
from templates.code.Event import Event
from templates.code.User import User


class TestNotification():
    @pytest.fixture()
    def fixture(self):
        self.user = User(1, "Derrick", "Foo", "derrick@gmail.com", "abc123")
        self.event = Event(1, self.user, "COMP4920 Meeting", "Standup", datetime.datetime.now(),
                           datetime.datetime.now(), "Work", "Work")
        self.eventCopy = Event(1, self.user, "COMP4920 Meeting", "Standup", datetime.datetime.now(),
                               datetime.datetime.now(), "Personal", "Work")
        self.event1 = Event(2, self.user, "21st Birthday", "Bday party at Sydney", datetime.datetime.now(),
                            datetime.datetime.now(), "Work", "Work")
        self.event_edit = Event(1, self.user, "COMP4920 Meeting 2.0", "Online", datetime.datetime.now(),
                                datetime.datetime.now(), "Personal", "Work")
        self.workCal = Calendar("Work", "red", self.user)
        self.personalCal = Calendar("Personal", "blue", self.user)
        self.user.addCalendars(self.workCal)

    def test_delete_accepted_shared_event_invitee(self, fixture):
        self.user1 = User(2, "Zainab", "Alasadi", "zainab@gmail.com", "abc123***")
        self.workCal1 = Calendar("Work", "red", self.user1)
        self.user1.addCalendars(self.workCal1)

        self.workCal.addEvent(self.event)
        self.event.addInvitee(self.user1)

        assert (len(self.user1.getNotifications()) == 1)
        assert (len(self.event.getInvitees()) == 1)

        for notif in self.user1.getNotifications():
            self.user1.acceptInvite(notif, self.workCal1)

        assert (len(self.user1.getNotifications()) == 0)

        self.user1.deleteEvent(self.event)

        assert (len(self.workCal.getEvents()) == 1)
        assert (len(self.workCal1.getEvents()) == 0)
        assert (len(self.user1.getNotifications()) == 0)
        assert (len(self.user.getNotifications()) == 0)

    def test_delete_accepted_shared_event_creator(self, fixture):
        self.user1 = User(2, "Zainab", "Alasadi", "zainab@gmail.com", "abc123***")
        self.workCal1 = Calendar("Work", "red", self.user1)
        self.user1.addCalendars(self.workCal1)

        self.workCal.addEvent(self.event)
        self.event.addInvitee(self.user1)

        for notif in self.user1.getNotifications():
            self.user1.acceptInvite(notif, self.workCal1)

        self.user.deleteEvent(self.event)

        assert (len(self.workCal.getEvents()) == 0)
        assert (len(self.workCal1.getEvents()) == 0)
        assert (len(self.user1.getNotifications()) == 1)
        for notif in self.user1.getNotifications():
            assert (notif.getNotifType() == 'deleted_event')

    def test_delete_unaccepted_shared_event_creator(self, fixture):
        self.user1 = User(2, "Zainab", "Alasadi", "zainab@gmail.com", "abc123***")
        self.workCal1 = Calendar("Work", "red", self.user1)
        self.user1.addCalendars(self.workCal1)

        self.workCal.addEvent(self.event)
        self.event.addInvitee(self.user1)

        self.user.deleteEvent(self.event)

        assert (len(self.workCal.getEvents()) == 0)
        assert (len(self.workCal1.getEvents()) == 0)
        assert (len(self.user1.getNotifications()) == 0)
