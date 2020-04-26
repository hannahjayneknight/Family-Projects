#!/usr/bin/env python
# coding: latin-1
'''
A script that checks every minute if it is time for someone to do a chore. If it is, then
a message is sent to them.

The chores, the time they need to be done and the person doing them is stored in an array.
'''

import time
import datetime
from dateutil import parser
import numpy as np
from datetime import timedelta  
import csv
import requests
import sys
import os
import atexit
import signal

class lockdaemon:
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__( self, pidfile ):

        self.pidfile = pidfile

    def daemonize( self ):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
            # exit first parent
                sys.exit( 0 )
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit( 1 )

        self.stdin = '/dev/null'
        self.stdout = '/dev/null'
        self.stderr = '/dev/null'

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
            # exit from second parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # write pidfile
        atexit.register( self.delpid )
        pid = str( os.getpid() )
        with open( self.pidfile, 'w+' ) as f:
            f.write( "%s\n" % pid )

    def delpid( self ):
        os.remove( self.pidfile )

    def start( self ):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        pid = None
        if os.path.exists( self.pidfile ):
            with open( self.pidfile ) as f:
                pid = f.read().strip()

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write( message % self.pidfile )
            sys.exit( 1 )

        # Start the daemon
        self.daemonize()
        self.run()

    def stop( self ):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = open( self.pidfile,'r' )
            pid = int( pf.read().strip() )
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write( message % self.pidfile )
            return # not an error in a restart

        # Try killing the daemon process
        try:
            while True:
                os.kill( pid, signal.SIGTERM )
                time.sleep( 0.1 )
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print( "OS error: {0}".format( err ) )
                sys.exit(1)

    def restart( self ):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def sendmessage( self, number, message ):
        passwords = {}
        # opens the file with the passwords on
        with open('babble_passwords.txt', 'r') as f:
            # runs through each line and makes a dictionary where the key is the
            # name of the password and the value is the password itself
            for line in f:
                (key, val) = line.split()
                passwords[key] = val

        # Number, Message, Domain
        our_params = {'Number': number, 'Message': message, 'Domain': passwords['bvdomain']}

        response = requests.get(url = passwords['smsurl'], params = our_params, auth=(passwords['bvuser'], passwords['bvpass']) )
        print( response )
        print( response.text )
        return response



    def run( self ):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """

        peopledict = {}
        with open('mobile_numbers.csv') as mobile_numbers:
            # 
            reader = csv.DictReader(mobile_numbers)
            for row in reader:
                peopledict[ row[ "name" ] ] = row[ "number" ]

        # so you definitely get the first chore
        last_check = datetime.datetime.now() - timedelta( minutes = 5 )  
        while True:
            # imports the timetable
            # NB: converts each element in the table to a string
            timetable = np.genfromtxt('timetable.csv', skip_header=1, delimiter=',', dtype=(str))

            # loops through each row 
            for timetablerow in timetable:
                # checks if it is the correct weekday
                if timetablerow [ 0 ] == str(datetime.datetime.today().weekday()):
                    currenttime = datetime.datetime.now()
                    # checks if the time is between five mins ago and the time now
                    if last_check < parser.parse( timetablerow[ 1 ] ) < currenttime:
                        # prints statement
                        print(timetablerow[3] + ', it is your turn to ' + timetablerow[2])
                        print('Sending sms to ' + peopledict[ str( timetablerow[3] ) ] )
                        self.sendmessage( peopledict[ str( timetablerow[3] ) ],  timetablerow[3] + ', it is your turn to do ' + timetablerow[2] )
                        
            last_check = datetime.datetime.now()
            time.sleep(300)



"""
## createProcess

Function to start us properly. Our main entry point.
"""
def createProcess():
    daemon = lockdaemon( '/tmp/lockserver.pid' )
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
                daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'debug' == sys.argv[1]:
            daemon.run()
        else:
            print( "Unknown command: " + sys.argv[1] )
            sys.exit(2)

            sys.exit(0)
    else:
        daemon.run()

createProcess()
