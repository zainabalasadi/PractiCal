import mysql.connector
import argparse
import bcrypt
import json

HOST = "localhost"
USER = "admin"
PASSWORD = "password"
DATABASE = "practiCal_db"

class DatabaseManager():

    def __init__(self, database, host, user, password):
        try:
            self._db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password,
                database=database,
                auth_plugin='mysql_native_password'
            )
        except Exception as e:
            print(("Error loading database {} using provided credentials.\n"
                   "The following error was raised:\n\n{}".format(database, e)))
            self._db = None


    def loadDatabase(self, database, host, user, password):

        try:
            self._db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password,
                database=database
            )
        except Exception as e:
            print(("Error loading database {} using provided credentials.\n"
                   "The following error was raised:\n\n{}".format(database, e)))
            self._db = None

    def addUser(self, firstName, lastName, email, password):
        cursor = self._db.cursor()
        sql = ("INSERT INTO users (first_name, last_name, email, password) "
               "VALUES (%s, %s, %s, %s)")
        val = (firstName.lower(), lastName.lower(), email.lower(), password)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            newID = cursor.lastrowid
            cursor.close()
            if not newID:
                raise Exception("No changes made")
            return newID
        except Exception as e:
            print(("Error trying to create new user.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def checkUserCred(self, email, password, use_bcrypt=False):
        cursor = self._db.cursor()
        sql = "SELECT uid, password FROM users WHERE email = %s"
        val = (email.lower(),)
        try:
            cursor.execute(sql, val)
            user = cursor.fetchone()
            cursor.close()
            if not user:
                raise ValueError("User not found")
            # Check password
            if use_bcrypt:
                try:
                    bytePW = bytes(user[1], 'utf-8')
                except:
                    bytePW = user[1]
                if bcrypt.hashpw(bytes(password, 'utf-8'), bytePW) != bytePW:
                    return 0
            else:
                if password != user[1]:
                    return 0
            return user[0]
        except Exception as e:
            print(("Error encountered while accessing database.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def deleteUser(self, userID):
        cursor = self._db.cursor()
        sql = "DELETE FROM users WHERE uid = %s"
        val = (userID,)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1
        except Exception as e:
            print(("Error encountered while trying to delete record.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def searchUser(self, query):
        cursor = self._db.cursor()
        q = query.replace(' ', '%')
        sql = ("SELECT first_name, last_name, email FROM users "
               "WHERE CONCAT(first_name, ' ', last_name) LIKE CONCAT('%', %s, '%') "
               "OR CONCAT(last_name, ' ', first_name) LIKE CONCAT('%', %s, '%') "
               "OR email LIKE CONCAT('%', %s, '%')")
        val = (q, q, q)
        try:
            cursor.execute(sql, q)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(("Error encounterd while searching for users.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def getUser(self, userID=None, email=None):
        try:
            cursor = self._db.cursor()
            if not userID and not email:
                raise Exception("Neither userID or email provided")

            condition = "uid = %s" if userID else "email = %s"
            otherFields = ", contacts, preferences" if userID else ""
            sql = ("SELECT uid, first_name, last_name, email {} FROM users "
                   "WHERE {}".format(otherFields, condition))
            val = (userID, )
            cursor.execute(sql, val)
            user = cursor.fetchone()
            cursor.close()
            if not user:
                raise ValueError("User not found")
            return user
        except Exception as e:
            print(("Error encountered while trying to locate user record.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def setUser(self, userID, newFName=None, newLName=None, newEmail=None,
                newPassword=None, newContacts=None, newPreferences=None):
        val = []
        fields = []
        if newFName:
            fields.append("first_name = %s")
            val.append(newFName)
        if newLName:
            fields.append("last_name = %s")
            val.append(newLName)
        if newEmail:
            fields.append("email = %s")
            val.append(newEmail)
        if newPassword:
            fields.append("password = %s")
            val.append(newPassword)
        if newContacts:
            fields.append("contacts = %s")
            val.append(newContacts)
        if newPreferences:
            fields.append("preferences = %s")
            val.append(newPreferences)
        sql = "UPDATE users SET {} WHERE uid = %s".format(", ".join(fields))
        val.append(userID)
        val = tuple(val)

        try:
            if len(val) == 1:
                raise Exception("No new field values to update")

            cursor = self._db.cursor()
            cursor.execute(sql, val)
            rowcount = cursor.rowcount
            cursor.close()

            if not rowcount:
                raise Exception("Fields were not changed")
            return 1
        except Exception as e:
            print(("Error encountered while trying to update record.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def setUserName(self, userID, newFName, newLName):
        cursor = self._db.cursor()
        sql = "UPDATE users SET first_name = %s, last_name = %s WHERE uid = %s"
        val = (newFName.lower(), newLName.lower(), userID)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("User name was not changed")
            return 1
        except Exception as e:
            print(("Error encountered while trying to update record.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def setUserEmail(self, userID, newEmail):
        cursor = self._db.cursor()
        sql = "UPDATE users SET email = %s WHERE uid = %s"
        val = (newEmail.lower(), userID)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("Email was not changed")
            return 1
        except Exception as e:
            print(("Error encountered while trying to update record.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def setUserPassword(self, userID, newPass):
        cursor = self._db.cursor()
        sql = "UPDATE users SET password = %s WHERE uid = %s"
        val = (newPass, userID)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("Password was not changed")
            return 1
        except Exception as e:
            print(("Error encountered while trying to update record.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def addEvent(self, userID, title, descr, calendar, category, startDT,
                 endDT=None, location=None):
        cursor = self._db.cursor()

        try:
            sql = "SELECT uid FROM users WHERE uid = %s"
            val = (userID, )
            cursor.execute(sql, val)
            if not cursor.fetchone():
                raise ValueError("User does not exist")

            sql = ("INSERT INTO events (uid, title, descr, startdt, "
                   "enddt, calendar, category, location) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            val = (userID, title, descr, startDT, endDT, calendar, category,
                location)
            cursor.execute(sql, val)
            self._db.commit()
            newID = cursor.lastrowid
            cursor.close()
            if not newID:
                raise Exception("Event not created")
            return newID

        except Exception as e:
            print(("Error encounterd while creating event.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def deleteEvent(self, eventID, userID=None):
        cursor = self._db.cursor()
        sql = "DELETE FROM events WHERE eid = %s"
        val = [eventID]
        if userID:
            sql += ", uid = %s"
            val.append(userID)
        val = tuple(val)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1

        except Exception as e:
            print(("Error encountered while deleting event.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def getEvent(self, eventID):
        cursor = self._db.cursor()
        sql = ("SELECT eid, uid, title, descr, startdt, enddt, calendar, "
               "category, location FROM events WHERE eid = %s")
        val = (eventID, )
        try:
            cursor.execute(sql, val)
            event = cursor.fetchone()
            cursor.close()
            if not event:
                raise Exception("Event not found")
            return event
        except Exception as e:
            print(("Error encountered while trying to locate record.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def getUserEvents(self, userID):
        cursor = self._db.cursor()
        sql = ("SELECT eid, uid, title, descr, startdt, enddt, calendar, "
               "category, location FROM events WHERE uid = %s")
        val = (userID, )
        try:
            cursor.execute(sql, val)
            events = cursor.fetchall()
            cursor.close()
            if events == None:
                events = []
            return events

        except Exception as e:
            print(("Error encountered while trying to locate records.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def setEvent(self, eventID, newTitle=None, newDescr=None, newStartDT=None,
                 newEndDT=None, newCalendar=None, newCategory=None,
                 newLocation=None):
        val = []
        fields = []
        if newTitle:
            fields.append("title = %s")
            val.append(newTitle)
        if newDescr:
            fields.append("descr = %s")
            val.append(newDescr)
        if newStartDT:
            fields.append("startdt = %s")
            val.append(newStartDT)
        if newEndDT:
            fields.append("enddt = %s")
            val.append(newEndDT)
        if newCalendar:
            fields.append("calendar = %s")
            val.append(newCalendar)
        if newCategory:
            fields.append("category = %s")
            val.append(newCategory)
        if newLocation:
            fields.append("location = %s")
            val.append(newLocation)
        sql = "UPDATE events SET {} WHERE eid = %s".format(", ".join(fields))
        val.append(eventID)
        val = tuple(val)

        try:
            if len(val) == 1:
                raise Exception("No new field values to update")

            cursor = self._db.cursor()
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()

            if not rowcount:
                raise Exception("No fields were changed")
            return 1

        except Exception as e:
            print(("Error encountered while trying to update records.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def setEventTitle(self, eventID, newTitle):
        cursor = self._db.cursor()
        sql = "UPDATE events SET title = %s WHERE eid = %s"
        val = (newTitle, eventID)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1
        except Exception as e:
            print(("Error encountered while updating event.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def setEventDescr(self, eventID, newDescr):
        cursor = self._db.cursor()
        sql = "UPDATE events SET descr = %s WHERE eid = %s"
        val = (newDescr, eventID)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1
        except Exception as e:
            print(("Error encountered while updating event.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def setEventDateTime(self, eventID, newStartDT, newEndDT):
        cursor = self._db.cursor()
        sql = "UPDATE events SET startdt = %s, enddt = %s WHERE eid = %s"
        val = (newStartDT, newEndDT, eventID)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1
        except Exception as e:
            print(("Error encountered while updating event.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def setEventCalendar(self, eventid, newCalendar):
        cursor = self._db.cursor()
        sql = "UPDATE events SET calendar = %s WHERE eid = %s"
        val = (newCalendar, eventid)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1
        except Exception as e:
            print(("Error encountered while updating event.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def addInvite(self, eventID, receiverID, status, calendar='Default'):
        if self.getInvite(eventID, receiverID):
            return 0
        cursor = self._db.cursor()
        sql = ("INSERT INTO invites (eid, receiver_id, status, calendar)"
               "VALUES (%s, %s, %s, %s)")
        val = (eventID, receiverID, status, calendar)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("Invite not added")
            return 1
        except Exception as e:
            print(("Error encountered while inserting invite.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def deleteInvite(self, eventID, receiverID):
        cursor = self._db.cursor()
        sql = ("DELETE FROM invites WHERE eid = %s AND receiver_id = %s")
        val = (eventID, receiverID)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("Invite not deleted")
            return 1
        except Exception as e:
            print(("Error encountered while deleting invite.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def getInvite(self, eventID, receiverID):
        cursor = self._db.cursor()
        sql = ("SELECT eid, receiver_id, status, calendar "
               "FROM invites WHERE eid = %s AND receiver_id = %s")
        val = (eventID, receiverID)
        try:
            cursor.execute(sql, val)
            invite = cursor.fetchone()
            cursor.close()
            return invite
        except Exception as e:
            print(("Error encountered while getting invite.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def getInvitesByUser(self, receiverID):
        cursor = self._db.cursor()
        sql = ("SELECT eid, receiver_id, status, calendar "
               "FROM invites WHERE receiver_id = %s")
        val = (receiverID, )
        try:
            cursor.execute(sql, val)
            invites = cursor.fetchall()
            cursor.close()
            return invites
        except Exception as e:
            print(("Error encountered while getting invites.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def getInvitesByEvent(self, eventID):
        cursor = self._db.cursor()
        sql = ("SELECT eid, receiver_id, status "
               "FROM invites WHERE eid = %s")
        val = (eventID, )
        try:
            cursor.execute(sql, val)
            invites = cursor.fetchall()
            cursor.close()
            return invites
        except Exception as e:
            print(("Error encountered while getting invites.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1


    def setInvite(self, eventID, receiverID, newStatus=None, newCalendar=None):
        val = []
        fields = []
        if newStatus:
            fields.append("status = %s")
            val.append(newStatus)
        if newCalendar:
            fields.append("calendar = %s")
            val.append(newCalendar)
        sql = ("UPDATE invites SET {} WHERE eid = %s and "
               "receiver_id = %s".format(", ".join(fields)))
        val += [eventID, receiverID]
        val = tuple(val)

        try:
            if len(val) == 2:
                raise Exception("No new field values to update")

            cursor = self._db.cursor()
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()

            if not rowcount:
                raise Exception("Invite not changed")
            return 1

        except Exception as e:
            print(("Error encountered while trying to update records.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def addNotification(self, eventID, senderID, receiverID, notifType):
        if self.getNotification(eventID, senderID, receiverID, notifType):
            return 0

        cursor = self._db.cursor()
        sql = ("INSERT INTO notifications "
               "(eid, sender_id, receiver_id, notif_type)"
               "VALUES (%s, %s, %s, %s)")
        val = (eventID, senderID, receiverID, notifType)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("Notification not added")
            return 1
        except Exception as e:
            print(("Error encountered while inserting notification.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def deleteNotification(self, eventID, senderID, receiverID, notifType):
        cursor = self._db.cursor()
        sql = ("DELETE FROM notifications WHERE eid = %s AND sender_id = %s AND "
               "receiver_id = %s AND notif_type = %s")
        val = (eventID, senderID, receiverID, notifType)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("Notification not deleted")
            return 1
        except Exception as e:
            print(("Error encountered while deleting notification.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def getNotification(self, eventID, senderID, receiverID, notifType):
        cursor = self._db.cursor()
        sql = ("SELECT eid, sender_id, receiver_id, notif_type "
               "FROM notifications WHERE eid = %s AND sender_id = %s AND "
               "receiver_id = %s AND notif_type = %s")
        val = (eventID, senderID, receiverID, notifType)
        try:
            cursor.execute(sql, val)
            invites = cursor.fetchall()
            cursor.close()
            return invites
        except Exception as e:
            print(("Error encountered while getting notifications.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def getNotifications(self, receiverID):
        cursor = self._db.cursor()
        sql = ("SELECT eid, sender_id, notif_type "
               "FROM notifications WHERE receiver_id = %s")
        val = (receiverID, )
        try:
            cursor.execute(sql, val)
            invites = cursor.fetchall()
            cursor.close()
            return invites
        except Exception as e:
            print(("Error encountered while getting notifications.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

def arg_parser():
    parser = argparse.ArgumentParser(
        prog="PractiCal Database Manager",
        description="Initialise PractiCal database")
    parser.add_argument("--d", nargs="?", default="practiCal_db",
                        help="Enter database name")
    parser.add_argument("--h", nargs="?", default="localhost",
                        help="Enter database server host")
    parser.add_argument("--u", nargs="?", default="admin",
                        help="Enter server username")
    parser.add_argument("--p", nargs="?", default="password",
                        help="Enter password")
    return parser.parse_args()

if __name__ == "__main__":

    args = arg_parser()
    database = args.d
    host = args.h
    user = args.u
    password = args.p

    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        auth_plugin='mysql_native_password'
    )

    cursor = db.cursor()
    print("Checking databases...")
    cursor.execute("SHOW DATABASES")
    tables = [x[0] for x in cursor.fetchall()]
    try:
        tables = [t.decode('utf-8') for t in tables]
    except:
        pass
    if database in tables:
        print(("Database already exists. Do you wish to reinitialise the "
               "{} database? (y/n)".format(database)))
        resp = input()
        if resp.lower()[0] == "n":
            quit()
        elif resp.lower()[0] == "y":
            cursor.execute("USE {}".format(database))
            print("Deleting data from database {}...".format(database))
            cursor.execute("SET foreign_key_checks = 0")
            cursor.execute(("DROP TABLE IF EXISTS users, events, invites, "
                            "notifications"))
            cursor.execute("SET foreign_key_checks = 1")
    else:
        print("Creating database {}...".format(database))
        cursor.execute("CREATE DATABASE {}".format(database))

    cursor.execute("USE {}".format(database))
    print("Initialising database...")
    cursor.execute(("CREATE TABLE users ("
                    "uid int NOT NULL AUTO_INCREMENT, "
                    "first_name VARCHAR(70) NOT NULL, "
                    "last_name VARCHAR(70) NOT NULL, "
                    "email VARCHAR(255) NOT NULL UNIQUE, "
                    "password VARBINARY(128) NOT NULL, "
                    "contacts TEXT, "
                    "preferences TEXT, "
                    "PRIMARY KEY (uid))"))
    cursor.execute(("CREATE TABLE events ("
                    "eid int NOT NULL AUTO_INCREMENT, "
                    "uid int NOT NULL, "
                    "title VARCHAR(70) NOT NULL, "
                    "descr TEXT, "
                    "startdt VARCHAR(25) NOT NULL, "
                    "enddt VARCHAR(25), "
                    "calendar VARCHAR(25), "
                    "category VARCHAR(25), "
                    "location TEXT, "
                    "PRIMARY KEY (eid), "
                    "FOREIGN KEY (uid) REFERENCES users(uid))"))
    cursor.execute(("CREATE TABLE invites ("
                    "eid int NOT NULL, "
                    "receiver_id int NOT NULL, "
                    "status int NOT NULL, "
                    "calendar VARCHAR(25), "
                    "FOREIGN KEY (eid) REFERENCES events(eid), "
                    "FOREIGN KEY (receiver_id) REFERENCES users(uid))"))
    cursor.execute(("CREATE TABLE notifications ("
                    "eid int NOT NULL, "
                    "sender_id int NOT NULL, "
                    "receiver_id int NOT NULL, "
                    "notif_type int NOT NULL, "
                    "FOREIGN KEY (eid) REFERENCES events(eid), "
                    "FOREIGN KEY (sender_id) REFERENCES users(uid), "
                    "FOREIGN KEY (receiver_id) REFERENCES users(uid))"))
    print("Database initialised.")

    print("Would you like to load in test data? (y/n)")
    resp = input()
    if resp.lower()[0] == "y":
        userPrefs1 = json.dumps(
            {
                'default_colour': '#566EE9',
                'calendars': {
                    'Default': {
                        'colour': '#566EE9'
                    },
                    'Calendar 1': {
                        'colour': 'green'
                    },
                    'Calendar 2': {
                        'colour': 'red'
                    }
                }
            })
        userPrefs2 = json.dumps(
            {
                'default_colour': '#566EE9',
                'calendars': {
                    'Default': {
                        'colour': '#9C2BAF'
                    },
                    'Social': {
                        'colour': '#FF9612'
                    },
                    'Work': {
                        'colour': '#9ACE4E'
                    },
                    'Uni': {
                        'colour': '#9C2BAF'
                    },
                }
            })
        cursor.execute(("INSERT INTO users "
                        "(first_name, last_name, email, password, preferences)"
                        "VALUES "
                        "('Egene', 'Oletu', 'egene.o@email.com', '{password}', '{up1}'), "
                        "('Zainab', 'Alasadi', 'zainab.a@email.com', '{password}', '{up2}'), "
                        "('Morgan', 'Green', 'morgan.g@email.com', '{password}', '{up1}'), "
                        "('Derrick', 'Foo', 'derrick.f@email.com', '{password}', '{up1}'), "
                        "('Michael', 'Ho', 'michael.h@email.com', '{password}', '{up1}')"
                        "".format(password=str(bcrypt.hashpw('password'.encode('utf-8'),
                            bcrypt.gensalt()).decode("utf-8")), up1=userPrefs1,
                            up2=userPrefs2)))
        cursor.execute(("INSERT INTO events "
                        "(uid, title, descr, startdt, enddt, calendar) "
                        "VALUES "
                        "(1, 'Event 1 title', 'Event 1 description', '2019-11-06T"
                        "12:00', '2019-11-06T13:00', 'Default'), "
                        "(1, 'Event 2 title', 'Event 2 description', '2019-11-07T"
                        "12:00', '2019-11-07T13:00', 'Default'), "
                        "(1, 'Event 3 title', 'Event 3 description', '2019-11-08T"
                        "12:00', '2019-11-08T13:00', 'Calendar 1'), "
                        "(1, 'Event 4 title', 'Event 4 description', '2019-11-09T"
                        "12:00', '2019-11-09T13:00', 'Calendar 1'), "
                        "(1, 'Event 5 title', 'Event 5 description', '2019-11-10T"
                        "12:00', '2019-11-10T13:00', 'Calendar 2'), "

                        "(2, 'Sprint Meeting', 'Sprint Meeting 5, discussing merging back-end and front-end', '2019-10-30T"
                        "14:00', '2019-10-30T16:00', 'Uni'), "
                        "(2, 'Lunch with Sarah', 'Circular Quay', '2019-11-13T"
                        "12:00', '2019-11-13T13:30', 'Social'), "
                        "(2, 'Doctor Appointment', 'Ask about hay fever', '2019-11-15T"
                        "13:00', '2019-11-15T13:30', 'Default'), "
                        "(2, 'AI Conference', 'Chat to Fred for job opportunities', '2019-11-18T"
                        "09:00', '2019-11-20T18:00', 'Work'), "
                        "(2, 'COMP4920 Diary Due', 'Submit project diaries by Give', '2019-11-24T"
                        "18:30', '2019-11-24T19:45', 'Uni'), "
                        "(2, 'COMP4920 Peer Assessment', 'Submit peer assessments on Moodle', '2019-11-24T"
                        "13:30', '2019-11-24T13:45', 'Uni'), "
                        "(2, 'COMP4920 Project Due', 'Event 9 description', '2019-11-24T"
                        "21:00', '2019-11-24T23:55', 'Uni'), "
                        "(2, 'COMP4920 Presentation', 'Presenting the wonderful PractiCal to staff', '2019-11-25T"
                        "15:00', '2019-11-25T17:00', 'Uni'), "
                        "(2, 'End of Term Drinks', 'Casual Dress Code', '2019-11-25T"
                        "18:00', '2019-11-25T20:00', 'Uni'), "
                        "(2, 'COMP9444 Exam', 'Bring: Pens/pencils, Calculator - UNSW Approved', '2019-11-30T"
                        "13:45', '2019-11-30T15:00', 'Uni'), "
                        "(2, 'COMP4418 Exam', 'No Calculator', '2019-12-05T"
                        "08:45', '2019-12-05T11:00', 'Uni'), "
                        "(2, 'Meenas Graduation', 'Bring Flowers', '2019-12-13T"
                        "08:45', '2019-12-13T11:00', 'Social'), "
                        "(2, 'CHRISTMAS', 'WOOHOO!', '2019-12-25T"
                        "00:00', '2019-12-26T00:00', 'Social'), "

                        "(3, 'Event 11 title', 'Event 11 description', '2019-11-06T"
                        "09:30', '2019-11-06T17:00', 'Default'), "
                        "(3, 'Event 12 title', 'Event 12 description', '2019-11-07T"
                        "09:30', '2019-11-07T17:00', 'Default'), "
                        "(3, 'Event 13 title', 'Event 13 description', '2019-11-08T"
                        "09:30', '2019-11-08T17:00', 'Default')"))
    db.commit()
    cursor.close()
