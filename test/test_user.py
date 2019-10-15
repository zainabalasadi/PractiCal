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
        assert (self.user.get_id() == 1)
        assert (self.user.get_firstName() == "Derrick")
        assert (self.user.get_lastName() == "Foo")
        assert (self.user.get_email() == "derrick@gmail.com")
        assert (self.user.validate("abc123") == True)
        assert (len(self.user.get_categories()) == 0)
        assert (len(self.user.get_contacts()) == 0)
        assert (len(self.user.get_groups()) == 0)