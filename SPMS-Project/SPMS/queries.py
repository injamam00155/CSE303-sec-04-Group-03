from SPMS import dbConnection
import mysql.connector
from django.db import connection
import numpy as np

mydb=dbConnection.queriesDB()

def fetchQuestions(course_id,section_id,assessment,semester):
    cursor = mydb.cursor()
    cursor.execute('''        
    use spms;
    SELECT question_id,total_marks, weight, clo_id
    FROM spms.spms_section_t as s,spms.spms_question_t as q
    WHERE s.section_id=q.section_id
    AND   s.section_num = {}
    AND course_id='{}'
    and assessment_name='{}}'
    and semester="{}";'''.format(section_id,course_id,assessment,semester))
    rows=cursor.fetchall()
    cursor.close()
    QuestionBank=[[]for i in range(4)]
    for i in range(len(rows)):
        QuestionBank[0].append(rows[i][0])
        QuestionBank[1].append(rows[i][1])
        QuestionBank[2].append(rows[i][2])
        QuestionBank[3].append(rows[i][3])
    return QuestionBank
    


# print(mydb)
# cursor = mydb.cursor()
# print(cursor)



##user info based queries
def isValid(user_id):
    cursor = mydb.cursor()
    cursor.execute('''        
    SELECT *     
    FROM spms_users_t
    WHERE user_id={}'''.format(user_id))
    rows=cursor.fetchall()
    cursor.close()
    return bool(rows)


def getPassword(user_id):
        cursor = mydb.cursor()
        cursor.execute('''        
            SELECT password     
            FROM spms_users_t
            WHERE user_id={}'''.format(user_id))
        password=cursor.fetchall()[0][0]
        cursor.close()
        return password

def getGroup(user_id):
            cursor = mydb.cursor()
            cursor.execute('''        
            SELECT grp    
            FROM spms_users_t
            WHERE user_id={}'''.format(user_id))
            group=cursor.fetchall()
            cursor.close()
            return group[0][0]
            #output faculty/student

def getName(user_id):
            name=""
            if getGroup(user_id)=="student":
                str="student"
            elif getGroup(user_id)=="faculty":
                str="faculty"
            cursor = mydb.cursor()
            cursor.execute('''        
            SELECT first_name,last_name   
            FROM spms_{}_t
            WHERE {}_id={}'''.format(str,str,user_id))
            if cursor.fetchall()[0]:
                name=cursor.fetchall()
                try:
                    name=name[0]+" "+name[1]
                    cursor.close()
                except:
                    name=""
                    cursor.close()
            cursor.close()
            return name
            #output fname+lname(null for now)

def getDept(user_id):
    if getGroup(user_id)=="student":
        str="student"
    elif getGroup(user_id)=="faculty":
        str="faculty"
    cursor = mydb.cursor()
    cursor.execute('''        
            SELECT department_id   
            FROM spms_{}_t
            WHERE {}_id={}'''.format(user_id))
    department=cursor.fetchall()
    cursor.close()
    return department

def setCurrUser(user_id):
    try:
        cursor = mydb.cursor()
        group=getGroup(user_id)
        #injamam
        cursor.execute('''        
        INSERT INTO spms.spms_currsess_t 
        VALUES ({}, '{}')
        '''.format(user_id,group))
        rows=cursor.fetchall()
        cursor.close()
    except:
        print("an exception occurred")
        cursor.close()
    return


def deleteCurrUser():
    if getCurruser_id():
        cursor = mydb.cursor()
        cursor.execute('''TRUNCATE TABLE spms.spms_currsess_t''')
        rows=cursor.fetchall()
        cursor.close()
    return



def getCurrUser():
    cursor = mydb.cursor()
    cursor.execute('''SELECT user_id,grp FROM spms_currsess_t''')
    try:
        rows=cursor.fetchall()
        cursor.close()
    except:
        cursor.close()
    return rows

def getCurruser_id():
    cursor = mydb.cursor()
    cursor.execute('''SELECT user_id,grp FROM spms_currsess_t''')
    try:
        rows=cursor.fetchall()
        cursor.close()
    except:
        cursor.close()
    return rows[0]

def getCurruser_grp():
    cursor = mydb.cursor()
    cursor.execute('''SELECT user_id,grp FROM spms_currsess_t''')
    try:
        rows=cursor.fetchall()
        cursor.close()
    except:
        cursor.close()
    return rows[1]


def getPassword(user_id):
        cursor = mydb.cursor()
        cursor.execute('''        
            SELECT password     
            FROM spms_users_t
            WHERE user_id={}'''.format(user_id))
        password=cursor.fetchall()[0][0]
        cursor.close()
        return password



## Analysis


def getStudentCourseWiseCO(user_id,courseid):
    cursor = mydb.cursor()
    cursor.execute('''
    SELECT coNum, (100*(sum( e.obtained_marks)/sum( a.total_marks))) as copercent
                FROM spms_registration_t r,
                    spms_question_t a, 
                    spms_evaluation_t e,
					spms_clo_t clo,
                    spms_plo_t p
                WHERE  r.registration_id = e.registration_id 
                    and e.question_id = a.question_id
                    and a.clo_id=clo.clo_id 
                    and clo.plo_id = p.plo_id
                    and  r.student_id = {}
		            and clo.course_id="{}"
                GROUP BY  clo.clo_id'''.format(user_id,courseid))
    rows=cursor.fetchall()
    cursor.close()
    CO=[[]for i in range(2)]
    for i in range(len(rows)):
        CO[0].append(rows[i][0])
        CO[1].append(rows[i][1])

    return CO
    #outputs [['CO1', 'CO2', 'CO3', 'CO4'], [Decimal('52.1212'), Decimal('77.1429'), Decimal('70.0000'), Decimal('50.0000')]]
    
# GPA Analysis

def getStudentCGPA(student_id):
        cursor = mydb.cursor()
        cursor.execute(''' 
            SELECT sum(Credits*grade)/sum(Credits)
            FROM(   
                SELECT  Credits,
                    CASE
                        WHEN sum(Marks) >= 85 THEN 4.0
                        WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                        WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                        WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                        WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                        WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                        WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                        WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                        WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                        WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                        ELSE 0.0
                    END as grade
                FROM(
                    SELECT c.clo_id as clo_id,a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks, c.coNum as Credits
                    FROM spms_registration_t r,
                        spms_section_t sc, 
                        spms_course_t c,
                        spms_question_t a, 
                        spms_evaluation_t e
                    WHERE r.section_id = sc.sectionID
                        and sc.course_id = c.clo_id 
                        and r.registration_id = e.registration_id 
                        and e.question_id = a.question_id
                        and r.student_id = '{}'
                    GROUP BY  c.clo_id,a.assessmentName) Derived 
                GROUP BY clo_id) Derived
                    '''.format(student_id))
        row = cursor.fetchall()[0][0]
        cursor.close()
        return np.round(row, 3)



