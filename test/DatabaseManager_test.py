from contextlib import redirect_stdout
import io
import importlib.util
spec = importlib.util.spec_from_file_location("DatabaseManager",
    "../templates/DatabaseManager.py")
DM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(DM)

dm = DM.DatabaseManager("test_db", "localhost", "admin", "password")
ef = io.StringIO()

print("Running tests on DatabaseManager module...")

# Test addUser
print("Testing addUser method...", end="")
user1ID = dm.addUser("fn_test1", "ln_test1", "email1@test.com", "password1")
assert user1ID != -1, "Test failed: User 1 not created"
user2ID = dm.addUser("fn_test2", "ln_test2", "email2@test.com", "password2")
assert user2ID != -1, "Test failed: User 2 not created"
user3ID = dm.addUser("fn_test3", "ln_test3", "email3@test.com", "password3")
assert user3ID != -1, "Test failed: User 3 not created"
print("Passed")

# Test checkUserPwd
print("Testing checkUserPwd method...", end="")
assert dm.checkUserPwd("email1@test.com", "password1") == 1, \
    "Test failed: Error checking user1 password"
assert dm.checkUserPwd("email1@test.com", "password") == 0, \
    "Test failed: Error checking false user1 password"
with redirect_stdout(ef):
    assert dm.checkUserPwd("email@test.com", "password") == -1, \
        "Test failed: Error checking password with fake user"
print("Passed")

# Test deleteUser
print("Testing deleteUser method...", end="")
assert dm.deleteUser(user3ID) == 1, "Test failed: User3 not deleted"
with redirect_stdout(ef):
    assert dm.getUser("email3@test.com") == -1, \
        "Test failed: User3 exists after deletion"
print("Passed")

# Test users table setters
print("Testing users table setter methods...", end="")
dm.setUserName(user2ID, "fn_test2_new", "ln_test2_new")
user = dm.getUser("email2@test.com")
assert user[1] == "fn_test2_new" and user[2] == "ln_test2_new", \
    "Test failed: User first and last names were not changed"
dm.setUserEmail(user2ID, "email2_new@test.com")
assert dm.getUser("email2_new@test.com"), \
    "Test failed: User email was not changed"
dm.setUserPassword(user2ID, "password2_new")
assert dm.checkUserPwd("email2_new@test.com", "password2_new") == 1, \
    "Test failed: User password was not changed"
print("Passed")

# Test addEvent
print("Testng addEvent method...", end="")
event1ID = dm.addEvent(user1ID, "test event 1", "Test event 1 description",
    "testCategory1", "2019-10-16 14:00:00", "2019-10-16 14:05:00") 
assert dm.getEvent(event1ID), "Test failed: Event 1 not created"
event2ID = dm.addEvent(user1ID, "test event 2", "Test event 2 description",
    "testCategory2", "2019-10-16 14:00:00") 
assert dm.getEvent(event2ID), "Test failed: Event 2 not created"
event3ID = dm.addEvent(user1ID, "test event 3", "Test event 3 description",
    "testCategory3", "2019-10-16 14:00:00", "2019-10-16 14:10:00")
assert dm.getEvent(event3ID), "Test failed: Event 3 not created"
print("Passed")

# Test deleteEvent
print("Testing deleteEvent method...", end="")
assert dm.deleteEvent(event3ID) == 1, "Test failed: Event 3 not deleted"
with redirect_stdout(ef):
    assert dm.getEvent(event3ID) == -1, \
        "Test failed: Event 3 still exists after deletion"
print("Passed")

# Test events table setters
print("Testing events table setter methods...", end="")
dm.setEventTitle(event2ID, "new test event 2")
event = dm.getEvent(event2ID)
assert event[2] == "new test event 2", \
    "Test failed: Event 2 title did not change"
dm.setEventDescr(event2ID, "New test event 2 description")
event = dm.getEvent(event2ID)
assert event[3] == "New test event 2 description", \
    "Test failed: Event 2 description did not change"
dm.setEventDateTime(event2ID, "2019-11-01 12:00:00", "2019-11-02 13:00:00")
event = dm.getEvent(event2ID)
assert str(event[4]) == "2019-11-01 12:00:00" and \
    str(event[5]) == "2019-11-02 13:00:00", \
    "Test failed: Event 2 date time did not change"
dm.setEventCategory(event2ID, "newTestCategory2")
event = dm.getEvent(event2ID)
assert event[6] == "newTestCategory2", \
    "Test failed: Event 2 category did not change"
print("Passed")
