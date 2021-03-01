import mysql.connector


def connect_db():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="secret",
    )
    return mydb


if __name__ == '__main__':
    connect_db()
