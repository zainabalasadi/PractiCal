from contextlib import redirect_stdout
import io
import importlib.util
spec = importlib.util.spec_from_file_location("DatabaseManager",
    "../templates/code/DatabaseManager.py")
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
with redirect_stdout(ef):
    test = dm.addUser("fn_test3", "ln_test3", "email3@test.com", "password3")
    assert test == -1, "Test failed: User 3 was created again"
user4ID = dm.addUser("fn_test4", "ln_test4", "email4@test.com", "password4")
assert user4ID != -1, "Test failed: User 4 not created"
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

# Test checkEmailExists
print("Testing checkEmailExists method...", end="")
assert dm.checkEmailExists("email1@test.com") == 1, \
    "Test failed: Error checking that email exists"
assert dm.checkEmailExists("wrong_email@test.com") == 0, \
    "Test failed: Error checking that email does not exist"
print("Passed")

# Test deleteUser
print("Testing deleteUser method...", end="")
assert dm.deleteUser(user3ID) == 1, "Test failed: User3 not deleted"
with redirect_stdout(ef):
    assert dm.getUser("email3@test.com", "password3") == -1, \
        "Test failed: User3 exists after deletion"
print("Passed")

# Test searchUser
print("Testing searchUser method...", end="")
print("Passed")

# Test users table setters
print("Testing users table setter methods...", end="")
dm.setUser(user2ID, newFName="fn2_new")
dm.setUser(user2ID, newLName="ln2_new")
dm.setUser(user2ID, newEmail="em2_new@test.com")
dm.setUser(user2ID, newPassword="pass2_new")
user = dm.getUser("em2_new@test.com", "pass2_new")
assert user != -1, "Test failed: Email or password not changed using setUser"
assert user[1] == "fn2_new", "Test failed: First name not changed using setUser"
assert user[2] == "ln2_new", "Test failed: Last name not changed using setUser"
assert dm.checkUserPwd("em2_new@test.com", "pass2_new") == 1, \
    "Test failed: Password not changed using setUser"
dm.setUser(user2ID, newFName="fn_test2", newEmail="email2@test.com")
user = dm.getUser("email2@test.com", "pass2_new")
assert user != -1, \
    "Test failed: Email not changed with first name using setUser"
assert user[1] == "fn_test2", \
    "Test failed: First name not changed with email using setUser"
dm.setUser(user2ID, newLName="ln_test2", newPassword="password2")
user = dm.getUser("email2@test.com", "password2")
assert user != -1, \
    "Test failed: Password not changed with last name using setUser"
assert user[2] == "ln_test2", \
    "Test failed: Last name not changed with password using setUser"

dm.setUserName(user2ID, "fn_test2_new", "ln_test2_new")
user = dm.getUser("email2@test.com", "password2")
assert user[1] == "fn_test2_new" and user[2] == "ln_test2_new", \
    "Test failed: User first and last names were not changed"
dm.setUserEmail(user2ID, "email2_new@test.com")
assert dm.getUser("email2_new@test.com", "password2"), \
    "Test failed: User email was not changed"
dm.setUserPassword(user2ID, "password2_new")
assert dm.checkUserPwd("email2_new@test.com", "password2_new") == 1, \
    "Test failed: User password was not changed"
print("Passed")

# Test addEvent
print("Testing addEvent method...", end="")
event1ID = dm.addEvent(user1ID, "test event 1", "Test event 1 description",
    "testCalendar1", "2019-10-16 14:00:00", "2019-10-16 14:05:00") 
assert dm.getEvent(event1ID), "Test failed: Event 1 not created"
event2ID = dm.addEvent(user1ID, "test event 2", "Test event 2 description",
    "testCalendar2", "2019-10-16 14:00:00") 
assert dm.getEvent(event2ID), "Test failed: Event 2 not created"
event3ID = dm.addEvent(user1ID, "test event 3", "Test event 3 description",
    "testCalendar3", "2019-10-16 14:00:00", "2019-10-16 14:10:00")
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
dm.setEvent(event2ID, newTitle="newTitle2")
dm.setEvent(event2ID, newDescr="newDescription2")
dm.setEvent(event2ID, newStartDT="2019-11-04 00:00:00")
dm.setEvent(event2ID, newEndDT="2019-11-04 12:00:00")
dm.setEvent(event2ID, newCalendar="newCalendar2")
event = dm.getEvent(event2ID)
assert event[2] == "newTitle2", \
    "Test failed: Title not changed using setEvent"
assert event[3] == "newDescription2", \
    "Test failed: Description not changed using setEvent"
assert str(event[4]) == "2019-11-04 00:00:00", \
    "Test failed: Start date time not changed using setEvent"
assert str(event[5]) == "2019-11-04 12:00:00", \
    "Test failed: End date time not changed using setEvent"
assert event[6] == "newCalendar2", \
    "Test failed: Calendar not changed using setEvent"
dm.setEvent(event2ID, newTitle="test event 2",
    newDescr="Test event 2 description", newCalendar="testCalendar2",
    newStartDT="2019-10-16 14:00:00", newEndDT="2019-10-16 15:00:00")
event = dm.getEvent(event2ID)
assert event[2] == "test event 2" \
    and event[3] == "Test event 2 description" \
    and str(event[4]) == "2019-10-16 14:00:00" \
    and str(event[5]) == "2019-10-16 15:00:00"\
    and event[6] == "testCalendar2", \
    "Test failed: One or more fields not changed using setEvent"  

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
dm.setEventCalendar(event2ID, "newTestCalendar2")
event = dm.getEvent(event2ID)
assert event[6] == "newTestCalendar2", \
    "Test failed: Event 2 category did not change"
print("Passed")

# Test addInvite
#print("Testing addInvite method...", end="")
#dm.addInvite(event1ID, user4ID)
#dm.addInvite(event2ID, user4ID)
#invites = dm.getInvitesByUser(user4ID) 
#assert invites and len(invites) == 2, \
#    "Test failed: One or more invites not created"
#print("Passed")

# Test deleteInvite
#print("Testing deleteInvite method...", end="")
#dm.deleteInvite(event2ID, user4ID)
#invites = dm.getInvitesByUser(user4ID)
#assert invites != -1 and len(invites) == 1, \
#    "Test failed: Invite not deleted"
#print("Passed")

# Test invites table setters
#print("Testing invites table setter methods...", end="")
#dm.setInviteStatus(event1ID, user4ID, "GOING")
#invites = dm.getInvitesByUser(user4ID)
#assert invites and invites[0][2] == "GOING", \
#    "Test failed: Invite status not changed"
#with redirect_stdout(ef):
#    assert dm.setInviteStatus(event1ID, user4ID, "invalid_status") == -1, \
#        "Test failed: Invite status changed to invalid value"
#dm.setInviteCalendar(event1ID, user4ID, "newCalendar")
#invites = dm.getInvitesByUser(user4ID)
#assert invites and invites[0][3] == "newCalendar", \
#    "Test failed: Invite calendar not changed"
#print("Passed")
