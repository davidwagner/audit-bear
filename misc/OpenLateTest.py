#!/usr/bin/python
#test the functions of analysis_places_open_late2
import dateutil.parser
import datetime
import analysis_places_open_late2
import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from auditLog import AuditLog
from ballotImage import BallotImage
import dateMod

path = sys.argv[1]
path2 = sys.argv[2]
path3 = sys.argv[3]

parsedLog = AuditLog(open(path, "r"))
parsedBallotImage = BallotImage(open(path2, 'r'), AuditLog(open(path, 'r')), open(path3, 'r'))
dateModObject = dateMod.DateMod(parsedLog, open(path3, 'r'))
mmap = dateMod.timecheck(dateMod.timeopen(dateModObject.edata))
validMachines = mmap.keys()
mapOpenLateTime = analysis_places_open_late2.open_late(parsedLog, parsedBallotImage, validMachines)
#FORMAT OUTPUT
now = datetime.datetime.now()
print "RUN DATE:"+now.strftime("%Y-%m-%d %H:%M")
print "NOTE: This report doesn't include early voting terminals nor the precincts that were closed before 7:00 PM"
print "Precinct Number    "+" Average close time after 7:00 PM (hh:mm:ss)"
#sort in descending order the dictionary by value.
for key, value in sorted(mapOpenLateTime.iteritems(), key=lambda (k,v): (v,k), reverse = True):
    print "%3s                 %s" % (key, value)
analysis_places_open_late2.graphOpenLate(mapOpenLateTime)
