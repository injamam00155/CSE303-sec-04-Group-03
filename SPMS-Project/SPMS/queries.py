from SPMS import dbConnection
import mysql.connector
from django.db import connection
import numpy as np

mydb=dbConnection.queriesDB()


# print(mydb)
# cursor = mydb.cursor()
# print(cursor)



##user info based queries
def getGroup(username):
            cursor = mydb.cursor()
            cursor.execute('''        
            SELECT grp    
            FROM spms_users_t
            WHERE userID={}'''.format(username))
            group=cursor.fetchall()[0][0]
            cursor.close()
            return group

def getName(username):
            cursor = mydb.cursor()
            name=""
            if getGroup(username)=="student":
                str="student"
            elif getGroup(username)=="faculty":
                str="faculty"
            cursor.execute('''        
            SELECT firstName,lastName   
            FROM spms_{}_t
            WHERE {}ID={}'''.format(str,str,username))
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


def setCurrUser(username):
    try:
        cursor = mydb.cursor()
        group=getGroup(username)
        #injamam
        cursor.execute('''        
        INSERT INTO spms.spms_currsess_t 
        VALUES ({}, '{}')
        '''.format(username,group))
        rows=cursor.fetchall()
        cursor.close()
    except:
        print("an exception occurred")
        cursor.close()
    return


def deleteCurrUser():
    if getCurrUser():
        cursor = mydb.cursor()
        cursor.execute('''TRUNCATE TABLE spms.spms_currsess_t''')
        rows=cursor.fetchall()
        cursor.close()
    return



def getCurrUser():
    cursor = mydb.cursor()
    cursor.execute('''SELECT userID,grp FROM spms_currsess_t''')
    try:
        rows=cursor.fetchall()
        cursor.close()
    except:
        cursor.close()
    return rows[0]


def isValid(username):
    cursor = mydb.cursor()
    cursor.execute('''        
    SELECT *     
    FROM spms_users_t
    WHERE userID={}'''.format(username))
    rows=cursor.fetchall()
    cursor.close()
    return bool(rows)


def getPassword(username):
        cursor = mydb.cursor()
        cursor.execute('''        
            SELECT password     
            FROM spms_users_t
            WHERE userID={}'''.format(username))
        password=cursor.fetchall()[0][0]
        cursor.close()
        return password


## Analysis
def getStudentCourseWiseCO(username,courseid):
    cursor = mydb.cursor()
    cursor.execute('''
    SELECT coNum, (100*(sum( e.obtainedMarks)/sum( a.totalMarks))) as copercent
                FROM spms_registration_t r,
                    spms_assessment_t a, 
                    spms_evaluation_t e,
					spms_clo_t clo,
                    spms_plo_t p
                WHERE  r.registrationID = e.registration_id 
                    and e.assessment_id = a.assessmentID
                    and a.co_id=clo.coID 
                    and clo.plo_id = p.ploID
                    and  r.student_id = {}
		    and clo.course_id="{}"
                GROUP BY  clo.coID'''.format(username,courseid))
    rows=cursor.fetchall()
    cursor.close()
    return bool(rows)


# GPA Analysis

