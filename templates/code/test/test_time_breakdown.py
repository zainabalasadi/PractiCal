import datetime
import pytest

from templates.code.Calendar import Calendar
from templates.code.Event import Event
from templates.code.User import User


class TestTimeBreakdown():
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

        self.workCal.addEvent(self.event)
        self.user.addCalendars(self.workCal)

    def test_category_hours(self, fixture):
        assert (self.user.calculateHoursCategory("Work", datetime.datetime(2017, 11, 27, 22, 45)) == 1)

    def test_category_hours_multiple_calendars(self, fixture):
        self.personalCal.addEvent(self.event1)
        self.user.addCalendars(self.personalCal)
        assert (self.user.calculateHoursCategory("Work", datetime.datetime(2017, 11, 27, 22, 45)) == 2)

    def test_category_hours_diff_weeks(self, fixture):
        self.workCal.addEvent(self.event_edit)
        assert (self.user.calculateHoursCategory("Work", datetime.datetime(2017, 11, 27, 22, 45)) == 1)

    def test_category_hours_multiple(self, fixture):
        self.workCal.addEvent(self.event1)
        assert (self.user.calculateHoursCategory("Work", datetime.datetime(2017, 11, 27, 22, 45)) == 2)