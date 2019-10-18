import datetime
import pytest

from src.code.Calendar import Calendar
from src.code.Event import Event
from src.code.User import User


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
        self.personalCal = Calendar("Personal", "blue", 1)
        self.user.addCalendars(self.workCal)

    def test_add_comment(self, fixture):
        self.event