def getStudentCGPA(studentID):
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
                    SELECT c.coID as coID,a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.coNum as Credits
                    FROM spms_registration_t r,
                        spms_section_t sc, 
                        spms_course_t c,
                        spms_assessment_t a, 
                        spms_evaluation_t e
                    WHERE r.section_id = sc.sectionID
                        and sc.course_id = c.coID 
                        and r.registrationID = e.registration_id 
                        and e.assessment_id = a.assessmentID
                        and r.student_id = '{}'
                    GROUP BY  c.coID,a.assessmentName) Derived 
                GROUP BY coID) Derived
                    '''.format(studentID))
        row = cursor.fetchall()[0][0]
        cursor.close()
        return np.round(row, 3)



def getStudentWiseGPA(studentID, semester):
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
                    SELECT c.coID as coID,a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.coNum as Credits
                    FROM spms_registration_t r,
                        spms_section_t sc, 
                        spms_course_t c,
                        spms_assessment_t a, 
                        spms_evaluation_t e
                    WHERE r.section_id = sc.sectionID
                        and sc.course_id = c.coID 
                        and r.registrationID = e.registration_id 
                        and e.assessment_id = a.assessmentID
                        and r.student_id = '{}'
                        and r.semester='{}' 
                    GROUP BY  c.coID,a.assessmentName) Derived 
                GROUP BY coID) Derived
                    '''.format(studentID, semester))

    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getSchoolWiseGPA(school, semester):
    cursor = mydb.cursor()
    cursor.execute('''
               SELECT AVG(grade) as avgGrade
               FROM(
                   SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                   FROM(   
                       SELECT  StudentID,Credits,
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
                           SELECT st.studentID as StudentID,c.coID as coID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                                spms_department_t d,
                                spms_school_t s,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_assessment_t a, 
                               spms_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and st.department_id = d.departmentID
                                and d.school_id = s.schoolID
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.coID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and s.schoolID = '{}'
                                and r.semester='{}'
                           GROUP BY  st.studentID,c.coID,a.assessmentName) Derived1
                       GROUP BY StudentID,coID) Derived2
                   GROUP BY StudentID)
                       '''.format(school, semester))
    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getDeptWiseGPA(dept, semester):
    cursor = mydb.cursor()
    cursor.execute('''
            SELECT AVG(grade) as avgGrade
            FROM(
                SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                FROM(   
                    SELECT  StudentID,Credits,
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
                        SELECT st.studentID as StudentID,c.coID as coID,
                            a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.coNum as Credits
                        FROM spms_student_t st,
                            spms_registration_t r,
                            spms_section_t sc, 
                            spms_course_t c,
                            spms_assessment_t a, 
                            spms_evaluation_t e
                        WHERE st.studentID = r.student_id
                            and r.section_id = sc.sectionID
                            and sc.course_id = c.coID 
                            and r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID
                            and st.department_id = '{}'
                            and r.semester='{}'
                        GROUP BY  st.studentID,c.coID,a.assessmentName) Derived1
                    GROUP BY StudentID,coID) Derived2
                GROUP BY StudentID)
                    '''.format(dept, semester))

    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getProgramWiseGPA(program, semester):
    cursor = mydb.cursor()
    cursor.execute('''
               SELECT AVG(grade) as avgGrade
               FROM(
                   SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                   FROM(   
                       SELECT  StudentID,Credits,
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
                           SELECT st.studentID as StudentID,c.coID as coID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_assessment_t a, 
                               spms_evaluation_t e
                           WHERE st.studentID = r.student_id
                               and r.section_id = sc.sectionID
                               and sc.course_id = c.coID 
                               and r.registrationID = e.registration_id 
                               and e.assessment_id = a.assessmentID
                               and st.program_id = '{}'
                               and r.semester='{}'
                           GROUP BY  st.studentID,c.coID,a.assessmentName) Derived1
                       GROUP BY StudentID,coID) Derived2
                   GROUP BY StudentID)
                       '''.format(program, semester))

    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getCourseWiseGPA(course, semester):
    cursor = mydb.cursor()
    cursor.execute('''
               SELECT AVG(gradepoint) as avgGrade
               FROM(   
                       SELECT  StudentID,
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
                           SELECT st.studentID as StudentID,c.coID as coID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_assessment_t a, 
                               spms_evaluation_t e
                           WHERE st.studentID = r.student_id
                               and r.section_id = sc.sectionID
                               and sc.course_id = c.coID 
                               and r.registrationID = e.registration_id 
                               and e.assessment_id = a.assessmentID
                               and c.coID = '{}'
                               and r.semester='{}'
                           GROUP BY  st.studentID,a.assessmentName) Derived
                       GROUP BY StudentID) Derived2
                       '''.format(course, semester))

    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getInstructorWiseGPA(instructor, semester):
    cursor = mydb.cursor()
    cursor.execute('''
               SELECT AVG(gradepoint) as avgGrade
               FROM(   
                       SELECT  StudentID,
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
                           SELECT st.studentID as StudentID,c.coID as coID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_assessment_t a, 
                               spms_evaluation_t e
                           WHERE st.studentID = r.student_id
                               and r.section_id = sc.sectionID
                               and r.registrationID = e.registration_id 
                               and e.assessment_id = a.assessmentID
                               and sc.faculty_id = '{}'
                               and r.semester='{}'
                           GROUP BY  st.studentID,a.assessmentName) Derived
                       GROUP BY StudentID) Derived2
                       '''.format(instructor, semester))

    row = cursor.fetchall()[0][0]
    cursor.close()
    return np.round(row, 3)


def getInstructorWiseGPAForCourse(course, semester):
    cursor = mydb.cursor()
    cursor.execute('''
               SELECT FacultyID, AVG(gradepoint) as avgGrade
               FROM(   
                       SELECT  FacultyID,StudentID,
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
                           SELECT sc.faculty_id as FacultyID, st.studentID as StudentID,c.coID as coID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_assessment_t a, 
                               spms_evaluation_t e
                           WHERE st.studentID = r.student_id
                               and r.section_id = sc.sectionID
                               and r.registrationID = e.registration_id 
                               and e.assessment_id = a.assessmentID
                               and sc.course_id = '{}'
                               and r.semester='{}'
                           GROUP BY  sc.faculty_id,st.studentID,a.assessmentName) Derived
                       GROUP BY FacultyID,StudentID) Derived2
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
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
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
                           SELECT st.studentID as StudentID,c.coID as coID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                                spms_head_t h,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_assessment_t a, 
                               spms_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and st.department_id = h.department_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.coID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and h.headID = '{}'
                                and r.semester='{}'
                           GROUP BY  st.studentID,c.coID,a.assessmentName) Derived1
                       GROUP BY StudentID,coID) Derived2
                   GROUP BY StudentID)
                       '''.format(head.headID, semesters[0]))
    else:
        cursor.execute('''
                      SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
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
                           SELECT st.studentID as StudentID,c.coID as coID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                                spms_head_t h,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_assessment_t a, 
                               spms_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and st.department_id = h.department_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.coID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and h.headID = '{}'
                                and r.semester in {}
                           GROUP BY  st.studentID,c.coID,a.assessmentName) Derived1
                       GROUP BY StudentID,coID) Derived2
                   GROUP BY StudentID)
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
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
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
                           SELECT st.studentID as StudentID,c.coID as coID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                                spms_department_t d,
                                spms_dean_t dn,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_assessment_t a, 
                               spms_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and st.department_id = d.departmentID
                                and d.school_id = dn.school_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.coID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and dn.deanID= '{}'
                                and r.semester='{}'
                           GROUP BY  st.studentID,c.coID,a.assessmentName) Derived1
                       GROUP BY StudentID,coID) Derived2
                   GROUP BY StudentID)
                       '''.format(dean.deanID, semesters[0]))
    else:
        cursor.execute('''
                       SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
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
                           SELECT st.studentID as StudentID,c.coID as coID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                                spms_department_t d,
                                spms_dean_t dn,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_assessment_t a, 
                               spms_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and st.department_id = d.departmentID
                                and d.school_id = dn.school_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.coID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and dn.deanID= '{}'
                                and r.semester in {}
                           GROUP BY  st.studentID,c.coID,a.assessmentName) Derived1
                       GROUP BY StudentID,coID) Derived2
                   GROUP BY StudentID)
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
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
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
                           SELECT st.studentID as StudentID,c.coID as coID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_assessment_t a, 
                               spms_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.coID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and r.semester='{}'
                           GROUP BY  st.studentID,c.coID,a.assessmentName) Derived1
                       GROUP BY StudentID,coID) Derived2
                   GROUP BY StudentID)
                       '''.format(semesters[0]))
    else:
        print(semesters)
        print(b, e)
        cursor.execute('''
                       SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
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
                           SELECT st.studentID as StudentID,c.coID as coID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.coNum as Credits
                           FROM spms_student_t st,
                               spms_registration_t r,
                               spms_section_t sc, 
                               spms_course_t c,
                               spms_assessment_t a, 
                               spms_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.coID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and r.semester in {}
                           GROUP BY  st.studentID,c.coID,a.assessmentName) Derived1
                       GROUP BY StudentID,coID) Derived2
                   GROUP BY StudentID)
                       '''.format(str(tuple(semesters))))
    row = cursor.fetchall()[0][0]
    cursor.close()
    return row


