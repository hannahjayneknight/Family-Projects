'''
A script that checks every minute if it is time for someone to do a chore. If it is, then 
a message is sent to them.

The chores, the time they need to be done and the person doing them is stored in an array.
'''

from io import StringIO
import numpy as np
import datetime

#imports the timetable
timetable = np.genfromtxt('/Users/hannahjayneknight/Desktop/git/personal/timetable.csv', skip_header=1, delimiter=', ', dtype=(str))


# checks if the day is today
for i in timetable[:,0]:
    if i == datetime.datetime.today().weekday():

        # continues to check if it is the correct time
        for i in timetable[:,1]:
            time_now = list(str(datetime.datetime.now().time()))
            time_now_string = time_now[0] + time_now[1] + time_now[2] + time_now[3] + time_now[4]
            
            time_plus_one_string = time_now[0] + time_now[1] + time_now[2] + time_now[3] + str(int(time_now[4])+1)
            time_minus_one_string = time_now[0] + time_now[1] + time_now[2] + time_now[3] + str(int(time_now[4])-1)
            
            if time_now_string == i or time_minus_one_string == i or time_plus_one_string == i:
                
                # print '[name], it is your turn to [chore]'
                print()

#for i in timetable[:,0]:
    #print(i)


