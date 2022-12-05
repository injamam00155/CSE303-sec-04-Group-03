import mysql.connector
import dbConnection

mydb=dbConnection.queriesDB()


cursor = mydb.cursor()
cursor.execute('''SELECT userID,grp FROM spms_currsess_t''')
try:
    rows=cursor.fetchall()
    cursor.close()
except:
    cursor.close()
    

print(rows)