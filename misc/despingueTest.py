#!/usr/bin/python
import despingue
import os, sys

cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from auditLog import AuditLog   #imports audit log class
from ballotImage import BallotImage  #imports ballot image class
import dateMod

path = sys.argv[1]
path2 = sys.argv[2]
path3 = sys.argv[3]

parsedLog = AuditLog(open(path, 'r'))
parsedBallotImage = BallotImage(open(path2, 'r'))


# first generate list of valid machines
dateModObject = dateMod.DateMod(parsedLog, open(path3, 'r'))
mmap = dateMod.timecheck(dateMod.timeopen(dateModObject.edata))
validMachines = mmap.keys()

finalMap = despingue.inferLines(parsedLog, parsedBallotImage, validMachines)
for pollingLocation in finalMap:
    for window in finalMap[pollingLocation]:
        print "Location " + pollingLocation + " busy in window " + str(window) + "? : " + str(finalMap[pollingLocation][window])

# finished!!!

