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
        SELECT DISTINCT c.courseid, cr.dept, cr.coursenum, c.area, c.title, c.descrip, c.prereqs, 
        p.profname
            FROM courses c
            JOIN crosslistings cr ON c.courseid = cr.courseid 
            JOIN coursesprofs cp ON c.courseid = cp.courseid
            JOIN profs p ON cp.profid = p.profid
            WHERE c.courseid = ?
    """
    
    cursor.execute(class_query, [classid])
    class_row = cursor.fetchone()
    courseid = class_row[6]
    
    cursor.execute(course_query, [courseid])
    course_row = cursor.fetchone()
    
    classDetails = f"""Class Id: {class_row[0]}
Days: {class_row[1]}
Start time: {class_row[2]}
End time: {class_row[3]}
Building: {class_row[4]}
Room: {class_row[5]}
"""

    courseDetails = f"""Course Id: {course_row[0]}
Dept and Number: {course_row[1]} {course_row[2]}
Area: {course_row[3]}
Title: {course_row[4]}
Description: {course_row[5]}
Prerequisites: {course_row[6]}
Professor: {course_row[7]}
"""
    wrappedClassDetails = textwrap.fill(classDetails, width=72, break_long_words=False, replace_whitespace=False)
    wrappedCourseDetails = textwrap.fill(courseDetails, width=72, break_long_words=False, replace_whitespace=False)

    print('-------------')
    print('Class Details')
    print('-------------')
    print(wrappedClassDetails)
    
    print('-------------')
    print('Course Details')
    print('-------------')
    print(wrappedCourseDetails)
    
#-----------------------------------------------------------------------  
def main():
    DATABASE_URL = 'file:reg.sqlite?mode=ro'
    
    parser = argparse.ArgumentParser(description = 'Registrar application: show details about a class')
    parser.add_argument('classid', help='the id of the class whose details should be shown')

    try:
        # Connects to the database and creates a curser connection 
        with sqlite3.connect(DATABASE_URL, isolation_level = None, uri = True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
        
                # Parses the stdin arguments
                args = parser.parse_args()
                
                # Calls the displayClassInfo function 
                displayClassInfo(cursor = cursor, classid=sys.argv[1])
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