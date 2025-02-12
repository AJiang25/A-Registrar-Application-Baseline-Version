#-----------------------------------------------------------------------
# imports
import sys
import sqlite3
import textwrap
import argparse
import contextlib

#-----------------------------------------------------------------------

def displayClassInfo(cursor, classid = None): 
    class_query = """
        SELECT classid, days, starttime, endtime, bldg, roomnum, courseid
        FROM classes 
        WHERE classid = ?
    """
    course_query = """
        SELECT DISTINCT c.courseid, c.area, c.title, c.descrip, c.prereqs
            FROM courses c
            WHERE c.courseid = ?
    """
    dept_query = """
        SELECT DISTINCT cr.dept, cr.coursenum
            FROM crosslistings cr
            WHERE cr.courseid = ?
            ORDER BY cr.dept ASC, cr.coursenum ASC
    """
    prof_query = """
        SELECT DISTINCT p.profname
            FROM courses c 
            JOIN coursesprofs cp ON c.courseid = cp.courseid
            JOIN profs p ON cp.profid = p.profid
            WHERE c.courseid = ?
            ORDER BY p.profname ASC
    """
    
    cursor.execute(class_query, [classid])
    class_row = cursor.fetchall()
    courseid = class_row[0][6]
    
    cursor.execute(course_query, [courseid])
    course_row = cursor.fetchone()
    
    cursor.execute(dept_query, [courseid])
    dept_row = cursor.fetchall()
    
    cursor.execute(prof_query, [courseid])
    prof_row = cursor.fetchall()
    
    print('-------------')
    print('Class Details')
    print('-------------')
    for row in class_row:
        print(f"Class Id: {row[0]}")
        print(f"Days: {row[1]}")
        print(f"Start time: {row[2]}")
        print(f"End time: {row[3]}")
        print(f"Building: {row[4]}")
        print(f"Room: {row[5]}")
    
    print('-------------')
    print('Course Details')
    print('-------------')
    
    print(f"Course Id: {course_row[0]}")
    for dept in dept_row: 
        print(f"Dept and Number: {dept[0]} {dept[1]}")
    print(f"Area: {course_row[1]}")
    
    title = f"Title: {course_row[2]}"
    wrappedTitle = textwrap.fill(title, width = 72, break_long_words=False, replace_whitespace=False, subsequent_indent=" "*3)
    print(wrappedTitle)
    
    description = f"Description: {course_row[3]}"
    wrappedDescription = textwrap.fill(description, width = 72, break_long_words=False, replace_whitespace=False, subsequent_indent=" "*3)
    print(wrappedDescription)
    
    prerequisites = f"Prerequisities: {course_row[4]}"
    wrappedPrerequisites = textwrap.fill(prerequisites, width = 72, break_long_words=False, replace_whitespace=False, subsequent_indent=" "*3)
    print(wrappedPrerequisites)

    for prof in prof_row: 
        print(f"Professor: {prof[0]}")
    
    
#     for row in class_row:
#         classDetails = f"""Class Id: {row[0]}
# Days: {row[1]}
# Start time: {row[2]}
# End time: {row[3]}
# Building: {row[4]}
# Room: {row[5]}
# """
#         wrappedClassDetails = textwrap.fill(classDetails, width = 72, break_long_words=False, replace_whitespace=False)

#         print(wrappedClassDetails)

#         course = f"""Course Id: {course_row[0]}"""
#         for dept in dept_row: 
#             f"""Dept and Number: {dept[1]} {dept[2]}"""
#         course1 = f""" 
#         Area: {course_row[1]}
#         Title: {course_row[2]}
#         Description: {course_row[3]}
#         Prerequisites: {course_row[4]}
#         """
        
        
        # for prof in prof_row: 
        #     f"""Professor: {prof[0]}"""
        
        # courseDetails = course + course1
            
 #       wrappedCourseDetails = textwrap.fill(courseDetails, width = 72, break_long_words=False, replace_whitespace=False)
        
 #       print(wrappedCourseDetails)
    
#-----------------------------------------------------------------------  
def main():
    DATABASE_URL = 'file:reg.sqlite?mode=ro'
    
    parser = argparse.ArgumentParser(description = 'Registrar application: show details about a class')
    parser.add_argument('classid', help='the id of the class whose details should be shown')

    try:
        # Connects to the database and creates a curser connection 
        with sqlite3.connect(DATABASE_URL, isolation_level = None, uri = True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                # parser.add_argument(type = int)
                # Parses the stdin arguments
                args = parser.parse_args()
                
                # args.classid.isnumeric():
                # classid doesn't exist
                
                # Calls the displayClassInfo function 
                displayClassInfo(cursor = cursor, classid=args.classid)
                sys.exit(0)

    except sqlite3.Error:
        print(f"{sys.argv[0]}: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{sys.argv[0]}: {str(e)}", file=sys.stderr) 
        sys.exit(2)
        

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()