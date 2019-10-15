import datetime
import pytest

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
                  
    def test_event(self, fixture):
        assert (self.event.get_user() == 1)
        assert (self.event.get_category() == "Work")
        assert (self.event.get_description() == "Standup")
        assert (self.event.get_name() == "COMP4920 Meeting")
        assert (self.event.get_ID() == 1)
        assert (self.event.get_startDateTime() <= self.event.get_endDateTime())

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