def getStudentWiseGPA(student_id, semester):
    cursor = mydb.cursor()
    cursor.execute(''' 
        SELECT sum(Credits*grade)/sum(Credits)
        FROM(   
                SELECT  Credits,
                    CASE
                        WHEN sum(Marks) >= 85 THEN 4.0
                        WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                        WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                        WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                        WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                        WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                        WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                        WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                        WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                        WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                        ELSE 0.0
                    END as grade
                FROM(
                    SELECT c.clo_id as clo_id,a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks, c.coNum as Credits
                    FROM spms_registration_t r,
                        spms_section_t sc, 
                        spms_course_t c,
                        spms_question_t a, 
                        spms_evaluation_t e
                    WHERE r.section_id = sc.sectionID
                        and sc.course_id = c.clo_id 
                        and r.registration_id = e.registration_id 
                        and e.question_id = a.question_id
                        and r.student_id = '{}'
                        and r.semester='{}' 
                    GROUP BY  c.clo_id,a.assessmentName) Derived 
                GROUP BY clo_id) Derived
                    '''.format(student_id, semester))

    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getSchoolWiseGPA(school, semester):
    cursor = mydb.cursor()
    cursor.execute('''
               SELECT AVG(grade) as avgGrade
               FROM(
                   SELECT student_id,sum(Credits*gradepoint)/sum(Credits) as grade
                   FROM(   
                       SELECT  student_id,Credits,
                           CASE
                               WHEN sum(Marks) >= 85 THEN 4.0
                               WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                               WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                               WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                               WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                               WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                               WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                               WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                               WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                               WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                               ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.student_id as student_id,c.clo_id as clo_id,
                               a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                                spms_department_t d,
                                spms_school_t s,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_question_t a, 
                               spms_evaluation_t e
                           WHERE st.student_id = r.student_id
                                and st.department_id = d.department_id
                                and d.school_id = s.school_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.clo_id 
                                and r.registration_id = e.registration_id 
                                and e.question_id = a.question_id
                                and s.school_id = '{}'
                                and r.semester='{}'
                           GROUP BY  st.student_id,c.clo_id,a.assessmentName) Derived1
                       GROUP BY student_id,clo_id) Derived2
                   GROUP BY student_id)
                       '''.format(school, semester))
    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getDeptWiseGPA(dept, semester):
    cursor = mydb.cursor()
    cursor.execute('''
            SELECT AVG(grade) as avgGrade
            FROM(
                SELECT student_id,sum(Credits*gradepoint)/sum(Credits) as grade
                FROM(   
                    SELECT  student_id,Credits,
                        CASE
                            WHEN sum(Marks) >= 85 THEN 4.0
                            WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                            WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                            WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                            WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                            WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                            WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                            WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                            WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                            WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                            ELSE 0.0
                        END as gradepoint
                    FROM(
                        SELECT st.student_id as student_id,c.clo_id as clo_id,
                            a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks, c.coNum as Credits
                        FROM spms_student_t st,
                            spms_registration_t r,
                            spms_section_t sc, 
                            spms_course_t c,
                            spms_question_t a, 
                            spms_evaluation_t e
                        WHERE st.student_id = r.student_id
                            and r.section_id = sc.sectionID
                            and sc.course_id = c.clo_id 
                            and r.registration_id = e.registration_id 
                            and e.question_id = a.question_id
                            and st.department_id = '{}'
                            and r.semester='{}'
                        GROUP BY  st.student_id,c.clo_id,a.assessmentName) Derived1
                    GROUP BY student_id,clo_id) Derived2
                GROUP BY student_id)
                    '''.format(dept, semester))

    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getProgramWiseGPA(program, semester):
    cursor = mydb.cursor()
    cursor.execute('''
               SELECT AVG(grade) as avgGrade
               FROM(
                   SELECT student_id,sum(Credits*gradepoint)/sum(Credits) as grade
                   FROM(   
                       SELECT  student_id,Credits,
                           CASE
                               WHEN sum(Marks) >= 85 THEN 4.0
                               WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                               WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                               WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                               WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                               WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                               WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                               WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                               WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                               WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                               ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.student_id as student_id,c.clo_id as clo_id,
                               a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_question_t a, 
                               spms_evaluation_t e
                           WHERE st.student_id = r.student_id
                               and r.section_id = sc.sectionID
                               and sc.course_id = c.clo_id 
                               and r.registration_id = e.registration_id 
                               and e.question_id = a.question_id
                               and st.program_id = '{}'
                               and r.semester='{}'
                           GROUP BY  st.student_id,c.clo_id,a.assessmentName) Derived1
                       GROUP BY student_id,clo_id) Derived2
                   GROUP BY student_id)
                       '''.format(program, semester))

    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getCourseWiseGPA(course, semester):
    cursor = mydb.cursor()
    cursor.execute('''
               SELECT AVG(gradepoint) as avgGrade
               FROM(   
                       SELECT  student_id,
                           CASE
                               WHEN sum(Marks) >= 85 THEN 4.0
                               WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                               WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                               WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                               WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                               WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                               WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                               WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                               WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                               WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                               ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.student_id as student_id,c.clo_id as clo_id,
                               a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_question_t a, 
                               spms_evaluation_t e
                           WHERE st.student_id = r.student_id
                               and r.section_id = sc.sectionID
                               and sc.course_id = c.clo_id 
                               and r.registration_id = e.registration_id 
                               and e.question_id = a.question_id
                               and c.clo_id = '{}'
                               and r.semester='{}'
                           GROUP BY  st.student_id,a.assessmentName) Derived
                       GROUP BY student_id) Derived2
                       '''.format(course, semester))

    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getInstructorWiseGPA(instructor, semester):
    cursor = mydb.cursor()
    cursor.execute('''
               SELECT AVG(gradepoint) as avgGrade
               FROM(   
                       SELECT  student_id,
                           CASE
                               WHEN sum(Marks) >= 85 THEN 4.0
                               WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                               WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                               WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                               WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                               WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                               WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                               WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                               WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                               WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                               ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.student_id as student_id,c.clo_id as clo_id,
                               a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_question_t a, 
                               spms_evaluation_t e
                           WHERE st.student_id = r.student_id
                               and r.section_id = sc.sectionID
                               and r.registration_id = e.registration_id 
                               and e.question_id = a.question_id
                               and sc.faculty_id = '{}'
                               and r.semester='{}'
                           GROUP BY  st.student_id,a.assessmentName) Derived
                       GROUP BY student_id) Derived2
                       '''.format(instructor, semester))

    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getInstructorWiseGPAForCourse(course, semester):
    cursor = mydb.cursor()
    cursor.execute('''
               SELECT FacultyID, AVG(gradepoint) as avgGrade
               FROM(   
                       SELECT  FacultyID,student_id,
                           CASE
                               WHEN sum(Marks) >= 85 THEN 4.0
                               WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                               WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                               WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                               WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                               WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                               WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                               WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                               WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                               WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                               ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT sc.faculty_id as FacultyID, st.student_id as student_id,c.clo_id as clo_id,
                               a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_question_t a, 
                               spms_evaluation_t e
                           WHERE st.student_id = r.student_id
                               and r.section_id = sc.sectionID
                               and r.registration_id = e.registration_id 
                               and e.question_id = a.question_id
                               and sc.course_id = '{}'
                               and r.semester='{}'
                           GROUP BY  sc.faculty_id,st.student_id,a.assessmentName) Derived
                       GROUP BY FacultyID,student_id) Derived2
               GROUP BY FacultyID
                       '''.format(course, semester))

    row = cursor.fetchall()
    cursor.close()
    return row


def getHeadWiseGPA(head):
    semlist = getAllSemesters()

    b = -1
    e = -1

    for s in range(0, len(semlist)):
        if semlist[s][0] == head.startDate:
            b = s

        if head.endDate == 'N/A':
            e = len(semlist) - 1
        elif semlist[s][0] == head.endDate:
            e = s

    semesters = []

    for i in range(b, e + 1):
        semesters.append(semlist[i][0])

    cursor = mydb.cursor()

    if len(semesters) == 1:
        cursor.execute('''
                SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT student_id,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  student_id,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.student_id as student_id,c.clo_id as clo_id,
                               a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                                spms_head_t h,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_question_t a, 
                               spms_evaluation_t e
                           WHERE st.student_id = r.student_id
                                and st.department_id = h.department_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.clo_id 
                                and r.registration_id = e.registration_id 
                                and e.question_id = a.question_id
                                and h.headID = '{}'
                                and r.semester='{}'
                           GROUP BY  st.student_id,c.clo_id,a.assessmentName) Derived1
                       GROUP BY student_id,clo_id) Derived2
                   GROUP BY student_id)
                       '''.format(head.headID, semesters[0]))
    else:
        cursor.execute('''
                      SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT student_id,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  student_id,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.student_id as student_id,c.clo_id as clo_id,
                               a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                                spms_head_t h,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_question_t a, 
                               spms_evaluation_t e
                           WHERE st.student_id = r.student_id
                                and st.department_id = h.department_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.clo_id 
                                and r.registration_id = e.registration_id 
                                and e.question_id = a.question_id
                                and h.headID = '{}'
                                and r.semester in {}
                           GROUP BY  st.student_id,c.clo_id,a.assessmentName) Derived1
                       GROUP BY student_id,clo_id) Derived2
                   GROUP BY student_id)
                       '''.format(head.headID, str(tuple(semesters))))
    row = cursor.fetchall()[0][0]
    cursor.close()
    return row


