import mysql.connector

HOST = "localhost"
USER = "admin"
PASSWORD = "password"
DATABASE = "practiCal_db"

class DatabaseManager():

    def loadDatabase(self, database, host, user, passwd):

        try:
            db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
            )
        except Exception as e:
            print(("Error loading database {} using provided credentials.\n"
                   "The following error was raised:\n\n{}".format(database, e)))
            db = None

    def createUser(self, first_name, last_name, email, password):
        cursor = db.cursor()
        try:
            cursor.execute(("INSERT INTO users (first_name, last_name, "
                            "email, password)"
                            "VALUES ({}, {}, {}, {})".format(first_name,
                            last_name, email, password)))
        except Exception as e:
            print(("Error trying to create new user.\n"
                   "The following error was raised:\n\n{}".format(e)))



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
            cursor.execute("DROP DATABASE {}".format(DATABASE))
            print("Deleting database {}...".format(DATABASE))

    print("Creating database {}...".format(DATABASE))
    cursor.execute("CREATE DATABASE {}".format(DATABASE))
    cursor.execute("USE {}".format(DATABASE))
    cursor.execute(("CREATE TABLE users ("
                    "uid int AUTO_INCREMENT PRIMARY KEY, "
                    "first_name VARCHAR(70), "
                    "last_name VARCHAR(70), "
                    "email VARCHAR(255) UNIQUE, "
                    "password VARCHAR(30))"))


