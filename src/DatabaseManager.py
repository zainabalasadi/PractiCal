import mysql.connector

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

    def addUser(self, first_name, last_name, email, password):
        cursor = self._db.cursor()
        sql = ("INSERT INTO users (first_name, last_name, email, password) "
               "VALUES (%s, %s, %s, %s)")
        val = (first_name.lower(), last_name.lower(), email.lower(), password)
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1
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

    def deleteUser(self, userid):
        cursor = self._db.cursor()
        sql = "DELETE FROM users WHERE uid = %d"
        val = (userid,)
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

    def setUserName(self, email, new_fname, new_lname):
        cursor = self._db.cursor()
        sql = "UPDATE users SET first_name = %s, last_name = %s WHERE email = %s"
        val = (new_fname.lower(), new_lname.lower(), email.lower())
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1
        except Exception as e:
            print(("Error encountered while trying to update record.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def setUserEmail(self, email, new_email):
        cursor = self._db.cursor()
        sql = "UPDATE users SET email = %s WHERE email = %s"
        val = (new_email.lower(), email.lower())
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1
        except Exception as e:
            print(("Error encountered while trying to update record.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1
        
    def setUserPassword(self, email, new_pass):
        cursor = self._db.cursor()
        sql = "UPDATE users SET password = %s WHERE email = %s"
        val = (new_pass, email.lower())
        try:
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1
        except Exception as e:
            print(("Error encountered while trying to update record.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def addEvent(self, userid, title, desc, category, startdt, enddt=None):
        cursor = self._db.cursor()

        try:
            sql = "SELECT uid FROM users WHERE uid = %d"
            val = (userid, )
            cursor.execute(sql, val)
            if not cursor.fetchone():
                raise ValueError("User does not exist")

            sql = ("INSERT INTO events (uid, title, desc, startdt, "
                   "enddt, category) "
                   "VALUES (%d, %s, %s, %s, %s, %s)")
            val = (userid, title, startdt, enddt, category)
            cursor.execute(sql, val)
            self._db.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if not rowcount:
                raise Exception("No changes made")
            return 1

        except Exception as e:
            print(("Error encounterd while creating event.\n"
                   "The following error was raised:\n\n{}".format(e)))
            return -1

    def deleteEvent(self, eventid):
        cursor = self._db.cursor()
        sql = "DELETE FROM events WHERE eid = %d"
        val = (eventid, )
        try:
            cursor.execut(sql, val)
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


if __name__ == "__main__":
    db = mysql.connector.connect(
        host=HOST,
        user=USER,
        passwd=PASSWORD
    )

    cursor = db.cursor()
    print("Checking databases...")
    cursor.execute("SHOW DATABASES")
    if DATABASE in [x[0] for x in cursor]:
        print(("Database already exists. Do you wish to reinitialise the "
               "{} database? (y/n)".format(DATABASE)))
        resp = input()
        if resp.lower()[0] == "n":
            quit()
        elif resp.lower()[0] == "y":
            print("Deleting data from database {}...".format(DATABASE))
            cursor.execute("DROP TABLE IF EXISTS users, events")
    else:
        print("Creating database {}...".format(DATABASE))
        cursor.execute("CREATE DATABASE {}".format(DATABASE))

    cursor.execute("USE {}".format(DATABASE))
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
                    "desc TEXT, "
                    "startdt DATETIME NOT NULL, "
                    "enddt DATETIME, "
                    "category VARCHAR(25), "
                    "PRIMARY KEY (eid), "
                    "FOREIGN KEY (uid) REFERENCES users(uid))"))
