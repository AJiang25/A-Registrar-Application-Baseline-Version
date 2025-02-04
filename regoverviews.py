#-----------------------------------------------------------------------
# imports
import sys
import sqlite3
import textwrap
import argparse

#-----------------------------------------------------------------------
def displayClasses(dept = None, num = None, area = None, title = None):
        sqliteConnection = sqlite3.connect('reg.sqlite')
        curser = sqliteConnection.cursor()
        query = """
            SELECT DISTINCT cl.classid, cr.dept, cr.coursenum, c.area, c.title 
            FROM courses c 
            JOIN crosslistings cr ON c.courseid = cr.courseid 
            JOIN classes cl ON c.courseid = cl.courseid
        """

        conditions = []
        descriptors = []
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

        query += "WHERE " + " AND ".join(conditions)
        # The rows must sorted. The primary sort must be by dept in ascending order, 
        # the secondary sort must be by coursenum in ascending order, and tertiary sort 
        # must be by classid in ascending order.
        query += "ORDER BY cr.dept, cr.coursenum;"
        curser.execute(query, descriptors)
        ans = curser.fetchall()

        print('%5s %4s %6s %4s %s' % ("ClsId", "Dept", "CrsNum", "Area", "Title"))
        print('%5s %4s %6s %4s %s' % ("-----", "----", "------", "----", "-----"))

        # Within each row, each line must consist of no more than 72 characters, 
        # not including the newline character.
        # line = line.rstrip(’\n’)
        
        # Within each row, each line must end after a word, not within a word. 
        # That is, no newline characters may appear within words.
        for row in ans:
            res = '%5s %4s %6s %4s %s' % (row[0], row[1], row[2], row[3], row[4])
            print(textwrap.fill(res, subsequent_indent=" "*23))

        #  Normally your regoverviews.py must terminate with exit status 0. 
        # If it detects a database-related error, then it must terminate with exit status 1. 
        # If it detects erroneous command-line arguments, 
        # then it must terminate with exit status 2 — as is the default behavior of argparse.

        sqliteConnection.close()  
             

#-----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description = 'Registrar application: show overviews of classes')
    parser.add_argument('-d', type=str, metavar = 'dept', help ='show only those classes whose department contains dept')
    parser.add_argument('-n', type=str, metavar = 'num', help ='show only those classes whose course number contains num')
    parser.add_argument('-a', type=str, metavar = 'area', help ='show only those classes whose distrib area contains area')
    parser.add_argument('-t', type=str, metavar = 'title', help ='show only those classes whose course title contains title')
    args = parser.parse_args()

    displayClasses(dept = args.d, num = args.n, area = args.a, title = args.t)
    
#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()