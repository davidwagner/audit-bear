#!/usr/bin/python
import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from auditLog import AuditLog

OPENED_EVENT = '0001672'
CLOSED_EVENT = '0001673'

path = sys.argv[1]
parsedLog = AuditLog(open(path, 'r'))
machineStatus = {}
for line in parsedLog:
    if not line[0] in machineStatus:
        machineStatus[line[0]] = [False, False]
    if line[4] == OPENED_EVENT:
        if line[0] in machineStatus:
            machineStatus[line[0]][0] = True
        else:
            machineStatus[line[0]] = [True, False]
    elif line[4] == CLOSED_EVENT:
        if line[0] in machineStatus:
            machineStatus[line[0]][1] = True
        else:
            machineStatus[line[0]] = [False, True]

for machine in sorted(machineStatus):
    openedStatus = "opened" if machineStatus[machine][0] else "not opened."
    closedStatus = "closed" if machineStatus[machine][0] else "not closed."
    print "Machine " + machine + " was " + openedStatus + " and " + closedStatus