def getDeanWiseGPA(dean):
    semlist = getAllSemesters()

    b = -1
    e = -1

    for s in range(0, len(semlist)):
        if semlist[s][0] == dean.startDate:
            b = s
        if dean.endDate == 'N/A':
            e = len(semlist) - 1
        elif semlist[s][0] == dean.endDate:
            e = s
    semesters = []

    for i in range(b, e + 1):
        semesters.append(semlist[i][0])

    cursor = mydb.cursor()

    if len(semesters) == 1:
        cursor.execute('''
                SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT student_id,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  student_id,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.student_id as student_id,c.clo_id as clo_id,
                               a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                                spms_department_t d,
                                spms_dean_t dn,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_question_t a, 
                               spms_evaluation_t e
                           WHERE st.student_id = r.student_id
                                and st.department_id = d.department_id
                                and d.school_id = dn.school_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.clo_id 
                                and r.registration_id = e.registration_id 
                                and e.question_id = a.question_id
                                and dn.deanID= '{}'
                                and r.semester='{}'
                           GROUP BY  st.student_id,c.clo_id,a.assessmentName) Derived1
                       GROUP BY student_id,clo_id) Derived2
                   GROUP BY student_id)
                       '''.format(dean.deanID, semesters[0]))
    else:
        cursor.execute('''
                       SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT student_id,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  student_id,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.student_id as student_id,c.clo_id as clo_id,
                               a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                                spms_department_t d,
                                spms_dean_t dn,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_question_t a, 
                               spms_evaluation_t e
                           WHERE st.student_id = r.student_id
                                and st.department_id = d.department_id
                                and d.school_id = dn.school_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.clo_id 
                                and r.registration_id = e.registration_id 
                                and e.question_id = a.question_id
                                and dn.deanID= '{}'
                                and r.semester in {}
                           GROUP BY  st.student_id,c.clo_id,a.assessmentName) Derived1
                       GROUP BY student_id,clo_id) Derived2
                   GROUP BY student_id)
                       '''.format(dean.deanID, str(tuple(semesters))))
    row = cursor.fetchall()[0][0]
    cursor.close()
    return row


def getVCWiseGPA(vc):
    semlist = getAllSemesters()

    b = -1
    e = -1

    for s in range(0, len(semlist)):
        if semlist[s][0] == vc.startDate:
            b = s
        if vc.endDate == 'N/A':
            e = len(semlist) - 1
        elif semlist[s][0] == vc.endDate:
            e = s
    semesters = []

    for i in range(b, e + 1):
        semesters.append(semlist[i][0])

    cursor = mydb.cursor()

    if len(semesters) == 1:
        cursor.execute('''
                SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT student_id,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  student_id,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.student_id as student_id,c.clo_id as clo_id,
                               a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_question_t a, 
                               spms_evaluation_t e
                           WHERE st.student_id = r.student_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.clo_id 
                                and r.registration_id = e.registration_id 
                                and e.question_id = a.question_id
                                and r.semester='{}'
                           GROUP BY  st.student_id,c.clo_id,a.assessmentName) Derived1
                       GROUP BY student_id,clo_id) Derived2
                   GROUP BY student_id)
                       '''.format(semesters[0]))
    else:
        print(semesters)
        print(b, e)
        cursor.execute('''
                       SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT student_id,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  student_id,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.student_id as student_id,c.clo_id as clo_id,
                               a.weight*(sum(e.obtained_marks)/sum(a.total_marks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_question_t a, 
                               spms_evaluation_t e
                           WHERE st.student_id = r.student_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.clo_id 
                                and r.registration_id = e.registration_id 
                                and e.question_id = a.question_id
                                and r.semester in {}
                           GROUP BY  st.student_id,c.clo_id,a.assessmentName) Derived1
                       GROUP BY student_id,clo_id) Derived2
                   GROUP BY student_id)
                       '''.format(str(tuple(semesters))))
    row = cursor.fetchall()[0][0]
    cursor.close()
    return row

#CLO Analysis
def getStudentWiseCLO(student_id):
    cursor = mydb.cursor()
    cursor.execute(''' 
                SELECT co.clo_num as clo_num,100*(sum( e.obtained_marks)/sum( a.total_marks)) as clopercent
                FROM spms_registration_t r,
                    spms_question_t a, 
                    spms_evaluation_t e,
                    spms_clo_t co
                WHERE  r.registration_id = e.registration_id 
                    and e.question_id = a.question_id
                    and a.clo_id=co.clo_id
                    and  r.student_id = '{}'
                GROUP BY  co.clo_num
                '''.format(student_id))
    row = cursor.fetchall()
    cursor.close()
    
    CLO=[[]for i in range(2)]
    for i in range(len(row)):
        CLO[0].append(row[i][0])
        CLO[1].append(row[i][1])
    return CLO

# PLO Analysis
def getStudentWisePLO(student_id):
    cursor = mydb.cursor()
    cursor.execute(''' 
                SELECT p.plo_num as plo_num,100*(sum( e.obtained_marks)/sum( a.total_marks)) as plopercent
                FROM spms_registration_t r,
                    spms_question_t a, 
                    spms_evaluation_t e,
                    spms_clo_t co, 
                    spms_plo_t p
                WHERE  r.registration_id = e.registration_id 
                    and e.question_id = a.question_id
                    and a.clo_id=co.clo_id 
                    and co.plo_id = p.plo_id
                    and  r.student_id = '{}'
                GROUP BY  p.plo_id
                '''.format(student_id))
    row = cursor.fetchall()
    cursor.close()
    
    PLO=[[]for i in range(2)]
    for i in range(len(row)):
        PLO[0].append(row[i][0])
        PLO[1].append(row[i][1])
    return PLO


def getCourseWiseStudentPLO(student_id, cat):
    cursor = mydb.cursor()
    cursor.execute(''' 
               SELECT p.plo_num as plo_num,co.course_id,sum(e.obtained_marks),sum(a.total_marks), derived.Total
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
               GROUP BY  p.plo_id,co.course_id
               '''.format(student_id))
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
        temptable = []
        if cat == 'report':
            temptable = [i]

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    if cat == 'report':
                        temptable.append(np.round(100 * k[2] / k[3], 2))
                    elif cat == 'chart':
                        temptable.append(np.round(100 * k[2] / k[4], 2))
                    found = True
            if not found:
                if cat == 'report':
                    temptable.append('N/A')
                elif cat == 'chart':
                    temptable.append(0)
        table.append(temptable)
    return plo, courses, table

