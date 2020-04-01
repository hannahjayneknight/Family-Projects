'''
A script that checks every minute if it is time for someone to do a chore. If it is, then
a message is sent to them.

The chores, the time they need to be done and the person doing them is stored in an array.
'''

import time
import datetime
from dateutil import parser
import numpy as np

# imports the timetable
# NB: converts each element in the table to a string
timetable = np.genfromtxt('/Users/hannahjayneknight/Desktop/git/personal/timetable.csv', skip_header=1, delimiter=',', dtype=(str))

while True:
    # saves the last time
    last_check = datetime.datetime.now()

    time.sleep(300)

    # checks if the day is today
    # loops through the column with the weekday numbers
    for weekdays in timetable[:, 0]:
        if weekdays == str(datetime.datetime.today().weekday()):

            # continues to check if it is the correct time

            # loops through the column with all the times
            for i in timetable[:, 1]:
                # checks if the time in the column is between the time of the last_check and now
                if last_check < parser.parse(i) < datetime.datetime.now() :
                    # saves the row number with the current time as a variable
                    row_number = i
                    # print '[name], it is your turn to [chore]'
                    print(timetable[row_number][3] + ', it is your turn to do ' + timetable[row_number][2])