# PLO Analysis
def getStudentWisePLO(studentID):
    cursor = mydb.cursor()
    cursor.execute(''' 
                SELECT p.ploNum as plonum,100*(sum( e.obtainedMarks)/sum( a.totalMarks)) as plopercent
                FROM spms_registration_t r,
                    spms_assessment_t a, 
                    spms_evaluation_t e,
                    spms_co_t co, 
                    spms_plo_t p
                WHERE  r.registrationID = e.registration_id 
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and  r.student_id = '{}'
                GROUP BY  p.ploID
                '''.format(studentID))
    row = cursor.fetchall()
    cursor.close()
    return row


def getCourseWiseStudentPLO(studentID, cat):
    cursor = mydb.cursor()
    cursor.execute(''' 
               SELECT p.ploNum as ploNum,co.course_id,sum(e.obtainedMarks),sum(a.totalMarks), derived.Total
               FROM spms_registration_t r,
                   spms_assessment_t a, 
                   spms_evaluation_t e,
                   spms_co_t co, 
                   spms_plo_t p,
                   (
                        SELECT p.ploNum as ploNum,sum(a.totalMarks) as Total, r.student_id as StudentID
                        FROM spms_registration_t r,
                            spms_assessment_t a, 
                            spms_evaluation_t e,
                            spms_co_t co, 
                            spms_plo_t p
                        WHERE r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID
                            and a.co_id=co.coID 
                            and co.plo_id = p.ploID 
                            and r.student_id = '{}'
                        GROUP BY  r.student_id,p.ploID) derived
               WHERE r.student_id = derived.StudentID
                    and e.registration_id = r.registrationID
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and p.ploNum = derived.ploNum
               GROUP BY  p.ploID,co.course_id
               '''.format(studentID))
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


