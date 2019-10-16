import datetime
import pytest

from src.Calendar import Calendar
from src.Event import Event
from src.User import User


class TestEvent():
    @pytest.fixture()
    def fixture(self):
        self.user = User(1, "Derrick", "Foo", "derrick@gmail.com", "abc123")
        self.event = Event(1, 1, "COMP4920 Meeting", "Standup", datetime.datetime.now(), datetime.datetime.now(),
                           "Work")
        self.event1 = Event(2, 1, "21st Birthday", "Bday party at Sydney", datetime.datetime.now(),
                            datetime.datetime.now(), "Work")
        self.event_edit = Event(1, 1, "COMP4920 Meeting 2.0", "Online", datetime.datetime.now(),
                                datetime.datetime.now(), "Personal")
        self.workCal = Calendar("Work", "red", 1)
        self.workPersonal = Calendar("Personal", "blue", 1)
        self.user.addCalendars(self.workCal)

    def test_add_event(self, fixture):
        self.workCal.addEvent(self.event)
        assert (len(self.user.getCalendars()) == 1)
        assert (len(self.workCal.getEvents()) == 1)

    def test_add_same_event(self, fixture):
        self.workCal.addEvent(self.event)
        assert (len(self.workCal.getEvents()) == 1)
        self.workCal.addEvent(self.event)
        assert (len(self.workCal.getEvents()) == 1)

    def test_add_multiple_events(self, fixture):
        self.workCal.addEvent(self.event)
        assert (len(self.workCal.getEvents()) == 1)
        self.workCal.addEvent(self.event1)
        assert (len(self.workCal.getEvents()) == 2)

    def test_delete_events_when_none_exist(self, fixture):
        assert not (self.workCal.deleteEvent(self.event))

    def test_delete_event(self, fixture):
        self.workCal.addEvent(self.event)
        assert (len(self.workCal.getEvents()) == 1)
        self.workCal.deleteEvent(self.event)
        assert (len(self.workCal.getEvents()) == 0)
        assert not (self.workCal.deleteEvent(self.event))

    def test_delete_shared_event(self, fixture):
        self.user1 = User(2, "Zainab", "Alasadi", "zainab@gmail.com", "abc123***")
        self.workCal1 = Calendar("Work", "red", 2)
        self.user1.addCalendars(self.workCal1)

        self.workCal.addEvent(self.event)
        self.event.addInvitee(self.user1)
        self.workCal1.addEvent(self.event)

        self.workCal1.deleteEvent(self.event)

        assert (len(self.workCal.getEvents()) == 1)
        assert (len(self.workCal1.getEvents()) == 0)

        self.workCal1.addEvent(self.event)
        self.workCal.deleteEvent(self.event)

        assert (len(self.workCal.getEvents()) == 0)
        assert (len(self.workCal1.getEvents()) == 0)
