import mysql.connector

def mysql_init():
    mydb = mysql.connector.connect(
        host= "35.247.164.240",
        user= "peet",
        passwd= "10042541",
        database= "testdb"
    )

    return mydb