def getCOWiseStudentPLO(studentID, cat):
    cursor = mydb.cursor()
    cursor.execute(''' 
               SELECT p.ploNum as ploNum,co.coNum, sum(e.obtainedMarks),sum(a.totalMarks),derived.Total 
               FROM spms_registration_t r,
                   spms_assessment_t a, 
                   spms_evaluation_t e,
                   spms_co_t co, 
                   spms_plo_t p,
                   (
                        SELECT p.ploNum as ploNum,sum(a.totalMarks) as Total, r.student_id as StudentID
                        FROM spms_registration_t r,
                            spms_assessment_t a, 
                            spms_evaluation_t e,
                            spms_co_t co, 
                            spms_plo_t p
                        WHERE r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID
                            and a.co_id=co.coID 
                            and co.plo_id = p.ploID 
                            and r.student_id = '{}'
                        GROUP BY  r.student_id,p.ploID) derived
               WHERE r.student_id = derived.StudentID
                    and e.registration_id = r.registrationID
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and p.ploNum = derived.ploNum
               GROUP BY  p.ploID,co.coNum
               '''.format(studentID))
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
             SELECT derived.plonum, avg(per)
             FROM(
                SELECT p.ploID as PLOID,p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as per
                FROM spms_registration_t r,
                    spms_evaluation_t e,
                    spms_student_t st,
                    spms_department_t d,
                    spms_school_t s,
                    spms_assessment_t a,
                    spms_co_t c,
                    spms_plo_t p
                WHERE r.student_id = st.studentID
                    and st.department_id = d.departmentID
                    and d.school_id = s.schoolID
                    and e.registration_id = r.registrationID
                    and a.assessmentID = e.assessment_id
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and d.school_id = '{}'
                    GROUP BY p.ploNum,r.student_id) derived
             GROUP BY derived.ploNum
                   '''.format(school))
    row = cursor.fetchall()
    cursor.close()
    return row


def getDeptWisePLO(dept):
    cursor = mydb.cursor()
    cursor.execute('''
             SELECT derived.plonum, avg(per)
             FROM(
                SELECT p.ploID as PLOID,p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as per
                FROM spms_registration_t r,
                    spms_evaluation_t e,
                    spms_student_t st,
                    spms_department_t d,
                    spms_assessment_t a,
                    spms_co_t c,
                    spms_plo_t p
                WHERE r.student_id = st.studentID
                    and st.department_id = d.departmentID
                    and e.registration_id = r.registrationID
                    and a.assessmentID = e.assessment_id
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and st.department_id = '{}'
                    GROUP BY p.ploNum,r.student_id) derived
             GROUP BY derived.ploNum
                   '''.format(dept))
    row = cursor.fetchall()
    cursor.close()
    row.sort(key=len)
    return row


def getProgramWisePLO(program):
    cursor = mydb.cursor()
    cursor.execute('''
             SELECT derived.plonum, avg(per)
             FROM(
                SELECT p.ploID as PLOID, p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as per
                FROM spms_registration_t r,
                    spms_evaluation_t e,
                    spms_student_t st,
                    spms_program_t p,
                    spms_assessment_t a,
                    spms_co_t c,
                    spms_plo_t p
                WHERE r.student_id = st.studentID
                    and st.program_id = p.programID
                    and e.registration_id = r.registrationID
                    and a.assessmentID = e.assessment_id
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and st.program_id = '{}'
                    GROUP BY p.ploID,r.student_id) derived
             GROUP BY derived.PLOID
                   '''.format(program))
    row = cursor.fetchall()
    cursor.close()
    return row


# Enrollment
def getSchoolWiseEnrolledStudents(school, semesters):
    cursor = mydb.cursor()

    if len(semesters) == 1:
        cursor.execute('''
            SELECT count( distinct st.studentID)
            FROM spms_school_t s,
                spms_department_t d,
                spms_student_t st,
                spms_registration_t r
            WHERE r.student_id = st.studentID
                and st.department_id = d.departmentID
                and d.school_id = s.schoolID
                 and s.schoolID = '{}'
                and r.semester = '{}'
            '''.format(school, semesters[0]))
        row = cursor.fetchall()
    else:
        cursor.execute('''
                   SELECT count( distinct st.studentID)
                   FROM spms_school_t s,
                       spms_department_t d,
                       spms_student_t st,
                       spms_registration_t r
                   WHERE r.student_id = st.studentID
                       and st.department_id = d.departmentID
                       and d.school_id = s.schoolID
                        and s.schoolID = '{}'
                       and r.semester in {}
                   '''.format(school, str(tuple(semesters))))
        row = cursor.fetchall()
        cursor.close()
    return row[0][0]


def getDeptWiseEnrolledStudents(dept, semesters):
    cursor = mydb.cursor()
    if (len(semesters) == 1):
        cursor.execute('''
            SELECT count(distinct st.studentID)
            FROM spms_department_t d,
                spms_student_t st,
                spms_registration_t r
            WHERE r.student_id = st.studentID
                and st.department_id = '{}'
                and r.semester = '{}'
            '''.format(dept, semesters[0]))
        row = cursor.fetchall()
    else:
        cursor.execute('''
                    SELECT count(distinct st.studentID)
                    FROM spms_department_t d,
                        spms_student_t st,
                        spms_registration_t r
                    WHERE r.student_id = st.studentID
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
            SELECT count( distinct st.studentID)
            FROM spms_program_t p,
                spms_student_t st,
                spms_registration_t r
            WHERE r.student_id = st.studentID
                and st.program_id = p.programID
                and st.program_id = '{}'
                and r.semester = '{}'
            '''.format(program, semesters[0]))
        row = cursor.fetchall()

    else:
        cursor.execute('''
                   SELECT count( distinct st.studentID)
                   FROM spms_program_t p,
                       spms_student_t st,
                       spms_registration_t r
                   WHERE r.student_id = st.studentID
                       and st.program_id = p.programID
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
                    FROM (SELECT r.student_id as StudentID, 100*sum(e.obtainedMarks)/sum(a.totalMarks) as percourse
                        FROM spms_registration_t r,
                            spms_evaluation_t e,
                            spms_assessment_t a,
                            spms_co_t c,
                            spms_plo_t p,
                            spms_program_t pr
                        WHERE r.registrationID = e.registration_id
                            and e.assessment_id = a.assessmentID
                            and a.co_id = c.coID
                            and c.plo_id = p.ploID
                            and p.program_id = pr.programID
                            and pr.programID='{}'
                            and p.ploNum = '{}'
                        GROUP BY r.student_id,c.coID) per
                    GROUP BY per.StudentID) avgTable
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
                SELECT StudentID, AVG(percourse) as actual
                FROM(
                           SELECT r.student_id as StudentID, 100*sum(e.obtainedMarks)/sum(a.totalMarks) as percourse
                               FROM spms_registration_t r,
                                   spms_evaluation_t e,
                                   spms_assessment_t a,
                                   spms_co_t c,
                                   spms_plo_t p,
                                   spms_program_t pr
                               WHERE r.registrationID = e.registration_id
                                   and e.assessment_id = a.assessmentID
                                   and a.co_id = c.coID
                                   and c.plo_id = p.ploID
                                   and p.program_id = pr.programID
                                   and pr.programID='{}'
                                   and p.ploNum ='{}'
                               GROUP BY r.student_id,r.registrationID) d1
                           GROUP BY StudentID)d2
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
              SELECT ploNum,COUNT(Marks)
              FROM(
                    SELECT ploNum, StudentID, avg(coursemarks) as Marks
                    FROM(
                          SELECT p.ploNum as ploNum, r.student_id as StudentID,c.course_id, 
                                100*(sum(e.obtainedMarks)/sum(a.totalMarks)) as coursemarks
                          FROM spms_student_t st,
                              spms_registration_t r,
                              spms_department_t d,
                              spms_evaluation_t e,
                              spms_assessment_t a,
                              spms_co_t c,
                              spms_plo_t p
                          WHERE st.studentID = r.student_id
                              and e.registration_id = r.registrationID
                              and a.assessmentID = e.assessment_id
                              and a.co_id = c.coID
                              and c.plo_id = p.ploID
                              and st.department_id = d.departmentID
                              and d.departmentID = '{}'
                          GROUP BY p.ploNum, r.student_id,c.course_id) derived1
                      GROUP BY  ploNum,StudentID) derived2
                    GROUP BY ploNum
          '''.format(dept))

    row1 = cursor.fetchall()
    cursor.close()
    row1.sort(key=lambda t: len(t[0]))

    cursor.execute('''
                  SELECT ploNum,COUNT(Marks)
                  FROM(
                        SELECT ploNum, StudentID, avg(coursemarks) as Marks
                        FROM(
                              SELECT p.ploNum as ploNum, r.student_id as StudentID,c.course_id, 
                                    100*(sum(e.obtainedMarks)/sum(a.totalMarks)) as coursemarks
                              FROM spms_student_t st,
                                  spms_registration_t r,
                                  spms_department_t d,
                                  spms_evaluation_t e,
                                  spms_assessment_t a,
                                  spms_co_t c,
                                  spms_plo_t p
                              WHERE st.studentID = r.student_id
                                  and e.registration_id = r.registrationID
                                  and a.assessmentID = e.assessment_id
                                  and a.co_id = c.coID
                                  and c.plo_id = p.ploID
                                  and st.department_id = d.departmentID
                                  and d.departmentID = '{}'
                              GROUP BY p.ploNum, r.student_id,c.course_id) derived1
                          GROUP BY  ploNum,StudentID
                          HAVING avg(coursemarks)>=40) derived2
                        GROUP BY ploNum
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
              SELECT ploNum,COUNT(Marks)
              FROM(
                    SELECT ploNum, StudentID, avg(coursemarks) as Marks
                    FROM(
                          SELECT p.ploNum as ploNum, r.student_id as StudentID,c.course_id, 
                                100*(sum(e.obtainedMarks)/sum(a.totalMarks)) as coursemarks
                          FROM spms_student_t st,
                              spms_registration_t r,
                              spms_department_t d,
                              spms_school_t s,
                              spms_evaluation_t e,
                              spms_assessment_t a,
                              spms_co_t c,
                              spms_plo_t p
                          WHERE st.studentID = r.student_id
                              and e.registration_id = r.registrationID
                              and a.assessmentID = e.assessment_id
                              and a.co_id = c.coID
                              and c.plo_id = p.ploID
                              and st.department_id = d.departmentID
                              and d.school_id = s.schoolID
                              and s.schoolID = '{}'
                          GROUP BY p.ploNum, r.student_id,c.course_id) derived1
                      GROUP BY  ploNum,StudentID) derived2
                    GROUP BY ploNum
          '''.format(school))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))
    cursor.close()
    cursor.execute('''
                  SELECT ploNum,COUNT(Marks)
                  FROM(
                        SELECT ploNum, StudentID, avg(coursemarks) as Marks
                        FROM(
                              SELECT p.ploNum as ploNum, r.student_id as StudentID,c.course_id, 
                                    100*(sum(e.obtainedMarks)/sum(a.totalMarks)) as coursemarks
                              FROM spms_student_t st,
                                  spms_registration_t r,
                                  spms_department_t d,
                                  spms_school_t s,
                                  spms_evaluation_t e,
                                  spms_assessment_t a,
                                  spms_co_t c,
                                  spms_plo_t p
                              WHERE st.studentID = r.student_id
                                  and e.registration_id = r.registrationID
                                  and a.assessmentID = e.assessment_id
                                  and a.co_id = c.coID
                                  and c.plo_id = p.ploID
                                  and st.department_id = d.departmentID
                                  and d.school_id = s.schoolID
                                  and s.schoolID = '{}'
                              GROUP BY p.ploNum, r.student_id,c.course_id) derived1
                          GROUP BY  ploNum,StudentID
                          HAVING avg(coursemarks)>=40) derived2
                        GROUP BY ploNum
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
        SELECT ploNum,COUNT(*)
        FROM(
            SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
            FROM spms_student_t st,
                spms_registration_t r,
                spms_department_t d,
                spms_school_t s,
                spms_evaluation_t e,
                spms_assessment_t a,
                spms_co_t c,
                spms_plo_t p
            WHERE st.studentID = r.student_id
                and e.registration_id = r.registrationID
                and a.assessmentID = e.assessment_id
                and a.co_id = c.coID
                and c.plo_id = p.ploID
                and st.department_id = d.departmentID
                and d.school_id = s.schoolID
                and s.schoolID = '{}'
                and r.semester = '{}'
            GROUP BY p.ploNum, c.course_id, r.student_id) derived
        GROUP BY  derived.ploNum
    '''.format(school, semester))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))
    cursor.close()
    cursor.execute('''
            SELECT ploNum,COUNT(*)
            FROM(
                SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
                FROM spms_student_t st,
                    spms_registration_t r,
                    spms_department_t d,
                    spms_school_t s,
                    spms_evaluation_t e,
                    spms_assessment_t a,
                    spms_co_t c,
                    spms_plo_t p
                WHERE st.studentID = r.student_id
                    and e.registration_id = r.registrationID
                    and a.assessmentID = e.assessment_id
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and st.department_id = d.departmentID
                    and d.school_id = s.schoolID
                    and s.schoolID = '{}'
                    and r.semester = '{}'
                GROUP BY p.ploNum, c.course_id, r.student_id
                HAVING  100*(sum(e.obtainedMarks)/sum(a.totalMarks))>=40) derived
            GROUP BY  derived.ploNum
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
        SELECT ploNum,COUNT(*)
        FROM(
            SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
            FROM spms_student_t st,
                spms_registration_t r,
                spms_department_t d,
                spms_evaluation_t e,
                spms_assessment_t a,
                spms_co_t c,
                spms_plo_t p
            WHERE st.studentID = r.student_id
                and e.registration_id = r.registrationID
                and a.assessmentID = e.assessment_id
                and a.co_id = c.coID
                and c.plo_id = p.ploID
                and st.department_id = d.departmentID
                and d.departmentID = '{}'
                and r.semester = '{}'
            GROUP BY p.ploNum, c.course_id, r.student_id) derived
        GROUP BY  derived.ploNum
    '''.format(dept, semester))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))
    cursor.close()
    cursor.execute('''
            SELECT ploNum,COUNT(*)
            FROM(
                SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
                FROM spms_student_t st,
                    spms_registration_t r,
                    spms_department_t d,
                    spms_evaluation_t e,
                    spms_assessment_t a,
                    spms_co_t c,
                    spms_plo_t p
                WHERE st.studentID = r.student_id
                    and e.registration_id = r.registrationID
                    and a.assessmentID = e.assessment_id
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and st.department_id = d.departmentID
                    and d.departmentID = '{}'
                    and r.semester = '{}'
                GROUP BY p.ploNum, c.course_id, r.student_id
                HAVING  100*(sum(e.obtainedMarks)/sum(a.totalMarks))>=40) derived
            GROUP BY  derived.ploNum
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
        SELECT ploNum,COUNT(*)
        FROM(
            SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
            FROM spms_student_t st,
                spms_registration_t r,
                spms_program_t pr,
                spms_evaluation_t e,
                spms_assessment_t a,
                spms_co_t c,
                spms_plo_t p
            WHERE st.studentID = r.student_id
                and e.registration_id = r.registrationID
                and a.assessmentID = e.assessment_id
                and a.co_id = c.coID
                and c.plo_id = p.ploID
                and st.program_id = pr.programID
                and pr.programID = '{}'
                and r.semester = '{}'
            GROUP BY p.ploNum, c.course_id, r.student_id) derived
        GROUP BY  derived.ploNum
    '''.format(program, semester))

    row1 = cursor.fetchall()
    row1.sort(key=lambda t: len(t[0]))
    cursor.close()
    cursor.execute('''
            SELECT ploNum,COUNT(*)
            FROM(
                SELECT p.ploNum as ploNum, c.course_id, r.student_id, 100*(sum(e.obtainedMarks)/sum(a.totalMarks))
                FROM spms_student_t st,
                    spms_registration_t r,
                    spms_program_t pr,
                    spms_evaluation_t e,
                    spms_assessment_t a,
                    spms_co_t c,
                    spms_plo_t p
                WHERE st.studentID = r.student_id
                    and e.registration_id = r.registrationID
                    and a.assessmentID = e.assessment_id
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and st.program_id = pr.programID
                    and pr.programID = '{}'
                    and r.semester = '{}'
                GROUP BY p.ploID, c.course_id, r.student_id
                HAVING  100*(sum(e.obtainedMarks)/sum(a.totalMarks))>=40) derived
            GROUP BY  derived.ploNum
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
        SELECT ploNum, COUNT(marks)
        FROM(
            SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
            FROM spms_registration_t r,
                spms_evaluation_t e,
                spms_assessment_t a,
                spms_co_t c,
                spms_plo_t p
            WHERE r.registrationID = e.registration_id
                and e.assessment_id = a.assessmentID
                and a.co_id = c.coID
                and c.plo_id = p.ploID
                and c.course_id = '{}'
                and r.semester ='{}'
            GROUP BY p.ploNum,r.student_id) derived1
        GROUP BY ploNum
    '''.format(course, semester))

    temp1 = cursor.fetchall()
    cursor.close()
    temp1.sort(key=lambda t: len(t[0]))

    expected = temp1[0][1]
    cursor.execute('''
           SELECT ploNum, COUNT(marks)
           FROM(
               SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
               FROM spms_registration_t r,
                   spms_evaluation_t e,
                   spms_assessment_t a,
                   spms_co_t c,
                   spms_plo_t p
               WHERE r.registrationID = e.registration_id
                   and e.assessment_id = a.assessmentID
                   and a.co_id = c.coID
                   and c.plo_id = p.ploID
                   and c.course_id = '{}'
                   and r.semester ='{}'
               GROUP BY p.ploNum,r.student_id
               HAVING 100*sum(e.obtainedMarks)/sum(a.totalMarks)>=40) derived1
           GROUP BY ploNum
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
            SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
            FROM spms_registration_t r,
                spms_evaluation_t e,
                spms_assessment_t a,
                spms_co_t c,
                spms_plo_t p
            WHERE r.registrationID = e.registration_id
                and e.assessment_id = a.assessmentID
                and a.co_id = c.coID
                and c.plo_id = p.ploID
                and r.student_id='{}'
                and r.semester ='{}'
            GROUP BY p.ploNum,c.course_id) derived1
    '''.format(student, semester))

    expected = cursor.fetchall()
    cursor.close()
    cursor.execute('''
           SELECT COUNT(marks)
           FROM(
               SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
               FROM spms_registration_t r,
                   spms_evaluation_t e,
                   spms_assessment_t a,
                   spms_co_t c,
                   spms_plo_t p
               WHERE r.registrationID = e.registration_id
                   and e.assessment_id = a.assessmentID
                   and a.co_id = c.coID
                   and c.plo_id = p.ploID
                   and r.student_id = '{}'
                   and r.semester ='{}'
               GROUP BY p.ploNum,c.course_id
               HAVING 100*sum(e.obtainedMarks)/sum(a.totalMarks)>=40) derived1
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
               SELECT coNum, ploNum, COUNT(marks)
               FROM(
                       SELECT c.coNum as coNum,p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                       FROM spms_registration_t r,
                           spms_evaluation_t e,
                           spms_assessment_t a, 
                           spms_co_t c,
                           spms_plo_t p
                       WHERE r.registrationID = e.registration_id
                           and e.assessment_id = a.assessmentID
                           and a.co_id = c.coID
                           and c.plo_id = p.ploID
                            and c.course_id = '{}'
                       GROUP BY r.student_id,c.course_id,c.coID, p.ploID
                       )derived
               WHERE marks>=40
               GROUP BY coNum,ploNum
               '''.format(course))
    row = cursor.fetchall()
    cursor.close()
    if row is None:
        row = []

    cursor = mydb.cursor()
    cursor.execute('''
               SELECT coNum, ploNum, COUNT(marks)
               FROM(
                       SELECT r.student_id as StudentID,c.course_id as coID,c.coNum as coNum,
                       p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                       FROM spms_registration_t r,
                           spms_evaluation_t e,
                           spms_assessment_t a, 
                           spms_co_t c,
                           spms_plo_t p
                       WHERE r.registrationID = e.registration_id
                           and e.assessment_id = a.assessmentID
                           and a.co_id = c.coID
                           and c.plo_id = p.ploID
                            and c.course_id = '{}'
                       GROUP BY r.student_id,c.course_id,c.coID, p.ploID
                       )derived
                GROUP BY coID,coNum,ploNum
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
            SELECT c.coNum as coNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
            FROM spms_student_t st, 
                spms_registration_t r,
                spms_evaluation_t e,
                spms_assessment_t a, 
                spms_co_t c
            WHERE st.studentID = r.student_id
                and r.registrationID = e.registration_id
                and e.assessment_id = a.assessmentID
                and a.co_id = c.coID
                and st.program_id = '{}'
            GROUP BY c.coNum,r.student_id) derived
        GROUP BY coNum
    '''.format(program))

    row1 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT coNum, COUNT(marks)
            FROM(
                SELECT c.coNum as coNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                FROM spms_student_t st, 
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_assessment_t a, 
                    spms_co_t c
                WHERE st.studentID = r.student_id
                    and r.registrationID = e.registration_id
                    and e.assessment_id = a.assessmentID
                    and a.co_id = c.coID
                    and st.program_id = '{}'
                GROUP BY c.coNum,r.student_id) derived
            WHERE marks>=40
            GROUP BY coNum
        '''.format(program))

    row2 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT ploNum, COUNT(marks)
            FROM(
                SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                FROM spms_student_t st, 
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_assessment_t a, 
                    spms_co_t c,
                    spms_plo_t p
                WHERE st.studentID = r.student_id
                    and r.registrationID = e.registration_id
                    and e.assessment_id = a.assessmentID
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and st.program_id = '{}'
                GROUP BY p.ploNum,r.student_id) derived
            GROUP BY ploNum
        '''.format(program))

    row3 = cursor.fetchall()
    cursor.close()
    row3.sort(key=lambda t: len(t[0]))

    cursor.execute('''
                SELECT ploNum, COUNT(marks)
                FROM(
                    SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                    FROM spms_student_t st, 
                        spms_registration_t r,
                        spms_evaluation_t e,
                        spms_assessment_t a, 
                        spms_co_t c,
                        spms_plo_t p
                    WHERE st.studentID = r.student_id
                        and r.registrationID = e.registration_id
                        and e.assessment_id = a.assessmentID
                        and a.co_id = c.coID
                        and c.plo_id = p.ploID
                        and st.program_id = '{}'
                    GROUP BY p.ploNum,r.student_id) derived
                WHERE marks>=40
                GROUP BY ploNum
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
            SELECT c.coNum as coNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
            FROM spms_student_t st, 
                spms_registration_t r,
                spms_evaluation_t e,
                spms_assessment_t a, 
                spms_co_t c
            WHERE st.studentID = r.student_id
                and r.registrationID = e.registration_id
                and e.assessment_id = a.assessmentID
                and a.co_id = c.coID
                and st.department_id = '{}'
            GROUP BY c.coNum,r.student_id) derived
        GROUP BY coNum
    '''.format(dept))

    row1 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT coNum, COUNT(marks)
            FROM(
                SELECT c.coNum as coNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                FROM spms_student_t st, 
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_assessment_t a, 
                    spms_co_t c
                WHERE st.studentID = r.student_id
                    and r.registrationID = e.registration_id
                    and e.assessment_id = a.assessmentID
                    and a.co_id = c.coID
                    and st.department_id = '{}'
                GROUP BY c.coNum,r.student_id) derived
            WHERE marks>=40
            GROUP BY coNum
        '''.format(dept))

    row2 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT ploNum, COUNT(marks)
            FROM(
                SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                FROM spms_student_t st, 
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_assessment_t a, 
                    spms_co_t c,
                    spms_plo_t p
                WHERE st.studentID = r.student_id
                    and r.registrationID = e.registration_id
                    and e.assessment_id = a.assessmentID
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and st.department_id = '{}'
                GROUP BY p.ploNum,r.student_id) derived
            GROUP BY ploNum
        '''.format(dept))

    row3 = cursor.fetchall()
    cursor.close()
    row3.sort(key=lambda t: len(t[0]))

    cursor.execute('''
                SELECT ploNum, COUNT(marks)
                FROM(
                    SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                    FROM spms_student_t st, 
                        spms_registration_t r,
                        spms_evaluation_t e,
                        spms_assessment_t a, 
                        spms_co_t c,
                        spms_plo_t p
                    WHERE st.studentID = r.student_id
                        and r.registrationID = e.registration_id
                        and e.assessment_id = a.assessmentID
                        and a.co_id = c.coID
                        and c.plo_id = p.ploID
                        and st.department_id = '{}'
                    GROUP BY p.ploNum,r.student_id) derived
                WHERE marks>=40
                GROUP BY ploNum
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
            SELECT c.coNum as coNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
            FROM spms_student_t st, 
                spms_department_t d,
                spms_school_t s,
                spms_registration_t r,
                spms_evaluation_t e,
                spms_assessment_t a, 
                spms_co_t c
            WHERE st.studentID = r.student_id
                and st.department_id = d.departmentID
                and d.school_id = s.schoolID
                and r.registrationID = e.registration_id
                and e.assessment_id = a.assessmentID
                and a.co_id = c.coID
                and s.schoolID = '{}'
            GROUP BY c.coNum,r.student_id) derived
        GROUP BY coNum
    '''.format(school))

    row1 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT coNum, COUNT(marks)
            FROM(
                SELECT c.coNum as coNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                FROM spms_student_t st, 
                    spms_department_t d,
                    spms_school_t s,
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_assessment_t a, 
                    spms_co_t c
                WHERE st.studentID = r.student_id
                    and st.department_id = d.departmentID
                    and d.school_id = s.schoolID
                    and r.registrationID = e.registration_id
                    and e.assessment_id = a.assessmentID
                    and a.co_id = c.coID
                    and s.schoolID = '{}'
                    GROUP BY c.coNum,r.student_id) derived
            WHERE marks>=40
            GROUP BY coNum
        '''.format(school))

    row2 = cursor.fetchall()
    cursor.close()
    cursor.execute('''
            SELECT ploNum, COUNT(marks)
            FROM(
                SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                FROM spms_student_t st, 
                    spms_department_t d,
                    spms_school_t s,
                    spms_registration_t r,
                    spms_evaluation_t e,
                    spms_assessment_t a, 
                    spms_co_t c,
                    spms_plo_t p
                WHERE st.studentID = r.student_id
                    and st.department_id = d.departmentID
                    and d.school_id = s.schoolID
                    and r.registrationID = e.registration_id
                    and e.assessment_id = a.assessmentID
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and s.schoolID = '{}'
                    GROUP BY p.ploNum,r.student_id) derived
            GROUP BY ploNum
        '''.format(school))

    row3 = cursor.fetchall()
    cursor.close()
    row3.sort(key=lambda t: len(t[0]))

    cursor.execute('''
                SELECT ploNum, COUNT(marks)
                FROM(
                    SELECT p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                    FROM spms_student_t st, 
                        spms_department_t d,
                        spms_school_t s,
                        spms_registration_t r,
                        spms_evaluation_t e,
                        spms_assessment_t a, 
                        spms_co_t c,
                        spms_plo_t p
                    WHERE st.studentID = r.student_id
                        and st.department_id = d.departmentID
                        and d.school_id = s.schoolID
                        and r.registrationID = e.registration_id
                        and e.assessment_id = a.assessmentID
                        and a.co_id = c.coID
                        and c.plo_id = p.ploID
                        and s.schoolID = '{}'
                    GROUP BY p.ploNum,r.student_id) derived
                WHERE marks>=40
                GROUP BY ploNum
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

# def getUserDept():
#     userid=
#     if(getGroup(userid)=="faculty"):
#         table="spms_faculty_t"
#     elif(getGroup(userid)=="student"):
#         table="spms_student_t"
#     cursor=mydb.cursor()
#     cursor.execute('''
#     SELECT department
#     FROM '''
#     )
