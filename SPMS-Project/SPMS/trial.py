import mysql.connector
import dbConnection

mydb=dbConnection.queriesDB()

userID=1616161
cursor = mydb.cursor()
cursor.execute('''SELECT userID,grp FROM spms_currsess_t''')
try:
    rows=cursor.fetchall()
    cursor.close()
except:
    cursor.close()

print(rows)