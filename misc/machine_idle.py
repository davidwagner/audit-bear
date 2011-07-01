#!/usr/bin/python

#The program determines the time that each machine was idle, and matches
#the times to the precinct of each machine.
def machinesIdle(fh, parsedBallotImage, validMachines):
    term_open = False
    dic_idle = {}
    dic2 = {}
    idle = False
    
    earlyVotingList = parsedBallotImage.getEarlyVotingList()
    for entry in fh:
        if (not entry[0] in validMachines) or (entry[0] in earlyVotingList):
            continue
        if not entry[0] in dic2:
            term_open = False
            idle = False
            dic2[entry[0]]=[]        
        if entry[4] == "0001672":
            term_open = True
            time1 = dateutil.parser.parse(entry[3])
            continue
        if (entry[4] != "0001633") and (term_open and not idle):
            if entry[4] != "0001635":
                time1 = dateutil.parser.parse(entry[3])
        if (entry[4] == "0001633" or entry[4] == "0001635") and (term_open and not idle):
            idle = True
        if (entry[4] != "0001633") and (term_open and idle):
            if entry[4] != "0001635":
                idle = False
                time2 = dateutil.parser.parse(entry[3])
                delta = time2 - time1
                dic2[entry[0]].append(delta)
                time1 = time2

    dicM = {}
    for machine in dic2:
        s = datetime.timedelta(0)
        for time in dic2[machine]:
            s += time
            dicM[machine] = str(s)

    precinctNumMap = parsedBallotImage.getPrecinctNumMap()
    pMap = {}
    for key2 in dicM:
        if precinctNumMap.has_key(key2):
            pMap.setdefault(int(precinctNumMap[key2]),[]).append(dicM[key2])

    for key in sorted(pMap):
        print "Precinct #"+str(key)+" had machines idle for the times: "+str(pMap[key])
    return

#TEST THE FUNCTION
import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    
from auditLog import AuditLog
from ballotImage import BallotImage

import dateMod
import datetime
import dateutil.parser

path = sys.argv[1]
path2 = sys.argv[2]
path3 = sys.argv[3]

fh = AuditLog(open(path, 'r'))
parsedBallotImage = BallotImage(open(path2, 'r'))

dateModObject = dateMod.DateMod(fh, open(path3, 'r'))
mmap = dateMod.timecheck(dateMod.timeopen(dateModObject.edata))
validMachines = mmap.keys()

machinesIdle(fh, parsedBallotImage, validMachines)
