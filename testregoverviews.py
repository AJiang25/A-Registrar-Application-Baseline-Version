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

    #Normal Case Testing
    exec_command(program, '-d COS')
    exec_command(program, '-d COS -a qr -n 2 -t intro')


    exec_command(program, '')
    exec_command(program, '-n 333')
    exec_command(program, '-n b')
    exec_command(program, '-a Qr')
    exec_command(program, '-t intro')
    exec_command(program, '-t science')
    exec_command(program, '-t C_S')
    exec_command(program, '-t c%S')
    exec_command(program, '-d cos -n 3')
    exec_command(program, '-t "Independent Study"')
    exec_command(program, '-t "Independent Study "')
    exec_command(program, '-t "Independent Study  "')
    exec_command(program, '-t " Independent Study"')
    exec_command(program, '-t "  Independent Study"')
    exec_command(program, '-t=-c')

    
    # Corner Case Testing
    

    #Error Case Testing 
    exec_command(program, 'a qr')
    exec_command(program, '-A qr')
    exec_command(program, '"-a " qr')
    exec_command(program, '-a qr st')
    exec_command(program, '-a')
    exec_command(program, '-a qr -d')
    exec_command(program, '-a -d cos')
    exec_command(program, '-x')

    # Coverage Testing 
    exec_command(program, '-h')
    
    # Database Testing
    try: 
        shutil.copy('reg.sqlite', 'regbackup.sqlite')
        os.remove('reg.sqlite')
        exec_command(program, '-d ENG') 
        shutil.copy('regflawed.sqlite', 'reg.sqlite')
        exec_command(program, '-d ENG') 
        shutil.copy('regbackup.sqlite', 'reg.sqlite')
    except FileNotFoundError:
        print('Database file not found, skipping database error tests.', file=sys.stderr)


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
