import mysql.connector
import dbConnection
from SPMS import queries

mydb=dbConnection.queriesDB()

def fetchQuestions(course_id,section_num,assessment,semester):
    cursor = mydb.cursor()
    cursor.execute('''        
    use spms;
    SELECT question_id,total_marks, weight, clo_id
    FROM spms.spms_section_t as s,spms.spms_question_t as q
    WHERE s.section_id=q.section_id
    AND   s.section_num = {}
    AND course_id='{}'
    and assessment_name='{}}'
    and semester="{}";'''.format(section_num,course_id,assessment,semester))
    rows=cursor.fetchall()
    cursor.close()
    QuestionBank=[[]for i in range(4)]
    for i in range(len(rows)):
        QuestionBank[0].append(rows[i][0])
        QuestionBank[1].append(rows[i][1])
        QuestionBank[2].append(rows[i][2])
        QuestionBank[3].append(rows[i][3])
    return QuestionBank

print(fetchQuestions("CSE101",1,"Mid","Spring 2020"))