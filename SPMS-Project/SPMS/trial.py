import mysql.connector
import dbConnection

mydb=dbConnection.queriesDB()

username=1416455
cursor = mydb.cursor()
cursor.execute('''        
SELECT grp    
FROM spms_users_t
WHERE userID={}'''.format(username))
group=cursor.fetchall()
cursor.close()

print(group)