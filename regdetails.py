#-----------------------------------------------------------------------
# imports
import sys
import sqlite3
import textwrap
import argparse

#-----------------------------------------------------------------------

def displayClassInfo(cursor, classid = None): 
    class_query = """
        SELECT classid, days, starttime, endtime, bldg, roomnum, courseid
        FROM classes 
        WHERE classid = ?
    """
    cursor.execute(class_query, [classid])
    class_row = cursor.fetchone()
    
    course_query = """
        
    """
    cursor.execute(course_query, [classid])
    course_row = cursor.fetchone()
    
    # query = """
    #         SELECT DISTINCT cl.classid, cl.courseid, cl.days, cl.starttime, 
    #         cl.endtime, cl.endtime, cl.bldg, cl.roomnum, c.area, c.title, 
    #         c.descrip, c.prereqs, cr.dept, cr.coursenum, p.profname
    #         FROM classes cl
    #         JOIN crosslistings cr ON c.courseid = cr.courseid 
    #         JOIN courses c ON c.courseid = cl.courseid
    #         JOIN coursesprofs cp ON cr.courseid = cp.courseid
    #         JOIN profs p ON cp.profid = p.profid
    #         WHERE cl.classid = ?
    #     """
    # descriptor = f"{classid}"

    # #query += "ORDER BY cr.dept ASC, cr.coursenum ASC, cl.classid ASC;"
    # curser.execute(query, [descriptor])
    # ans = curser.fetchall()

    print('-------------')
    print('Class Details')
    print('-------------')
    classDetails = f"""Class Id: {class_row[0]}
Days: {class_row[1]}
Start time: {class_row[2]}
End time: {class_row[3]}
Building: {class_row[4]}
Room: {class_row[5]}"""
    print(classDetails)

    # labels = ["Class Id: ", "Days: ", "Start time: ", "End time: ", "Building: ", "Room: "]
    # for row in ans:
    #     res = (f"Class Id: {row[0]}")
    #     res+= (f"Days: %s" % row[1])
    #     res+= (f"Start time: %s" % row[2])
    #     res+= (f"End time: %s" % row[3])
    #     res+= (f"Building: %s" % row[4])
    #     res+= (f"Room: %s" % row[5])

        #res = f"Course information:{'\n'.join(ans[0])}"
        #res = '%5s %4s %6s %4s %s %s %s %s %s %s %s %s %s %s %s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])

    print('-------------')
    print('Course Details')
    print('-------------')
        
#-----------------------------------------------------------------------  
def main():
    parser = argparse.ArgumentParser(description = 'Registrar application: show details about a class')
    parser.add_argument('classid', help='the id of the class whose details should be shown')
    

    try:
        # Connects to the database and creates a curser connection 
        sqliteConnection = sqlite3.connect('reg.sqlite')
        cursor = sqliteConnection.cursor()
        
        # Parses the stdin arguments
        args = parser.parse_args()
        
        # Calls the displayClassInfo function 
        displayClassInfo(cursor = cursor, classid=sys.argv[1])
        sys.exit(0)

    except sqlite3.Error:
        #ASK ABOUT THE PRINT STATEMENTS
        print(f"{sys.argv[0]}: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{sys.argv[0]}: {str(e)}", file=sys.stderr) 
        sys.exit(2)
    finally: 
        if sqliteConnection:
            sqliteConnection.close() 

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()