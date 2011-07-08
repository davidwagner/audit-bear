#!/usr/bin/python
from __future__ import division
def consecutiveVotes(parsedLog, ballotImage, validMachines, pollingLate):
    import dateutil.parser as dp
    import datetime
    mapMachines = {}
    mapCountCV = {}
    td = datetime.timedelta(0)
    countIM = 0
    countVM = 0
    for line in parsedLog:
        if not line[0] in validMachines:
            continue
        if not line[0] in mapMachines:
            mapMachines[line[0]] = 0
            mapCountCV[line[0]] = 0
            delta = datetime.timedelta(0)
            count = 0
            countVM += 1
        if line[4] in ("0001510", "0001511", "0001513", "0001514", "0001515", "0001516", "0001517", "0001518", "0001519"):
            if line[3][11:] >= "19:00:00":
                count += 1
                if count == 1:
                    t1 = dp.parse(line[3])
                    t1 = datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
                    delta = t1 - delta
                    t2 = delta
                else:
                    t1 = dp.parse(line[3])
                    t1 = datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
                    delta = (t1 - t2)
                    t2 = t1
                    mapMachines[line[0]] += (delta.seconds/60)
                    mapCountCV[line[0]] += 1
                    #print line[0] + " "+str(delta)
            else:
                continue
    mapMachines2 = {}
    for machine in mapMachines:
        try:
            mapMachines[machine] = round((mapMachines[machine] / mapCountCV[machine]), 1)
        except:
            continue
    
    precinctNumMap = parsedBallotImage.getPrecinctNumMap()
    pMap = {}
    for key in mapMachines:
        #countT = 0
        if precinctNumMap.has_key(key) and precinctNumMap[key] in pollingLate.keys():
            #countT += 1
            pMap.setdefault(precinctNumMap[key],[]).append(mapMachines[key])
    for key in pMap:
        print key, pMap[key]
    #print count
#test functions
import analysis_places_open_late2
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
pollOpenLate = analysis_places_open_late2.open_late(parsedLog, parsedBallotImage, validMachines)
consecutiveVotes(parsedLog, parsedBallotImage, validMachines, pollOpenLate)
