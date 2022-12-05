import mysql.connector
import dbConnection

mydb=dbConnection.queriesDB()

cursor = mydb.cursor()
cursor.execute('''        
SELECT *     
FROM spms_users_t
WHERE userID={}'''.format(1695838))
rows=cursor.fetchall()
cursor.close()

print(type(rows[0][2][0]))