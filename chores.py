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


def sendmessage( number, message ):
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
                print(timetablerow[3] + ', it is your turn to do ' + timetablerow[2])
                print('Sending sms to ' + peopledict[ str( timetablerow[3] ) ] )
                sendmessage( peopledict[ str( timetablerow[3] ) ],  timetablerow[3] + ', it is your turn to do ' + timetablerow[2] )
                
    last_check = datetime.datetime.now()
    time.sleep(300)
