import datetime
import pytest

from templates.code.Calendar import Calendar
from templates.code.Event import Event
from templates.code.User import User


class TestCalendar():
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

        self.event.setCalendar(self.workCal)

    def test_add_event(self, fixture):
        assert (self.workCal.addEvent(self.event))
        assert (len(self.user.getCalendars()) == 1)
        assert (len(self.workCal.getEvents()) == 1)

    def test_add_same_event_same_calendar(self, fixture):
        assert (self.workCal.addEvent(self.event))
        assert (len(self.workCal.getEvents()) == 1)
        assert not (self.workCal.addEvent(self.event))
        assert (len(self.workCal.getEvents()) == 1)

    def test_add_same_event_diff_calendars(self, fixture):
        assert (self.workCal.addEvent(self.event))
        assert (len(self.workCal.getEvents()) == 1)
        assert (self.personalCal.addEvent(self.event))
        self.user.addCalendars(self.personalCal)
        assert (len(self.personalCal.getEvents()) == 1)

    def test_add_multiple_events(self, fixture):
        assert (self.workCal.addEvent(self.event))
        assert (len(self.workCal.getEvents()) == 1)
        assert (self.workCal.addEvent(self.event1))
        assert (len(self.workCal.getEvents()) == 2)

    def test_delete_events_when_none_exist(self, fixture):
        assert not (self.workCal.deleteEvent(self.event))

    def test_delete_event(self, fixture):
        assert (self.workCal.addEvent(self.event))
        assert (len(self.workCal.getEvents()) == 1)
        assert (self.workCal.deleteEvent(self.event))
        assert (len(self.workCal.getEvents()) == 0)
        assert not (self.workCal.deleteEvent(self.event))

    def test_delete_event_diff_calendars(self, fixture):
        assert (self.workCal.addEvent(self.event))
        assert (len(self.workCal.getEvents()) == 1)
        assert (self.personalCal.addEvent(self.eventCopy))
        self.user.addCalendars(self.personalCal)
        assert (len(self.personalCal.getEvents()) == 1)

        self.user.deleteEvent(self.event)
        assert (len(self.personalCal.getEvents()) == 1)
        assert (len(self.workCal.getEvents()) == 0)

    def test_delete_event_all_calendars(self, fixture):
        assert (self.workCal.addEvent(self.event))
        assert (len(self.workCal.getEvents()) == 1)
        assert (self.personalCal.addEvent(self.event))
        self.user.addCalendars(self.personalCal)
        assert (len(self.personalCal.getEvents()) == 1)

        self.user.deleteEvent(self.event)
        assert (len(self.personalCal.getEvents()) == 0)
        assert (len(self.workCal.getEvents()) == 0)

    def test_delete_all_when_none(self, fixture):
        self.user.deleteEvent(self.event)
        assert (len(self.personalCal.getEvents()) == 0)
        assert (len(self.workCal.getEvents()) == 0)

    def test_delete_event_one_calendar(self, fixture):
        assert (self.workCal.addEvent(self.event))
        assert (len(self.workCal.getEvents()) == 1)
        self.event.setCalendar(self.workCal)
        assert (self.personalCal.addEvent(self.eventCopy))
        self.user.addCalendars(self.personalCal)
        self.eventCopy.setCalendar(self.personalCal)
        assert (len(self.personalCal.getEvents()) == 1)

        assert (self.user.deleteEventOneCalendar(self.event))
        assert (len(self.personalCal.getEvents()) == 1)
        assert (len(self.workCal.getEvents()) == 0)

    def test_delete_one_when_none(self, fixture):
        self.user.deleteEventOneCalendar(self.event)
        assert (len(self.personalCal.getEvents()) == 0)
        assert (len(self.workCal.getEvents()) == 0)
