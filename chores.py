'''
A script that checks every minute if it is time for someone to do a chore. If it is, then
a message is sent to them.

The chores, the time they need to be done and the person doing them is stored in an array.
'''

import datetime
import numpy as np

# imports the timetable
# converts each element in the table to a string
timetable = np.genfromtxt('/Users/hannahjayneknight/Desktop/git/personal/timetable.csv', skip_header=1, delimiter=', ', dtype=(str))

while True:

    # checks if the day is today

    # loops through the column with the weekday numbers
    for weekdays in timetable[:, 0]:
        if weekdays == str(datetime.datetime.today().weekday()):

            # continues to check if it is the correct time

            # loops through the column with all the times
            for times in timetable[:, 1]:
                # finds the time now
                time_now = list(str(datetime.datetime.now().time()))
                # writes the current time as a string
                time_now_string = str(time_now[0]) + str(time_now[1]) + str(time_now[2]) + str(time_now[3]) + str(time_now[4])
        
                # finds the row with the time now
                if time_now_string == str(times):
                    # saves the row number with the current time as a variable
                    row_number = times
                    # print '[name], it is your turn to [chore]'
                    print(timetable[row_number][3] + ', it is your turn to do ' + timetable[row_number][2])

'''
Given I used a "while True" loop, I omitted the following:
            # writes the current time +/- 1 minute as a string
            time_plus_one_string = time_now[0] + time_now[1] + time_now[2] + time_now[3] + str(int(time_now[4])+1)
            time_minus_one_string = time_now[0] + time_now[1] + time_now[2] + time_now[3] + str(int(time_now[4])-1)

            # finds the row with the time now or +/- 1 minute 
            if time_now_string == i or time_minus_one_string == i or time_plus_one_string == i:
'''
