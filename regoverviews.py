#-----------------------------------------------------------------------
# imports
import sqlite3
import textwrap

#-----------------------------------------------------------------------
def getAllClasses():
        sqliteConnection = sqlite3.connect('reg.sqlite')
        print("Connected to the database")
        curser = sqliteConnection.cursor()
        curser.execute("SELECT DISTINCT cl.classid, cr.dept, cr.coursenum, c.area, c.title FROM courses c JOIN crosslistings cr ON c.courseid = cr.courseid JOIN classes cl ON c.courseid = cl.courseid ORDER BY cr.dept, cr.coursenum;")
        ans = curser.fetchall()
        for row in ans:
            res = '%5s %4s %6s %4s %s' % (row[0], row[1], row[2], row[3], row[4])
            print(res)
        sqliteConnection.close()       

#-----------------------------------------------------------------------
def main():
    getAllClasses()
    
    
    
    
#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()