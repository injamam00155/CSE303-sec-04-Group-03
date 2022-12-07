import mysql.connector
import dbConnection
import queries

mydb=mysql.connector.connect(
        host= '127.0.0.1',
        user= 'root',  
        password= 'inja',  
        database= 'spms'  
    )

print(queries.getStudentWisePLO(1616161)[0])

