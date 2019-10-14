import datetime
import pytest

from src.User import User
from src.event import Event


class TestEvent():

    @pytest.fixture()
    def fixture(self):
        self.user = User("Derrick", "abc123")
        self.event = Event("Derrick", "COMP4920 Meeting", 1, "Standup", datetime.datetime.now(),
                           datetime.datetime.now(),
                           "Work")
        self.event1 = Event("Derrick", "21st Birthday", 2, "Henry", datetime.datetime.now(), datetime.datetime.now(),
                            "Personal")
        self.event_edit = Event("Michael", "COMP4920 Meeting 2.0", 1, "Online", datetime.datetime.now(),
                                datetime.datetime.now(), "Personal")
        self.event_bad_edit = Event("Michael", "COMP4920 Meeting 2.0", 2, "Online", datetime.datetime.now(),
                                    datetime.datetime.now(), "Personal")

    def test_event(self, fixture):
        assert (self.event.get_user() == "Derrick")
        assert (self.event.get_category() == "Work")
        assert (self.event.get_description() == "Standup")
        assert (self.event.get_name() == "COMP4920 Meeting")
        assert (self.event.get_ID() == 1)
        assert (self.event.get_startDateTime() <= self.event.get_endDateTime())

    def test_user(self, fixture):
        assert (len(self.user.get_events()) == 0)
        assert (self.user.get_password() == "abc123")
        assert (self.user.get_username() == "Derrick")

    def test_add_event(self, fixture):
        self.user.add_event(self.event)
        assert (len(self.user.get_events()) == 1)

    def test_add_same_event(self, fixture):
        self.user.add_event(self.event)
        assert (len(self.user.get_events()) == 1)
        self.user.add_event(self.event)
        assert (len(self.user.get_events()) == 1)

    def test_add_multiple_events(self, fixture):
        self.user.add_event(self.event)
        assert (len(self.user.get_events()) == 1)
        self.user.add_event(self.event1)
        assert (len(self.user.get_events()) == 2)

    def test_delete_events_when_none_exist(self, fixture):
        assert not (self.user.delete_event(self.event))

    def test_delete_event(self, fixture):
        self.user.add_event(self.event)
        assert (len(self.user.get_events()) == 1)
        self.user.delete_event(self.event)
        assert (len(self.user.get_events()) == 0)
        assert not (self.user.delete_event(self.event))

    def test_edit_event(self, fixture):
        self.user.add_event(self.event)
        self.user.edit_event(self.event_edit)
        for event in self.user.get_events():
            assert (event.get_user() == "Michael")
        assert (len(self.user.get_events()) == 1)

    def test_bad_edit_event(self, fixture):
        self.user.add_event(self.event)
        self.user.edit_event(self.event_bad_edit)
        for event in self.user.get_events():
            assert event.get_user() == "Derrick"
        assert (len(self.user.get_events()) == 1)