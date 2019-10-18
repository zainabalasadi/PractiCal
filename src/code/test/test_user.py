import datetime
import pytest

from src.User import User
from src.Event import Event


class TestUser():
    @pytest.fixture()
    def fixture(self):
        self.user = User(1, "Derrick", "Foo", "derrick@gmail.com", "abc123")
        self.user1 = User(2, "Zainab", "Alasadi", "zainab@gmail.com", "abc123***")

    def test_user(self, fixture):
        assert (self.user.getID() == 1)
        assert (self.user.getFirstName() == "Derrick")
        assert (self.user.getLastName() == "Foo")
        assert (self.user.getEmail() == "derrick@gmail.com")
        assert (self.user.validate("abc123") == True)
        assert (len(self.user.getCalendars()) == 0)
        assert (len(self.user.getContacts()) == 0)
        assert (len(self.user.getGroups()) == 0)
