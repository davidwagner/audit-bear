#!/usr/bin/python
import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from auditLog import AuditLog

VOTE_EVENT = '0001510'
WORKER_VOTE_EVENT = '0001511'
path = sys.argv[1]
parsedLog = AuditLog(open(path, 'r'))
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

# Graph it
#import matplotlib.pyplot as plt
#x = []
#for machine in sorted(machineVotes):
#    x.extend([int(machine)] * machineVotes[machine])

# you might want to set bins smaller...
#nbList = []
#for machine in machineVotes:
#    nbList.append(int(machine))

#nb = max(nbList) - min(nbList)
#n, bins, patches = plt.hist(x, bins=nb)
#plt.xlabel('Serial Number')
#plt.ylabel('Votes')
#plt.title('Votes per machine')
#plt.show()

