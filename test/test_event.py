import datetime
import pytest

from src.Calendar import Calendar
from src.User import User
from src.Event import Event


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
        self.workCal = Calendar("Derrick", "red")
        self.workPersonal = Calendar("Derrick", "blue")
        self.user.addCalendars(self.workCal)
                  
    def test_event(self, fixture):
        assert (self.event.getUser() == 1)
        assert (self.event.getCategory() == "Work")
        assert (self.event.getDescription() == "Standup")
        assert (self.event.getName() == "COMP4920 Meeting")
        assert (self.event.getID() == 1)
        assert (self.event.getStartDateTime() <= self.event.getEndDateTime())

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