def getCOWiseStudentPLO(student_id, cat):
    cursor = mydb.cursor()
    cursor.execute(''' 
               SELECT p.plo_num as plo_num,co.coNum, sum(e.obtained_marks),sum(a.total_marks),derived.Total 
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
               GROUP BY  p.plo_id,co.coNum
               '''.format(student_id))
    row = cursor.fetchall()
    cursor.close()
    table = []
    cos = []

    for entry in row:
        if entry[1] not in cos:
            cos.append(entry[1])
    cos.sort()
    plo = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6", "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]

    for i in cos:
        temptable = []
        if cat == 'report':
            temptable = [i]

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    if cat == 'report':
                        temptable.append(np.round(100 * k[2] / k[3], 2))
                    elif cat == 'chart':
                        temptable.append(np.round(100 * k[2] / k[4], 2))
                    found = True
            if not found:
                if cat == 'report':
                    temptable.append('N/A')
                elif cat == 'chart':
                    temptable.append(0)
        table.append(temptable)
    return plo, cos, table


def getSchoolWisePLO(school):
    cursor = mydb.cursor()
    cursor.execute('''
             SELECT derived.plo_num, avg(per)
             FROM(
                SELECT p.plo_id as plo_id,p.plo_num as plo_num, 100*sum(e.obtained_marks)/sum(a.total_marks) as per
                FROM spms_registration_t r,
                    spms_evaluation_t e,
                    spms_student_t st,
                    spms_department_t d,
                    spms_school_t s,
                    spms_question_t a,
                    spms_clo_t c,
                    spms_plo_t p
                WHERE r.student_id = st.student_id
                    and st.department_id = d.department_id
                    and d.school_id = s.school_id
                    and e.registration_id = r.registration_id
                    and a.question_id = e.question_id
                    and a.clo_id = c.clo_id
                    and c.plo_id = p.plo_id
                    and d.school_id = '{}'
                    GROUP BY p.plo_num,r.student_id) derived
             GROUP BY derived.plo_num
                   '''.format(school))
    row = cursor.fetchall()
    Error Code: 1055. Expression #1 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'spms.p.plo_id' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by

    cursor.close()
    return row


def getDeptWisePLO(dept):
    cursor = mydb.cursor()
    cursor.execute('''
             SELECT derived.plo_num, avg(per)
             FROM(
                SELECT p.plo_id as plo_id,p.plo_num as plo_num, 100*sum(e.obtained_marks)/sum(a.total_marks) as per
                FROM spms_registration_t r,
                    spms_evaluation_t e,
                    spms_student_t st,
                    spms_department_t d,
                    spms_question_t a,
                    spms_clo_t c,
                    spms_plo_t p
                WHERE r.student_id = st.student_id
                    and st.department_id = d.departmentID
                    and e.registration_id = r.registration_id
                    and a.question_id = e.question_id
                    and a.clo_id = c.clo_id
                    and c.plo_id = p.plo_id
                    and st.department_id = '{}'
                    GROUP BY p.plo_num,r.student_id) derived
             GROUP BY derived.plo_num
                   '''.format(dept))
    row = cursor.fetchall()
    cursor.close()
    row.sort(key=len)
    return row


def getProgramWisePLO(program):
    cursor = mydb.cursor()
    cursor.execute('''
             SELECT derived.plo_num, avg(per)
             FROM(
                SELECT p.plo_id as plo_id, p.plo_num as plo_num, 100*sum(e.obtained_marks)/sum(a.total_marks) as per
                FROM spms_registration_t r,
                    spms_evaluation_t e,
                    spms_student_t st,
                    spms_program_t p,
                    spms_question_t a,
                    spms_clo_t c,
                    spms_plo_t p
                WHERE r.student_id = st.student_id
                    and st.program_id = p.program_id
                    and e.registration_id = r.registration_id
                    and a.question_id = e.question_id
                    and a.clo_id = c.clo_id
                    and c.plo_id = p.plo_id
                    and st.program_id = '{}'
                    GROUP BY p.plo_id,r.student_id) derived
             GROUP BY derived.plo_id
                   '''.format(program))
    row = cursor.fetchall()
    cursor.close()
    return row


# Enrollment
def getSchoolWiseEnrolledStudents(school, semesters):
    cursor = mydb.cursor()

    if len(semesters) == 1:
        cursor.execute('''
            SELECT count( distinct st.student_id)
            FROM spms_school_t s,
                spms_department_t d,
                spms_student_t st,
                spms_registration_t r
            WHERE r.student_id = st.student_id
                and st.department_id = d.department_id
                and d.school_id = s.school_id
                 and s.school_id = '{}'
                and r.semester = '{}'
            '''.format(school, semesters[0]))
        row = cursor.fetchall()
    else:
        cursor.execute('''
                   SELECT count( distinct st.student_id)
                   FROM spms_school_t s,
                       spms_department_t d,
                       spms_student_t st,
                       spms_registration_t r
                   WHERE r.student_id = st.student_id
                       and st.department_id = d.department_id
                       and d.school_id = s.school_id
                        and s.school_id = '{}'
                       and r.semester in {}
                   '''.format(school, str(tuple(semesters))))
        row = cursor.fetchall()
        cursor.close()
    return row[0][0]


def getDeptWiseEnrolledStudents(dept, semesters):
    cursor = mydb.cursor()
    if (len(semesters) == 1):
        cursor.execute('''
            SELECT count(distinct st.student_id)
            FROM spms_department_t d,
                spms_student_t st,
                spms_registration_t r
            WHERE r.student_id = st.student_id
                and st.department_id = '{}'
                and r.semester = '{}'
            '''.format(dept, semesters[0]))
        row = cursor.fetchall()
    else:
        cursor.execute('''
                    SELECT count(distinct st.student_id)
                    FROM spms_department_t d,
                        spms_student_t st,
                        spms_registration_t r
                    WHERE r.student_id = st.student_id
                        and st.department_id = '{}'
                        and r.semester in {}
                    '''.format(dept, str(tuple(semesters))))
        row = cursor.fetchall()
        cursor.close()
    return row[0][0]


def getProgramWiseEnrolledStudents(program, semesters):
    cursor = mydb.cursor()

    if len(semesters) == 1:
        cursor.execute('''
            SELECT count( distinct st.student_id)
            FROM spms_program_t p,
                spms_student_t st,
                spms_registration_t r
            WHERE r.student_id = st.student_id
                and st.program_id = p.program_id
                and st.program_id = '{}'
                and r.semester = '{}'
            '''.format(program, semesters[0]))
        row = cursor.fetchall()

    else:
        cursor.execute('''
                   SELECT count( distinct st.student_id)
                   FROM spms_program_t p,
                       spms_student_t st,
                       spms_registration_t r
                   WHERE r.student_id = st.student_id
                       and st.program_id = p.program_id
                       and st.program_id = '{}'
                       and r.semester in {}
                   '''.format(program, str(tuple(semesters))))
        row = cursor.fetchall()

    return row[0][0]


# Semesters Information
def getAllSemesters():
    cursor = mydb.cursor()
    cursor.execute('''
            SELECT DISTINCT semester
            FROM spms_registration_t r    
        ''')

    row = cursor.fetchall()
    cursor.close()
    return row


