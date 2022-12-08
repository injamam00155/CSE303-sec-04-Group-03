SELECT f.first_name,f.last_name,f.email, course_description, requied_textbook, cource_policy
                FROM spms.spms_section_t as s,
                spms.spms_course_outline_t as c,
                spms.spms_faculty_t as f
                WHERE c.section_id=s.section_id
                and f.faculty_id=s.faculty_id
                and s.section_num='{}'
                and s.semester='{}'
                and s.course_id='{}'