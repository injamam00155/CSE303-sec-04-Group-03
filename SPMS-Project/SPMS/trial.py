import mysql.connector
import dbConnection

mydb=dbConnection.queriesDB()

userID=1616161
cursor = mydb.cursor()
cursor.execute('''        
SELECT grp    
FROM spms_users_t
WHERE userID={}'''.format(userID))
group=cursor.fetchall()
cursor.close()

print(group[0][0])