# PLO Statistics
def getProgramWisePLOStats(program):
    plo = ['PLO1', 'PLO2', 'PLO3', 'PLO4', 'PLO5', 'PLO6', 'PLO7', 'PLO8', 'PLO9', 'PLO10', 'PLO11', 'PLO12']
    achieved = []
    attempted = []

    for p in plo:
        cursor = mydb.cursor()
        cursor.execute('''SELECT COUNT(*)
                FROM(SELECT AVG(percourse) as actual
                    FROM (SELECT r.student_id as student_id, 100*sum(e.obtained_marks)/sum(a.total_marks) as percourse
                        FROM spms_registration_t r,
                            spms_evaluation_t e,
                            spms_question_t a,
                            spms_clo_t c,
                            spms_plo_t p,
                            spms_program_t pr
                        WHERE r.registration_id = e.registration_id
                            and e.question_id = a.question_id
                            and a.clo_id = c.clo_id
                            and c.plo_id = p.plo_id
                            and p.program_id = pr.program_id
                            and pr.program_id='{}'
                            and p.plo_num = '{}'
                        GROUP BY r.student_id,c.clo_id) per
                    GROUP BY per.student_id) avgTable
          '''.format(program, p))
        row = cursor.fetchall()
        cursor.close()
        if row is not None:
                attempted.append(row[0][0])
        else:
                attempted.append(0)

    for p in plo:
        cursor = mydb.cursor()
        cursor.execute('''SELECT COUNT(*)
               FROM(
                SELECT student_id, AVG(percourse) as actual
                FROM(
                           SELECT r.student_id as student_id, 100*sum(e.obtained_marks)/sum(a.total_marks) as percourse
                               FROM spms_registration_t r,
                                   spms_evaluation_t e,
                                   spms_question_t a,
                                   spms_clo_t c,
                                   spms_plo_t p,
                                   spms_program_t pr
                               WHERE r.registration_id = e.registration_id
                                   and e.question_id = a.question_id
                                   and a.clo_id = c.clo_id
                                   and c.plo_id = p.plo_id
                                   and p.program_id = pr.program_id
                                   and pr.program_id='{}'
                                   and p.plo_num ='{}'
                               GROUP BY r.student_id,r.registration_id) d1
                           GROUP BY student_id)d2
                           WHERE actual>=40
               '''.format(program, p))
        row = cursor.fetchall()
        cursor.close()
        if row is not None:
                achieved.append(row[0][0])
        else:
                achieved.append(0)

    return plo, achieved, attempted


def getDeptWisePLOStats(dept):
    cursor = mydb.cursor()

    cursor.execute('''
              SELECT plo_num,COUNT(Marks)
              FROM(
                    SELECT plo_num, student_id, avg(coursemarks) as Marks
                    FROM(
                          SELECT p.plo_num as plo_num, r.student_id as student_id,c.course_id, 
                                100*(sum(e.obtained_marks)/sum(a.total_marks)) as coursemarks
                          FROM spms_student_t st,
                              spms_registration_t r,
                              spms_department_t d,
                              spms_evaluation_t e,
                              spms_question_t a,
                              spms_clo_t c,
                              spms_plo_t p
                          WHERE st.student_id = r.student_id
                              and e.registration_id = r.registration_id
                              and a.question_id = e.question_id
                              and a.clo_id = c.clo_id
                              and c.plo_id = p.plo_id
                              and st.department_id = d.department_id
                              and d.department_id = '{}'
                          GROUP BY p.plo_num, r.student_id,c.course_id) derived1
                      GROUP BY  plo_num,student_id) derived2
                    GROUP BY plo_num
          '''.format(dept))

    row1 = cursor.fetchall()
    cursor.close()
    row1.sort(key=lambda t: len(t[0]))

    cursor.execute('''
                  SELECT plo_num,COUNT(Marks)
                  FROM(
                        SELECT plo_num, student_id, avg(coursemarks) as Marks
                        FROM(
                              SELECT p.plo_num as plo_num, r.student_id as student_id,c.course_id, 
                                    100*(sum(e.obtained_marks)/sum(a.total_marks)) as coursemarks
                              FROM spms_student_t st,
                                  spms_registration_t r,
                                  spms_department_t d,
                                  spms_evaluation_t e,
                                  spms_question_t a,
                                  spms_clo_t c,
                                  spms_plo_t p
                              WHERE st.student_id = r.student_id
                                  and e.registration_id = r.registration_id
                                  and a.question_id = e.question_id
                                  and a.clo_id = c.clo_id
                                  and c.plo_id = p.plo_id
                                  and st.department_id = d.department_id
                                  and d.department_id = '{}'
                              GROUP BY p.plo_num, r.student_id,c.course_id) derived1
                          GROUP BY  plo_num,student_id
                          HAVING avg(coursemarks)>=40) derived2
                        GROUP BY plo_num
              '''.format(dept))

    row2 = cursor.fetchall()
    row2.sort(key=lambda t: len(t[0]))
    cursor.close()
    plo = []
    attempted = []
    achieved = []

    for i in row1:
        plo.append(i[0])
        attempted.append(i[1])

    for i in row2:
        achieved.append(i[1])

    return plo, achieved, attempted


def getSchoolWisePLOStats(school):
    cursor = mydb.cursor()

    cursor.execute('''
              SELECT plo_num,COUNT(Marks)
              FROM(
                    SELECT plo_num, student_id, avg(coursemarks) as Marks
                    FROM(
                          SELECT p.plo_num as plo_num, r.student_id as student_id,c.course_id, 
                                100*(sum(e.obtained_marks)/sum(a.total_marks)) as coursemarks
                          FROM spms_student_t st,
                              spms_registration_t r,
                              spms_department_t d,
                              spms_school_t s,
                              spms_evaluation_t e,
                              spms_question_t a,
                              spms_clo_t c,
                              spms_plo_t p
                          WHERE st.student_id = r.student_id
                              and e.registration_id = r.registration_id
                              and a.question_id = e.question_id
                              and a.clo_id = c.clo_id
                              and c.plo_id = p.plo_id
                              and st.department_id = d.department_id
                              and d.school_id = s.school_id
                              and s.school_id = '{}'
                          GROUP BY p.plo_num, r.student_id,c.course_id) derived1
                      GROUP BY  plo_num,student_id) derived2
                    GROUP BY plo_num
          '''.format(school))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))
    cursor.close()
    cursor.execute('''
                  SELECT plo_num,COUNT(Marks)
                  FROM(
                        SELECT plo_num, student_id, avg(coursemarks) as Marks
                        FROM(
                              SELECT p.plo_num as plo_num, r.student_id as student_id,c.course_id, 
                                    100*(sum(e.obtained_marks)/sum(a.total_marks)) as coursemarks
                              FROM spms_student_t st,
                                  spms_registration_t r,
                                  spms_department_t d,
                                  spms_school_t s,
                                  spms_evaluation_t e,
                                  spms_question_t a,
                                  spms_clo_t c,
                                  spms_plo_t p
                              WHERE st.student_id = r.student_id
                                  and e.registration_id = r.registration_id
                                  and a.question_id = e.question_id
                                  and a.clo_id = c.clo_id
                                  and c.plo_id = p.plo_id
                                  and st.department_id = d.department_id
                                  and d.school_id = s.school_id
                                  and s.school_id = '{}'
                              GROUP BY p.plo_num, r.student_id,c.course_id) derived1
                          GROUP BY  plo_num,student_id
                          HAVING avg(coursemarks)>=40) derived2
                        GROUP BY plo_num
              '''.format(school))

    row2 = cursor.fetchall()
    row2.sort(key=lambda t: len(t[0]))
    cursor.close()
    plo = []
    attempted = []
    achieved = []

    for i in row1:
        plo.append(i[0])
        attempted.append(i[1])

    for i in row2:
        achieved.append(i[1])

    return plo, achieved, attempted


