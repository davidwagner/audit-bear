#!/usr/bin/python
VOTE_EVENT = '0001510'
WORKER_VOTE_EVENT = '0001511'

import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from auditLog import AuditLog
import dateutil.parser as dp
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

path = sys.argv[1]
parsedLog = AuditLog(open(path, 'r'))
voteTimes = []
votesInMinute = {}

for line in parsedLog:
    if line[4] in (VOTE_EVENT, WORKER_VOTE_EVENT):
        time = dp.parse(line[3])
        time = time.replace(year = 2011, month = 11, day = 11, second = 0, microsecond = 0)
        # add it to the map..

        if time in votesInMinute:
            votesInMinute[time] += 1
        else:
            votesInMinute[time] = 1


mdateVotesInMinute = {}
for time in sorted(votesInMinute):
    print str(time.hour) + ":" + str(time.minute) + " ->" + str(votesInMinute[time])
    mdateVotesInMinute[time] = votesInMinute[time]

# we could pick a day (above, before vote population) or consolidate into some random day
# change date to mdate...
sortedDates = sorted(votesInMinute)

sortedCounts = []
for date in sortedDates:
    sortedCounts.append(votesInMinute[date])
    
print sortedDates

plt.plot_date(sortedDates, sortedCounts, '-', xdate=True, ydate=False) 
plt.show()

