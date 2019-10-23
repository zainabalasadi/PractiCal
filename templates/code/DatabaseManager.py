import mysql.connector
import argparse
from templates.code.Calendar import Calandar
from templates.code.Comment import Comment
from templates.code.Event import Event
#from templates.code.Group import Group
from templates.code.Notification import Notification
from templates.code.User import User

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
                database=database
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

    def checkUserPwd(self, email, password):
        cursor = self._db.cursor()
        sql = "SELECT email, password FROM users WHERE email = %s"
        val = (email.lower(),)
        try:
            cursor.execute(sql, val)
            user = cursor.fetchone()
            cursor.close()
            if not user:
                raise ValueError("User not found")
            if user[1] == password:
                return 1
            else:
                return 0
        except Exception as e:
            print(("Error encountered while accessing database.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def checkEmailExists(self, email):
        cursor = self._db.cursor()
        sql = "SELECT email FROM users WHERE email = %s"
        val = (email.lower(), )
        try:
            cursor.execute(sql, val)
            user = cursor.fetchone()
            cursor.close()
            if not user:
                return 0
            return 1
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

    def getUser(self, email, password):
        cursor = self._db.cursor()
        sql = ("SELECT uid, first_name, last_name FROM users"
               "WHERE email = %s, password = %s")
        val = (email, password)
        try:
            cursor.execute(sql, val)
            user = cursor.fetchone()
            cursor.close()
            if not user:
                raise Exception("Credentials provided dont match")
            
            events = self.getUserEvents(user[0])
            if events = -1:
                events = []
            calendars = dict()
            for e in events:
                calName = e.getCalendar().getName()
                if calName in calendars.keys():
                    calendars[calName].append(e)
                else:
                    calendars[calName] = [e]
            return User(userID=user[0], 
                        firstName=user[1],
                        lastName=user[2],
                        email=email,
                        password=password
                        calendars=calendars)

        except Exception as e:
            print(("Error encountered while trying to locate user record.\n"
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

    def addEvent(self, userID, title, descr, category, startDT, endDT=None):
        cursor = self._db.cursor()

        try:
            sql = "SELECT uid FROM users WHERE uid = %s"
            val = (userID, )
            cursor.execute(sql, val)
            if not cursor.fetchone():
                raise ValueError("User does not exist")

            sql = ("INSERT INTO events (uid, title, descr, startdt, "
                   "enddt, category) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")
            val = (userID, title, descr, startDT, endDT, category)
            cursor.execute(sql, val)
            self._db.commit()
            newID = cursor.lastrowid
            cursor.close()
            if not newID:
                raise Exception("No changes made")
            return newID

        except Exception as e:
            print(("Error encounterd while creating event.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def deleteEvent(self, eventID):
        cursor = self._db.cursor()
        sql = "DELETE FROM events WHERE eid = %s"
        val = (eventID, )
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
        sql = ("SELECT eid, uid, title, descr, startdt, enddt, category "
               "FROM events WHERE eid = %s")
        val = (eventID, )
        try:
            cursor.execute(sql, val)
            event = cursor.fetchone()
            cursor.close()
            if not event:
                raise Exception("Event not found")
            return Event(eventId=event[0],
                        user=event[1],
                        name=event[2],
                        description=event[3],
                        startDateTime=event[4],
                        endDateTime=event[5],
                        calendar=event[6])
        except Exception as e:
            print(("Error encountered while trying to locate record.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def getUserEvents(self, userID):
        cursor = self._db.cursor()
        sql = ("SELECT eid, uid, title, descr, startdt, enddt, category "
               "FROM events WHERE uid = %s")
        val = (userID, )
        try:
            cursor.execute(sql, val)
            events = cursor.fetchall()
            cursor.close()
            if events == None:
                events = []
            return [Event(eventId=e[0],
                        user=e[1],
                        name=e[2],
                        description=e[3],
                        startDateTime=e[4],
                        endDateTime=e[5],
                        calendar=e[6])
                    for e in events]
            
        except Exception as e:
            print(("Error encountered while trying to locate records.\n"
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

    def setEventCategory(self, eventid, newCategory):
        cursor = self._db.cursor()
        sql = "UPDATE events SET category = %s WHERE eid = %s"
        val = (newCategory, eventid)
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

    def addInvite(self, eventID, userID, status='UNKNOWN'):
        cursor = self._db.cursor()
        sql = ("INSERT INTO invites (eid, uid, status)"
               "VALUES (%s, %s, %s)")
        val = (eventID, userID, status)
        try:
            cursor.execute(sql, val)
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("Invite not added")
            return 1
        except Exception as e:
            print(("Error encountered while inserting invite.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1
            
    def deleteInvite(self, eventID, userID):
        cursor = self._db.cursor()
        sql = "DELETE FROM invites WHERE eid = %s, uid = %s"
        val = (eventID, userID)
        try:
            cursor.execute(sql, val)
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1
        except Exception as e:
            print(("Error encountered while updating invite.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def getInvites(self, eventID="", userID="", status="*")
        cursor = self._db.cursor()
        sql = ("SELECT eid, uid, status FROM invites " 
               "WHERE eid = %s, uid = %s, status = %s")
        val = (eventID, userID, status)
        try:
            cursor.execute(sql, val)
            invites = cursor.fetchall()
            cursor.close()
            return invites            
        except Exception as e:
            print(("Error encountered while getting invites.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1
        

    def setInviteStatus(self, eventID, userID, newStatus):
        cursor = self._db.cursor()
        sql = "UPDATE invites SET status = %s WHERE eid = %s, uid = %s"
        val = (newStatus, eventID, userID)
        try:
            cursor.execute(sql, val)
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("Invite not added")
            return 1
        except Exception as e:
            print(("Error encountered while inserting invite.\n"
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
        passwd=password
    )

    cursor = db.cursor()
    print("Checking databases...")
    cursor.execute("SHOW DATABASES")
    if database in [x[0] for x in cursor]:
        print(("Database already exists. Do you wish to reinitialise the "
               "{} database? (y/n)".format(database)))
        resp = input()
        if resp.lower()[0] == "n":
            quit()
        elif resp.lower()[0] == "y":
            cursor.execute("USE {}".format(database))
            print("Deleting data from database {}...".format(database))
            cursor.execute("SET foreign_key_checks = 0")
            cursor.execute("DROP TABLE IF EXISTS users, events")
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
                    "password VARCHAR(128) NOT NULL, "
                    "PRIMARY KEY (uid))"))
    cursor.execute(("CREATE TABLE events ("
                    "eid int NOT NULL AUTO_INCREMENT, "
                    "uid int NOT NULL, "
                    "title VARCHAR(70) NOT NULL, "
                    "descr TEXT, "
                    "startdt DATETIME NOT NULL, "
                    "enddt DATETIME, "
                    "category VARCHAR(25), "
                    "PRIMARY KEY (eid), "
                    "FOREIGN KEY (uid) REFERENCES users(uid))"))
    cursor.execute(("CREATE TABLE invites ("
                    "eid int NOT NULL, "
                    "uid int NOT NULL, "
                    "status ENUM('UNKNOWN', 'GOING', 'MAYBE', 'NOT_GOING'), "
                    "FOREIGN KEY (eid) REFERENCES events(eid), "
                    "FOREIGN KEY (uid) REFERENCES users(uid))"))
    db.commit()
    cursor.close()