# PLO Comparison
def getSchoolWisePLOComp(school, semester):
    cursor = mydb.cursor()
    cursor.execute('''
        SELECT plo_num,COUNT(*)
        FROM(
            SELECT p.plo_num as plo_num, c.course_id, r.student_id, 100*(sum(e.obtained_marks)/sum(a.total_marks))
            FROM spms_student_t st,
                spms_registration_t r,
                spms_department_t d,
                spms_school_t s,
                spms_evaluation_t e,
                spms_question_t a,
                spms_clo_t c,
                spms_plo_t p
            WHERE st.student_id = r.student_id
                and e.registration_id = r.registration_id
                and a.question_id = e.question_id
                and a.clo_id = c.clo_id
                and c.plo_id = p.plo_id
                and st.department_id = d.department_id
                and d.school_id = s.school_id
                and s.school_id = '{}'
                and r.semester = '{}'
            GROUP BY p.plo_num, c.course_id, r.student_id) derived
        GROUP BY  derived.plo_num
    '''.format(school, semester))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))
    cursor.close()
    cursor.execute('''
            SELECT plo_num,COUNT(*)
            FROM(
                SELECT p.plo_num as plo_num, c.course_id, r.student_id, 100*(sum(e.obtained_marks)/sum(a.total_marks))
                FROM spms_student_t st,
                    spms_registration_t r,
                    spms_department_t d,
                    spms_school_t s,
                    spms_evaluation_t e,
                    spms_question_t a,
                    spms_clo_t c,
                    spms_plo_t p
                WHERE st.student_id = r.student_id
                    and e.registration_id = r.registration_id
                    and a.question_id = e.question_id
                    and a.clo_id = c.clo_id
                    and c.plo_id = p.plo_id
                    and st.department_id = d.department_id
                    and d.school_id = s.school_id
                    and s.school_id = '{}'
                    and r.semester = '{}'
                GROUP BY p.plo_num, c.course_id, r.student_id
                HAVING  100*(sum(e.obtained_marks)/sum(a.total_marks))>=40) derived
            GROUP BY  derived.plo_num
        '''.format(school, semester))

    row2 = cursor.fetchall()
    row2.sort(key=lambda t: len(t[0]))
    cursor.close()
    plo = []
    expected = []
    actual = []

    for r in row1:
        plo.append(r[0])
        expected.append(r[1])

    for r in row2:
        actual.append(r[1])

    return plo, expected, actual


def getDeptWisePLOComp(dept, semester):
    cursor = mydb.cursor()
    cursor.execute('''
        SELECT plo_num,COUNT(*)
        FROM(
            SELECT p.plo_num as plo_num, c.course_id, r.student_id, 100*(sum(e.obtained_marks)/sum(a.total_marks))
            FROM spms_student_t st,
                spms_registration_t r,
                spms_department_t d,
                spms_evaluation_t e,
                spms_question_t a,
                spms_clo_t c,
                spms_plo_t p
            WHERE st.student_id = r.student_id
                and e.registration_id = r.registration_id
                and a.question_id = e.question_id
                and a.clo_id = c.clo_id
                and c.plo_id = p.plo_id
                and st.department_id = d.department_id
                and d.department_id = '{}'
                and r.semester = '{}'
            GROUP BY p.plo_num, c.course_id, r.student_id) derived
        GROUP BY  derived.plo_num
    '''.format(dept, semester))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))
    cursor.close()
    cursor.execute('''
            SELECT plo_num,COUNT(*)
            FROM(
                SELECT p.plo_num as plo_num, c.course_id, r.student_id, 100*(sum(e.obtained_marks)/sum(a.total_marks))
                FROM spms_student_t st,
                    spms_registration_t r,
                    spms_department_t d,
                    spms_evaluation_t e,
                    spms_question_t a,
                    spms_clo_t c,
                    spms_plo_t p
                WHERE st.student_id = r.student_id
                    and e.registration_id = r.registration_id
                    and a.question_id = e.question_id
                    and a.clo_id = c.clo_id
                    and c.plo_id = p.plo_id
                    and st.department_id = d.department_id
                    and d.department_id = '{}'
                    and r.semester = '{}'
                GROUP BY p.plo_num, c.course_id, r.student_id
                HAVING  100*(sum(e.obtained_marks)/sum(a.total_marks))>=40) derived
            GROUP BY  derived.plo_num
        '''.format(dept, semester))

    row2 = cursor.fetchall()
    row2.sort(key=lambda t: len(t[0]))
    cursor.close()
    plo = []
    expected = []
    actual = []

    for r in row1:
        plo.append(r[0])
        expected.append(r[1])

    for r in row2:
        actual.append(r[1])

    return plo, expected,actual


def getProgramWisePLOComp(program, semester):
    cursor = mydb.cursor()
    cursor.execute('''
        SELECT plo_num,COUNT(*)
        FROM(
            SELECT p.plo_num as plo_num, c.course_id, r.student_id, 100*(sum(e.obtained_marks)/sum(a.total_marks))
            FROM spms_student_t st,
                spms_registration_t r,
                spms_program_t pr,
                spms_evaluation_t e,
                spms_question_t a,
                spms_clo_t c,
                spms_plo_t p
            WHERE st.student_id = r.student_id
                and e.registration_id = r.registration_id
                and a.question_id = e.question_id
                and a.clo_id = c.clo_id
                and c.plo_id = p.plo_id
                and st.program_id = pr.program_id
                and pr.program_id = '{}'
                and r.semester = '{}'
            GROUP BY p.plo_num, c.course_id, r.student_id) derived
        GROUP BY  derived.plo_num
    '''.format(program, semester))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))
    cursor.close()
    cursor.execute('''
            SELECT plo_num,COUNT(*)
            FROM(
                SELECT p.plo_num as plo_num, c.course_id, r.student_id, 100*(sum(e.obtained_marks)/sum(a.total_marks))
                FROM spms_student_t st,
                    spms_registration_t r,
                    spms_program_t pr,
                    spms_evaluation_t e,
                    spms_question_t a,
                    spms_clo_t c,
                    spms_plo_t p
                WHERE st.student_id = r.student_id
                    and e.registration_id = r.registration_id
                    and a.question_id = e.question_id
                    and a.clo_id = c.clo_id
                    and c.plo_id = p.plo_id
                    and st.program_id = pr.program_id
                    and pr.program_id = '{}'
                    and r.semester = '{}'
                GROUP BY p.plo_id, c.course_id, r.student_id
                HAVING  100*(sum(e.obtained_marks)/sum(a.total_marks))>=40) derived
            GROUP BY  derived.plo_num
        '''.format(program, semester))

    row2 = cursor.fetchall()
    row2.sort(key=lambda t: len(t[0]))
    cursor.close()
    plo = []
    expected = []
    actual = []

    for r in row1:
        plo.append(r[0])
        expected.append(r[1])

    for r in row2:
        actual.append(r[1])

    return plo, expected, actual


def getCourseWisePLOComp(course, semester):
    cursor = mydb.cursor()

    cursor.execute('''
        SELECT plo_num, COUNT(marks)
        FROM(
            SELECT p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
            FROM spms_registration_t r,
                spms_evaluation_t e,
                spms_question_t a,
                spms_clo_t c,
                spms_plo_t p
            WHERE r.registration_id = e.registration_id
                and e.question_id = a.question_id
                and a.clo_id = c.clo_id
                and c.plo_id = p.plo_id
                and c.course_id = '{}'
                and r.semester ='{}'
            GROUP BY p.plo_num,r.student_id) derived1
        GROUP BY plo_num
    '''.format(course, semester))

    temp1 = cursor.fetchall()
    cursor.close()
    temp1.sort(key=lambda t: len(t[0]))

    expected = temp1[0][1]
    cursor.execute('''
           SELECT plo_num, COUNT(marks)
           FROM(
               SELECT p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
               FROM spms_registration_t r,
                   spms_evaluation_t e,
                   spms_question_t a,
                   spms_clo_t c,
                   spms_plo_t p
               WHERE r.registration_id = e.registration_id
                   and e.question_id = a.question_id
                   and a.clo_id = c.clo_id
                   and c.plo_id = p.plo_id
                   and c.course_id = '{}'
                   and r.semester ='{}'
               GROUP BY p.plo_num,r.student_id
               HAVING 100*sum(e.obtained_marks)/sum(a.total_marks)>=40) derived1
           GROUP BY plo_num
       '''.format(course, semester))

    actual = []
    temp2 = cursor.fetchall()
    temp2.sort(key=lambda t: len(t[0]))
    cursor.close()
    plo = []

    for i in temp2:
        plo.append(i[0])
        actual.append(i[1])

    return plo, expected, actual


