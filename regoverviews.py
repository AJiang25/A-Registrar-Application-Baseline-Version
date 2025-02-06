#-----------------------------------------------------------------------
# imports
import sys
import sqlite3
import textwrap
import argparse
import contextlib

#-----------------------------------------------------------------------
def displayClasses(cursor, dept = None, num = None, area = None, title = None):   
        conditions = []
        descriptors = []
        query = """
            SELECT DISTINCT cl.classid, cr.dept, cr.coursenum, c.area, c.title 
            FROM courses c 
            JOIN crosslistings cr ON c.courseid = cr.courseid 
            JOIN classes cl ON c.courseid = cl.courseid
        """
        if dept: 
            conditions.append("cr.dept LIKE ? ESCAPE '\\'")
            descriptor = dept.lower().replace("%", r"\%").replace("_", r"\_")
            descriptors.append(f"%{descriptor}%")
        if num:
            conditions.append("cr.coursenum LIKE ? ESCAPE '\\'")
            descriptor = num.lower().replace("%", r"\%").replace("_", r"\_")
            descriptors.append(f"%{descriptor}%")
        if area:
            conditions.append("c.area LIKE ? ESCAPE '\\'")
            descriptor = area.lower().replace("%", r"\%").replace("_", r"\_")
            descriptors.append(f"%{descriptor}%")
        if title:
            conditions.append("c.title LIKE ? ESCAPE '\\'")
            descriptor = title.lower().replace("%", r"\%").replace("_", r"\_")
            descriptors.append(f"%{descriptor}%")
        if conditions:
            query += "WHERE " + " AND ".join(conditions)
            
        query += "ORDER BY cr.dept ASC, cr.coursenum ASC, cl.classid ASC;"
        cursor.execute(query, descriptors)
        ans = cursor.fetchall()

        print('%5s %4s %6s %4s %s' % ("ClsId", "Dept", "CrsNum", "Area", "Title"))
        print('%5s %4s %6s %4s %s' % ("-----", "----", "------", "----", "-----"))

        for row in ans:
            res = '%5s %4s %6s %4s %s' % (row[0], row[1], row[2], row[3], row[4])
            print(textwrap.fill(res, width = 72, break_long_words= False, subsequent_indent=" "*23))
        
#-----------------------------------------------------------------------
def main():

    parser = argparse.ArgumentParser(description = 'Registrar application: show overviews of classes')
    parser.add_argument('-d', type=str, metavar = 'dept', help ='show only those classes whose department contains dept')
    parser.add_argument('-n', type=str, metavar = 'num', help ='show only those classes whose course number contains num')
    parser.add_argument('-a', type=str, metavar = 'area', help ='show only those classes whose distrib area contains area')
    parser.add_argument('-t', type=str, metavar = 'title', help ='show only those classes whose course title contains title')
    
    try:
        # Connects to the database and creates a curser connection 
        with sqlite3.connect('reg.sqlite') as connection:
            with contextlib.closing(connection.cursor()) as cursor:
        
                # Parses the stdin arguments
                args = parser.parse_args()
                
                # Calls the displayClasses function 
                displayClasses(cursor = cursor, dept = args.d, num = args.n, area = args.a, title = args.t)
                sys.exit(0)
        
    # Normally your regoverviews.py must terminate with exit status 0. 
    # If it detects a database-related error, then it must terminate with exit status 1. 
    # If it detects erroneous command-line arguments, 
    # then it must terminate with exit status 2 — as is the default behavior of argparse.
    except sqlite3.Error:
        #ASK ABOUT THE PRINT STATEMENTS
        print(f"{sys.argv[0]}: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{sys.argv[0]}: {str(e)}", file=sys.stderr) 
        sys.exit(2)
#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()