#!/usr/bin/python
from __future__ import division
def consecutiveVotes(parsedLog, ballotImage, validMachines, pollingLate):
    import dateutil.parser as dp
    import datetime
    mapMachines = {}
    mapCountCV = {}
    td = datetime.timedelta(0)
    for i in range(0, len(parsedLog)-1):
        #if not line[0] in validMachines:
            #continue
        if not parsedLog[i][0] in mapMachines:
            mapMachines[parsedLog[i][0]] = 0
            mapCountCV[parsedLog[i][0]] = 0
            delta = datetime.timedelta(0)
            #count = 0
        if parsedLog[i][4] in ("0001510", "0001511") and parsedLog[i+1][4] in ("0002810") and parsedLog[i+2][4] in ("0001510", "0001511"):
            if parsedLog[i][3][11:] >= "19:00:00":
                #count += 1
                t1 = dp.parse(parsedLog[i][3])
                t1 = datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
                
                t2 = dp.parse(parsedLog[i+2][3])
                t2 = datetime.timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
                delta1 = t2 - t1
                
                #t3 = dp.parse(parsedLog[i+2][3])
                #t3 = datetime.timedelta(hours=t3.hour, minutes=t3.minute, seconds=t3.second)
                
                #t4 = dp.parse(parsedLog[i+3][3])
                #t4 = datetime.timedelta(hours=t4.hour, minutes=t4.minute, seconds=t4.second)
                
                #delta2 = t4 - t3
                #delta = delta1 + delta2
                mapMachines[parsedLog[i][0]] += round(delta1.seconds/60,1)
                mapCountCV[parsedLog[i][0]] += 1
                #print parsedLog[i][0] + " "+ str(round(delta1.seconds/60,1))
            else:
                continue
    
    for machine in mapMachines:
        try:
            mapMachines[machine] = round((mapMachines[machine] / mapCountCV[machine]), 1)
        except:
            continue
    
    precinctNumMap = parsedBallotImage.getPrecinctNumMap()
    pMap = {}
    for key in mapMachines:
        if precinctNumMap.has_key(key) and precinctNumMap[key] in pollingLate.keys():
            pMap.setdefault(precinctNumMap[key],[]).append(mapMachines[key])
    
    pTimeVotes = {}
    for location in pMap:
        t = 0
        for time in pMap[location]:
            t += time

        a = round(t/len(pMap[location]),1)
        pTimeVotes[location] = a
    
    for key in pTimeVotes:
        print key, pTimeVotes[key]
    return pTimeVotes

def graphTimeVotes(mapVotes):
    import matplotlib.pyplot as plt

    mapRange = {}
    for key in mapVotes:
        mapRange[mapVotes[key]] = 0
    
    print mapRange.items()
    
    for average in mapRange:
        for location in mapVotes:
            if mapVotes[location] == average:
                mapRange[average] += 1
    
    #for key in mapRange:
        #print key, mapRange[key]
    
    plt.bar(mapRange.keys(), mapRange.values(), .1)
    plt.axis([0, max(mapRange.keys()), 0, max(mapRange.values())+1])
    plt.grid(True)
    plt.show()
    return
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
parsedBallotImage = BallotImage(open(path2, 'r'), AuditLog(open(path, 'r')), open(path3, 'r'))


# first generate list of valid machines
dateModObject = dateMod.DateMod(parsedLog, open(path3, 'r'))
mmap = dateMod.timecheck(dateMod.timeopen(dateModObject.edata))
validMachines = mmap.keys()
pollOpenLate = analysis_places_open_late2.open_late(parsedLog, parsedBallotImage, validMachines)
map = consecutiveVotes(parsedLog, parsedBallotImage, validMachines, pollOpenLate)
graphTimeVotes(map)
