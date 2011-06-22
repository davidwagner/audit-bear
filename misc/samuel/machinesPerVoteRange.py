#!/usr/bin/python
import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from auditLog import AuditLog
import math

VOTE_EVENT = '0001510'
WORKER_VOTE_EVENT = '0001511'

#parsedLog = parse(open('audit_log.txt', 'r'))
parsedLog = AuditLog(open(sys.argv[1], 'r'))
machineVotes = {}
totalVotes = 0
for line in parsedLog:
    if not line[0] in machineVotes:
        machineVotes[line[0]] = 0
    if line[4] in (VOTE_EVENT, WORKER_VOTE_EVENT):
        machineVotes[line[0]] += 1
        totalVotes += 1

for machine in sorted(machineVotes):
    print "Machine " + machine + " has " + str(machineVotes[machine]) + " votes."

print "Total votes", totalVotes
print "Number of machines", len(machineVotes)

# Graph it
# ask for vote stepping...
stepping = raw_input("Enter stepping number: ")

# calculate number of bins
x = machineVotes.values()
maxVotes = max(x)
m = math.ceil(maxVotes / int(stepping)) + 1
print "maxVotes is", maxVotes
print "M is ", m

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
# bins = either the number of bins (actual bins returned is bins+1)
# or the sequence giving the bins (see bins that hist returns... you'll get it
# n is the info for each of the bins... it gets calculated by what is in x
# and the bins
(n, bins, patches) = ax.hist(x, bins=m, range=(0, m*int(stepping)))
print 'n =',n
print 'bins =',bins
print 'patches =',patches
ax.set_xlabel('Ranges')
ax.set_xlim(0, m*int(stepping))
ax.set_ylabel('Number of Machines')
ax.set_title('#Machines vs Vote count ranges')
xaxis = ax.get_xaxis()
#xaxis.set_ticklabels(('1am', '2am', '3am', '4am', '5am'))


#ax.xticks([i for i in range(0, int((m)*int(stepping)) + 1, int(stepping))])
fig.savefig('test.png', dpi=150) # 150 corresponds to 1200x900

