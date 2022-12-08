import mysql.connector
import dbConnection
import queries

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='inja',
    database='spms'
)


def xyz(course_id,semester,section_num):
    cursor = mydb.cursor()
    cursor.execute(''' 
               SELECT f.first_name,f.last_name,f.email, course_description, requied_textbook, cource_policy
                FROM spms.spms_section_t as s,
                spms.spms_course_outline_t as c,
                spms.spms_faculty_t as f
                WHERE c.section_id=s.section_id
                and f.faculty_id=s.faculty_id
                and s.section_num='{}'
                and s.semester='{}'
                and s.course_id='{}'
               '''.format(section_num,semester,course_id))
    row = cursor.fetchall()
    cursor.close()
    return row[0]

print(queries.getCourseOutline("CSE101","Spring 2020",1)[0]+' '+queries.getCourseOutline("CSE101","Spring 2020",1)[1])
print(xyz("CSE101","Spring 2020",1)[0]+' '+xyz("CSE101","Spring 2020",1)[1])
# print(xyz("CSE101","Spring 2020",1)[2])
# print(getCOWiseStudentPLO("CSE101","Spring 2020",1)[3])
# print(getCOWiseStudentPLO("CSE101","Spring 2020",1)[4])
# print(getCOWiseStudentPLO("CSE101","Spring 2020",1)[5])
# print(getCOWiseStudentPLO("CSE101","Spring 2020",1)[6])
