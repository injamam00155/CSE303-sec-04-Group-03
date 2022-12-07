import mysql.connector
import dbConnection
import queries

mydb=mysql.connector.connect(
        host= '127.0.0.1',
        user= 'root',  
        password= 'inja',  
        database= 'spms'  
    )

<<<<<<< HEAD
print(queries.getStudentWisePLO(1616161)[0])

=======

question=queries.fetchQuestions("CSE101",1,"Mid","Spring 2020")
# print(question)

# print(queries.getStudentWisePLO(1616161)[0])
# print(queries.getStudentWisePLO(1616161)[1])
# print(queries.getDeptWisePLO("CSE")[1])
>>>>>>> da26507b4c72f46782838383c7f94e744c9a0d5d
