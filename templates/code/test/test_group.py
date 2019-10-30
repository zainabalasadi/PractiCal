import pytest

from templates.code.Group import Group
from templates.code.User import User


class TestGroup():
    @pytest.fixture()
    def fixture(self):
        self.user = User(1, "Derrick", "Foo", "derrick@gmail.com", "abc123")
        self.user1 = User(2, "Zainab", "Alasadi", "zainab@gmail.com", "abc123***")
        self.group = Group("Work")

    def test_add_member_to_group(self, fixture):
        self.group.addMember(self.user)
        assert (len(self.group.getMembers()) == 1)
        self.group.addMember(self.user1)
        assert (len(self.group.getMembers()) == 2)

    def test_add_same_member_twice(self, fixture):
        self.group.addMember(self.user)
        assert (len(self.group.getMembers()) == 1)
        self.group.addMember(self.user)
        assert (len(self.group.getMembers()) == 1)

    def test_delete_member(self, fixture):
        self.group.addMember(self.user)
        assert (len(self.group.getMembers()) == 1)
        self.group.removeMember(self.user)
        assert (len(self.group.getMembers()) == 0)

    def test_delete_member_when_none(self, fixture):
        self.group.removeMember(self.user)
        assert (len(self.group.getMembers()) == 0)

    def test_add_same_member_diff_groups(self, fixture):
        self.group.addMember(self.user)
        self.group1 = Group("Friends")
        self.group1.addMember(self.user)

        assert (len(self.group.getMembers()) == 1)
        assert (len(self.group1.getMembers()) == 1)
