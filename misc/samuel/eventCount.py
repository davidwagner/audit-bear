#!/usr/bin/python
import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from auditLog import AuditLog
path = sys.argv[1]
parsedLog = AuditLog(open(path, 'r'))
eventMap = {}
strEvent = {}
for line in parsedLog:
    if line[4] in eventMap:
        eventMap[line[4]] += 1
    else:
        eventMap[line[4]] = 1
        strEvent[line[4]] = line[5]

for k in sorted(eventMap):
    print "Event number " + str(k) + ' - "' + strEvent[k] + '" appeared ' + str(eventMap[k]) + " times."

    