def getStudentWisePLOComp(student, semester):
    cursor = mydb.cursor()

    cursor.execute('''
        SELECT  COUNT(marks)
        FROM(
            SELECT p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
            FROM spms_registration_t r,
                spms_evaluation_t e,
                spms_question_t a,
                spms_clo_t c,
                spms_plo_t p
            WHERE r.registration_id = e.registration_id
                and e.question_id = a.question_id
                and a.clo_id = c.clo_id
                and c.plo_id = p.plo_id
                and r.student_id='{}'
                and r.semester ='{}'
            GROUP BY p.plo_num,c.course_id) derived1
    '''.format(student, semester))

    expected = cursor.fetchall()
    cursor.close()
    cursor.execute('''
           SELECT COUNT(marks)
           FROM(
               SELECT p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
               FROM spms_registration_t r,
                   spms_evaluation_t e,
                   spms_question_t a,
                   spms_clo_t c,
                   spms_plo_t p
               WHERE r.registration_id = e.registration_id
                   and e.question_id = a.question_id
                   and a.clo_id = c.clo_id
                   and c.plo_id = p.plo_id
                   and r.student_id = '{}'
                   and r.semester ='{}'
               GROUP BY p.plo_num,c.course_id
               HAVING 100*sum(e.obtained_marks)/sum(a.total_marks)>=40) derived1
       '''.format(student, semester))

    actual = cursor.fetchall()
    cursor.close()
    return expected[0][0], actual[0][0]


# Report
def getCourseReport(course):
    row = []
    total = 0
    cursor = mydb.cursor()
    cursor.execute('''
               SELECT coNum, plo_num, COUNT(marks)
               FROM(
                       SELECT c.coNum as coNum,p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
                       FROM spms_registration_t r,
                           spms_evaluation_t e,
                           spms_question_t a, 
                           spms_clo_t c,
                           spms_plo_t p
                       WHERE r.registration_id = e.registration_id
                           and e.question_id = a.question_id
                           and a.clo_id = c.clo_id
                           and c.plo_id = p.plo_id
                            and c.course_id = '{}'
                       GROUP BY r.student_id,c.course_id,c.clo_id, p.plo_id
                       )derived
               WHERE marks>=40
               GROUP BY coNum,plo_num
               '''.format(course))
    row = cursor.fetchall()
    cursor.close()
    if row is None:
        row = []

    cursor = mydb.cursor()
    cursor.execute('''
               SELECT coNum, plo_num, COUNT(marks)
               FROM(
                       SELECT r.student_id as student_id,c.course_id as clo_id,c.coNum as coNum,
                       p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
                       FROM spms_registration_t r,
                           spms_evaluation_t e,
                           spms_question_t a, 
                           spms_clo_t c,
                           spms_plo_t p
                       WHERE r.registration_id = e.registration_id
                           and e.question_id = a.question_id
                           and a.clo_id = c.clo_id
                           and c.plo_id = p.plo_id
                            and c.course_id = '{}'
                       GROUP BY r.student_id,c.course_id,c.clo_id, p.plo_id
                       )derived
                GROUP BY clo_id,coNum,plo_num
               '''.format(course))
    total = cursor.fetchone()[2]
    cursor.close()
    coplo = []
    temp = []
    for i in row:
        temp.append(i[2])
        coplo.append([i[0], i[1]])
    temp = np.array(temp)

    success = np.round(temp / total * 100, 3)
    failCount = total - temp
    fail = np.round(failCount / total * 100, 3)
    row = np.column_stack((temp, success, failCount, fail)).tolist()

    finalRow = []
    for i in range(len(row)):
        tempRow = coplo[i]
        for j in range(len(row[i])):
            tempRow.append(row[i][j])
        finalRow.append(tempRow)

    return (finalRow, total)


def getProgramReport(program):
    cursor = mydb.cursor()

    cursor.execute('''
        SELECT coNum, COUNT(marks)
        FROM(
            SELECT c.coNum as coNum,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
            FROM spms_student_t st, 
                spms_registration_t r,
                spms_evaluation_t e,
                spms_question_t a, 
                spms_clo_t c
            WHERE st.student_id = r.student_id
                and r.registration_id = e.registration_id
                and e.question_id = a.question_id
                and a.clo_id = c.clo_id
                and st.program_id = '{}'
            GROUP BY c.coNum,r.student_id) derived
        GROUP BY coNum
    '''.format(program))

    row1 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT coNum, COUNT(marks)
            FROM(
                SELECT c.coNum as coNum,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
                FROM spms_student_t st, 
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_question_t a, 
                    spms_clo_t c
                WHERE st.student_id = r.student_id
                    and r.registration_id = e.registration_id
                    and e.question_id = a.question_id
                    and a.clo_id = c.clo_id
                    and st.program_id = '{}'
                GROUP BY c.coNum,r.student_id) derived
            WHERE marks>=40
            GROUP BY coNum
        '''.format(program))

    row2 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT plo_num, COUNT(marks)
            FROM(
                SELECT p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
                FROM spms_student_t st, 
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_question_t a, 
                    spms_clo_t c,
                    spms_plo_t p
                WHERE st.student_id = r.student_id
                    and r.registration_id = e.registration_id
                    and e.question_id = a.question_id
                    and a.clo_id = c.clo_id
                    and c.plo_id = p.plo_id
                    and st.program_id = '{}'
                GROUP BY p.plo_num,r.student_id) derived
            GROUP BY plo_num
        '''.format(program))

    row3 = cursor.fetchall()
    cursor.close()
    row3.sort(key=lambda t: len(t[0]))

    cursor.execute('''
                SELECT plo_num, COUNT(marks)
                FROM(
                    SELECT p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
                    FROM spms_student_t st, 
                        spms_registration_t r,
                        spms_evaluation_t e,
                        spms_question_t a, 
                        spms_clo_t c,
                        spms_plo_t p
                    WHERE st.student_id = r.student_id
                        and r.registration_id = e.registration_id
                        and e.question_id = a.question_id
                        and a.clo_id = c.clo_id
                        and c.plo_id = p.plo_id
                        and st.program_id = '{}'
                    GROUP BY p.plo_num,r.student_id) derived
                WHERE marks>=40
                GROUP BY plo_num
            '''.format(program))

    row4 = cursor.fetchall()
    cursor.close()
    row4.sort(key=lambda t: len(t[0]))

    finalrow = []

    for i in range(len(row1)):
        temp = []
        tot = row1[i][1]
        suc = row2[i][1]

        temp.append(row1[i][0])
        temp.append(tot)
        temp.append(suc)
        temp.append(np.round(100 * suc / tot, 2))
        temp.append(tot - suc)
        temp.append(np.round(100 * (tot - suc) / tot, 2))

        finalrow.append(temp)

    for i in range(len(row3)):
        temp = []
        tot = row3[i][1]
        suc = row4[i][1]

        temp.append(row3[i][0])
        temp.append(tot)
        temp.append(suc)
        temp.append(np.round(100 * suc / tot, 2))
        temp.append(tot - suc)
        temp.append(np.round(100 * (tot - suc) / tot, 2))

        finalrow.append(temp)

    return finalrow


