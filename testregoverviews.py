#!/usr/bin/env python

#-----------------------------------------------------------------------
# testregoverviews.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import os
import sys

#-----------------------------------------------------------------------

MAX_LINE_LENGTH = 72
UNDERLINE = '-' * MAX_LINE_LENGTH

#-----------------------------------------------------------------------

def print_flush(message):
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def exec_command(program, args):

    print_flush(UNDERLINE)
    command = 'python ' + program + ' ' + args
    print_flush(command)
    exit_status = os.system(command)
    if os.name == 'nt':  # Running on MS Windows?
        print_flush('Exit status = ' + str(exit_status))
    else:
        print_flush('Exit status = ' + str(os.WEXITSTATUS(exit_status)))

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 2:
        print('usage: ' + sys.argv[0] + ' regprogram', file=sys.stderr)
        sys.exit(1)

    program = sys.argv[1]

    exec_command(program, '-d COS')
    exec_command(program, '-d COS -a qr -n 2 -t intro')
    
    # Corner Case Testing
    
    # Coverage Testing 
    
    # Database Testing
    # Execute the statement shutil.copy('reg.sqlite', 'regbackup.sqlite') 
    # to make a backup copy of reg.sqlite.
    # Execute the statement os.remove('reg.sqlite') to delete the reg.sqlite database. 
    # Subsequent test should fail because the database is missing.
    # Execute the statement shutil.copy('regflawed.sqlite', 'reg.sqlite') to copy some 
    # "flawed" database file to reg.sqlite. The flawed database might be empty, or corrupted. 
    # Subsequent tests should fail because the database indeed is flawed.
    # Execute the statementshutil.copy('regbackup.sqlite', 'reg.sqlite') to copy the original 
    # correct database back to reg.sqlite.
    # If you include such tests in your testregoverviews.py (or testregdetails.py) program, 
    # then make sure you submit your regflawed.sqlite file. Otherwise your testregoverviews.py 
    # (or testregdetails.py) program will fail when your grader runs it.

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
