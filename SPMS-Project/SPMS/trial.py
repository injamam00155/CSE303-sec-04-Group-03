import mysql.connector
import dbConnection
from SPMS import queries

mydb=dbConnection.queriesDB()

student_id=queries.getCurrUser()[0][0]
print(student_id)
row = queries.getStudentWisePLO(student_id)
print(row)
chart1 = 'PLO Achievement'
plolabel1 = []
plodata1 = []
for i in row:
    plolabel1.append(i[0])
    plodata1.append(i[1])


context={
    "page":"dashboard",
    "id":queries.getCurrUser()[0][0],
    "group":queries.getCurrUser()[0][1],
    "name":queries.getName(str(queries.getCurrUser()[0][0])),
        'chart1': chart1,
    'plolabel1': plolabel1,
    'plodata1': plodata1,
}
    