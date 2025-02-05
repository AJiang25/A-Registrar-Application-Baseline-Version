#-----------------------------------------------------------------------
# imports
import sys
import sqlite3
import textwrap
import argparse

#-----------------------------------------------------------------------

def displayClassInfo(curser, classid = None): 
    query = """
            
        """
    curser.execute(query, classid)
    ans = curser.fetchall()


#-----------------------------------------------------------------------  
def main():
    parser = argparse.ArgumentParser(description = 'Registrar application: show details about a class')
    parser.add_argument('classid', help='the id of the class whose details should be shown')

    try:
        # Connects to the database and creates a curser connection 
        sqliteConnection = sqlite3.connect('reg.sqlite')
        curser = sqliteConnection.cursor()
        
        # Parses the stdin arguments
        args = parser.parse_args()
        
        # Calls the displayClassInfo function 
        displayClassInfo(curser = curser, classid = argsv[0])
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



#----------------