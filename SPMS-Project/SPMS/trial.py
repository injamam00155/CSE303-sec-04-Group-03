import mysql.connector
import dbConnection
import queries

mydb=mysql.connector.connect(
        host= '127.0.0.1',
        user= 'root',  
        password= 'inja',  
        database= 'spms'  
    )
def getCourseWiseStudentPLO(student_id):
    cursor = mydb.cursor()
    cursor.execute('''
        SELECT p.plo_num as plo_num,co.course_id,cast(100*sum(e.obtained_marks)/sum(a.total_marks) as decimal(10,2))
               FROM spms_registration_t r,
                   spms_question_t a, 
                   spms_evaluation_t e,
                   spms_clo_t co, 
                   spms_plo_t p,
                   (
                        SELECT p.plo_num as plo_num,sum(a.total_marks) as Total, r.student_id as student_id
                        FROM spms_registration_t r,
                            spms_question_t a, 
                            spms_evaluation_t e,
                            spms_clo_t co, 
                            spms_plo_t p
                        WHERE r.registration_id = e.registration_id 
                            and e.question_id = a.question_id
                            and a.clo_id=co.clo_id 
                            and co.plo_id = p.plo_id 
                            and r.student_id = '{}'
                        GROUP BY  r.student_id,p.plo_id) derived
               WHERE r.student_id = derived.student_id
                    and e.registration_id = r.registration_id
                    and e.question_id = a.question_id
                    and a.clo_id=co.clo_id 
                    and co.plo_id = p.plo_id
                    and p.plo_num = derived.plo_num
               GROUP BY  p.plo_id,co.course_id'''.format(student_id))
    row = cursor.fetchall()
    cursor.close()
    table = []
    courses = []

    for entry in row:
        if entry[1] not in courses:
            courses.append(entry[1])
    courses.sort()
    plo = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6", "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]

    for i in courses:
        temptable = [i]

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    temptable.append(k[2])
                    found = True
            if not found:
                temptable.append('N/A')
        table.append(temptable)
    return plo, courses, table