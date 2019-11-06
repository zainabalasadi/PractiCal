from PractiCalManager import PractiCalManager

pm = PractiCalManager("practiCal_db", "localhost", "admin", "password")
print("Running tests on PractiCalManager module...")

# Test loginUser
print("Testing loginUser method...", end="")
user1 = pm.loginUser("egene.o@email.com", "password")
assert user1, "Test failed: User 1 not logged in"
cals = user1.getCalendars()
assert len(cals) == 2, "Test failed: Failed to load calendars"
for cal in cals:
    if cal.getName() == "Calendar1":
        assert len(cal.getEvents()) == 3, \
            "Test failed: Failed to load calendar 1 events"
    elif cal.getName() == "Calendar2":
        assert len(cal.getEvents()) == 2, \
            "Test failed: Failed to load calendar 2 events"
print("Passed")

# Test addUser
print("Testing addUser method...", end="")
assert pm.addUser("Test", "User", "test.user@email.com", "password"), \
    "Test failed: Test user not created"
user2 = pm.loginUser("test.user@email.com", "password")
assert user2, "Test failed: New user not logged in"
print("Passed")

# Test addEvent
print("Testing addEvent method...", end="")
event1 = pm.addEvent(user1.getID(), "Test event title", "Test event description",
    "default", "2019-11-06 12:00:00", "2019-11-07 12:00:00")
assert event1, "Test failed: Test event not created"
print("Passed")

# Test sendInvite
print("Testing sendInvite method...", end="")
pm.sendInvite(event1.getID(), user1.getID(),
    ['zainab.a@email.com', 'michael.h@email.com'])
user3 = pm.loginUser("zainab.a@email.com", "password")
assert user3 and event1 in user3.getInvites(), \
    "Test failed: User3 didnt get invite to event1 from user1"
event2 = pm.addEvent(user1.getID(), "Test event title 2", "Test event description 2",
    "default", "2019-11-06 12:00:00", "2019-11-07 12:00:00")
pm.sendInvite(event2.getID(), user1.getID(), ["zainab.a@email.com"])
assert event2 in user3.getInvites(), \
    "Test failed: User3 didnt get invite to event2 from user1"
print("Passed")

# Test send

# Test logoutUser
print("Testing logoutUser method...", end="")
assert pm.logoutUser(user1.getID()), "Test failed: User1 not logged out"
print("Passed")