def getDeptReport(dept):
    cursor = mydb.cursor()

    cursor.execute('''
        SELECT coNum, COUNT(marks)
        FROM(
            SELECT c.coNum as coNum,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
            FROM spms_student_t st, 
                spms_registration_t r,
                spms_evaluation_t e,
                spms_question_t a, 
                spms_clo_t c
            WHERE st.student_id = r.student_id
                and r.registration_id = e.registration_id
                and e.question_id = a.question_id
                and a.clo_id = c.clo_id
                and st.department_id = '{}'
            GROUP BY c.coNum,r.student_id) derived
        GROUP BY coNum
    '''.format(dept))

    row1 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT coNum, COUNT(marks)
            FROM(
                SELECT c.coNum as coNum,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
                FROM spms_student_t st, 
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_question_t a, 
                    spms_clo_t c
                WHERE st.student_id = r.student_id
                    and r.registration_id = e.registration_id
                    and e.question_id = a.question_id
                    and a.clo_id = c.clo_id
                    and st.department_id = '{}'
                GROUP BY c.coNum,r.student_id) derived
            WHERE marks>=40
            GROUP BY coNum
        '''.format(dept))

    row2 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT plo_num, COUNT(marks)
            FROM(
                SELECT p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
                FROM spms_student_t st, 
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_question_t a, 
                    spms_clo_t c,
                    spms_plo_t p
                WHERE st.student_id = r.student_id
                    and r.registration_id = e.registration_id
                    and e.question_id = a.question_id
                    and a.clo_id = c.clo_id
                    and c.plo_id = p.plo_id
                    and st.department_id = '{}'
                GROUP BY p.plo_num,r.student_id) derived
            GROUP BY plo_num
        '''.format(dept))

    row3 = cursor.fetchall()
    cursor.close()
    row3.sort(key=lambda t: len(t[0]))

    cursor.execute('''
                SELECT plo_num, COUNT(marks)
                FROM(
                    SELECT p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
                    FROM spms_student_t st, 
                        spms_registration_t r,
                        spms_evaluation_t e,
                        spms_question_t a, 
                        spms_clo_t c,
                        spms_plo_t p
                    WHERE st.student_id = r.student_id
                        and r.registration_id = e.registration_id
                        and e.question_id = a.question_id
                        and a.clo_id = c.clo_id
                        and c.plo_id = p.plo_id
                        and st.department_id = '{}'
                    GROUP BY p.plo_num,r.student_id) derived
                WHERE marks>=40
                GROUP BY plo_num
            '''.format(dept))

    row4 = cursor.fetchall()
    cursor.close()      
    row4.sort(key=lambda t: len(t[0]))

    finalrow = []

    for i in range(len(row1)):
        temp = []
        tot = row1[i][1]
        suc = row2[i][1]

        temp.append(row1[i][0])
        temp.append(tot)
        temp.append(suc)
        temp.append(np.round(100 * suc / tot, 2))
        temp.append(tot - suc)
        temp.append(np.round(100 * (tot - suc) / tot, 2))

        finalrow.append(temp)

    for i in range(len(row3)):
        temp = []
        tot = row3[i][1]
        suc = row4[i][1]

        temp.append(row3[i][0])
        temp.append(tot)
        temp.append(suc)
        temp.append(np.round(100 * suc / tot, 2))
        temp.append(tot - suc)
        temp.append(np.round(100 * (tot - suc) / tot, 2))

        finalrow.append(temp)

    return finalrow


def getSchoolReport(school):
    cursor = mydb.cursor()

    cursor.execute('''
        SELECT coNum, COUNT(marks)
        FROM(
            SELECT c.coNum as coNum,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
            FROM spms_student_t st, 
                spms_department_t d,
                spms_school_t s,
                spms_registration_t r,
                spms_evaluation_t e,
                spms_question_t a, 
                spms_clo_t c
            WHERE st.student_id = r.student_id
                and st.department_id = d.department_id
                and d.school_id = s.school_id
                and r.registration_id = e.registration_id
                and e.question_id = a.question_id
                and a.clo_id = c.clo_id
                and s.school_id = '{}'
            GROUP BY c.coNum,r.student_id) derived
        GROUP BY coNum
    '''.format(school))

    row1 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT coNum, COUNT(marks)
            FROM(
                SELECT c.coNum as coNum,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
                FROM spms_student_t st, 
                    spms_department_t d,
                    spms_school_t s,
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_question_t a, 
                    spms_clo_t c
                WHERE st.student_id = r.student_id
                    and st.department_id = d.department_id
                    and d.school_id = s.school_id
                    and r.registration_id = e.registration_id
                    and e.question_id = a.question_id
                    and a.clo_id = c.clo_id
                    and s.school_id = '{}'
                    GROUP BY c.coNum,r.student_id) derived
            WHERE marks>=40
            GROUP BY coNum
        '''.format(school))

    row2 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT plo_num, COUNT(marks)
            FROM(
                SELECT p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
                FROM spms_student_t st, 
                    spms_department_t d,
                    spms_school_t s,
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_question_t a, 
                    spms_clo_t c,
                    spms_plo_t p
                WHERE st.student_id = r.student_id
                    and st.department_id = d.department_id
                    and d.school_id = s.school_id
                    and r.registration_id = e.registration_id
                    and e.question_id = a.question_id
                    and a.clo_id = c.clo_id
                    and c.plo_id = p.plo_id
                    and s.school_id = '{}'
                    GROUP BY p.plo_num,r.student_id) derived
            GROUP BY plo_num
        '''.format(school))

    row3 = cursor.fetchall()
    cursor.close()
    row3.sort(key=lambda t: len(t[0]))

    cursor.execute('''
                SELECT plo_num, COUNT(marks)
                FROM(
                    SELECT p.plo_num as plo_num,100*sum(e.obtained_marks)/sum(a.total_marks) as marks
                    FROM spms_student_t st, 
                        spms_department_t d,
                        spms_school_t s,
                        spms_registration_t r,
                        spms_evaluation_t e,
                        spms_question_t a, 
                        spms_clo_t c,
                        spms_plo_t p
                    WHERE st.student_id = r.student_id
                        and st.department_id = d.department_id
                        and d.school_id = s.school_id
                        and r.registration_id = e.registration_id
                        and e.question_id = a.question_id
                        and a.clo_id = c.clo_id
                        and c.plo_id = p.plo_id
                        and s.school_id = '{}'
                    GROUP BY p.plo_num,r.student_id) derived
                WHERE marks>=40
                GROUP BY plo_num
            '''.format(school))

    row4 = cursor.fetchall()
    cursor.close()
    row4.sort(key=lambda t: len(t[0]))

    finalrow = []

    for i in range(len(row1)):
        temp = []
        tot = row1[i][1]
        suc = row2[i][1]

        temp.append(row1[i][0])
        temp.append(tot)
        temp.append(suc)
        temp.append(np.round(100 * suc / tot, 2))
        temp.append(tot - suc)
        temp.append(np.round(100 * (tot - suc) / tot, 2))

        finalrow.append(temp)

    for i in range(len(row3)):
        temp = []
        tot = row3[i][1]
        suc = row4[i][1]

        temp.append(row3[i][0])
        temp.append(tot)
        temp.append(suc)
        temp.append(np.round(100 * suc / tot, 2))
        temp.append(tot - suc)
        temp.append(np.round(100 * (tot - suc) / tot, 2))

        finalrow.append(temp)

    return finalrow

def getQuestion(semester,course_id,section_num,assessment_name):
    cursor=mydb.cursor()
    cursor.execute('''
            SELECT st.section_id
            FROM spms_student_t st,
            WHERE st.semester='{}'
            and st.course_id='{}'
            and st.section_num='{}'
            )'''.format(semester,course_id,section_num))
    cursor.close()
    sectionid=cursor.fetchall()
    cursor.execute('''
            SELECT st.question_id
            FROM spms_question_t st,
            WHERE st.section_id='{}'
            and st.question_id= '{}'
            )'''.format(sectionid,assessment_name))
    cursor.close()
    question=cursor.fetchall()
    return question

