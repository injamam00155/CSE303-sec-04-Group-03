import mysql.connector
import dbConnection
import queries

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='inja',
    database='spms'
)


def getCourseOutline(course_id,semester,section_num):
    cursor = mydb.cursor()
    cursor.execute(''' 
SELECT f.first_name,f.last_name,f.email,assessment_and_marks_distribution,grade_conversion_scheme,requied_textbook,cource_policy,university_regulation_and_code_of_conduct
FROM spms.spms_section_t as s,
    spms.spms_course_outline_t as c,
    spms.spms_faculty_t as f
WHERE c.section_id=s.section_id
and f.faculty_id=s.faculty_id
and s.section_num={}
and s.semester="{}"
and s.course_id="{}"
               '''.format(course_id,semester,section_num))
    row = cursor.fetchall()
    cursor.close()
    return row[0]

print(getCourseOutline(1,"Spring 2020","CSE101"))