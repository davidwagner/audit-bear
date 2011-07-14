#!/usr/bin/python
from __future__ import division
def consecutiveVotes(parsedLog, ballotImage, validMachines, pollingLate):
    import collections as col
    import dateutil.parser as dp
    import datetime
    import numpy as np
    
    mapMachines = {} # key->machine serial number, value-> average time between consecutive votes after 7:00PM
    mapCountCV = {} # key->machine serial number, value-> count each time when a consecutive two votes events is found (votes after 7:00PM)

    mapMachinesB = {} # key->machine serial number, value-> average time between consecutive votes before 7:00PM
    mapCountCVB = {} # key->machine serial number, value-> count each time when a consecutive two votes events are found (votes before 7:00PM)
    
    mapMachinesAllTimes = {} #key->machine serial number, value-> a list of each time two consecutive votes are found in that machine ex: [(2nd vote - 1st vote),1st vote, 2nd vote] (after 7:00 PM)
    mapMachinesAllTimesB={} #key->machine serial number, value-> a list of each time two consecutive votes are found in that machine ex: [(2nd vote - 1st vote),1st vote, 2nd vote] (before 7:00 PM)
    precinctNumMap = parsedBallotImage.getPrecinctNumMap()

    earlyVoting = parsedBallotImage.getEarlyVotingList()
    for i in range(0, len(parsedLog)-1):
        if not ((parsedLog[i][0] in validMachines) and (precinctNumMap.has_key(parsedLog[i][0])) and (precinctNumMap[parsedLog[i][0]] in pollingLate.keys()) and (not parsedLog[i][0] in earlyVoting)):
            continue
        
        if parsedLog[i][4] in ("0001510", "0001511") and parsedLog[i+1][4] in ("0001510", "0001511"):
            if parsedLog[i+1][3][11:] < "19:00:00":
                t1 = dp.parse(parsedLog[i][3])
                t1 = datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
                
                t2 = dp.parse(parsedLog[i+1][3])
                t2 = datetime.timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
                delta1 = t2 - t1
                
                mapMachinesAllTimesB.setdefault(parsedLog[i][0],[]).append([round(delta1.seconds/60,1), str(t1), str(t2)])
                mapMachinesB[parsedLog[i][0]] = mapMachinesB.get(parsedLog[i][0], 0) + round(delta1.seconds/60,1)
                mapCountCVB[parsedLog[i][0]] = mapCountCVB.get(parsedLog[i][0], 0) + 1
        
        if parsedLog[i][4] in ("0001510", "0001511") and parsedLog[i+1][4] in ("0002810") and parsedLog[i+2][4] in ("0001510", "0001511"):
            if parsedLog[i+1][3][11:] < "19:00:00":
                t1 = dp.parse(parsedLog[i][3])
                t1 = datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
                
                t2 = dp.parse(parsedLog[i+2][3])
                t2 = datetime.timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
                delta1 = t2 - t1
                
                mapMachinesAllTimesB.setdefault(parsedLog[i][0],[]).append([round(delta1.seconds/60,1), str(t1), str(t2)])
                mapMachinesB[parsedLog[i][0]] = mapMachinesB.get(parsedLog[i][0], 0) + round(delta1.seconds/60,1)
                mapCountCVB[parsedLog[i][0]] = mapCountCVB.get(parsedLog[i][0], 0) + 1

        if parsedLog[i][4] in ("0001510", "0001511") and parsedLog[i+1][4] in ("0002810") and parsedLog[i+2][4] in ("0001510", "0001511"):
            if parsedLog[i][3][11:] >= "19:00:00":
               
                t1 = dp.parse(parsedLog[i][3])
                t1 = datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
                
                t2 = dp.parse(parsedLog[i+2][3])
                t2 = datetime.timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
                delta1 = t2 - t1
                
                mapMachinesAllTimes.setdefault(parsedLog[i][0],[]).append([round(delta1.seconds/60,1), str(t1), str(t2)])
                mapMachines[parsedLog[i][0]] = mapMachines.get(parsedLog[i][0], 0) + round(delta1.seconds/60,1)
                mapCountCV[parsedLog[i][0]] = mapCountCV.get(parsedLog[i][0], 0) + 1
                
    #for machine in sorted(mapMachinesAllTimesB):
        #print machine, mapMachinesAllTimesB[machine]
    #calculate average time between consecutive votes after 7 PM in each machine.
    for machine in mapMachines:
        try:
            mapMachines[machine] = round((mapMachines[machine] / mapCountCV[machine]), 1)
        except:
            continue
    
    pMap = {} #key-> precinct number, value-> list of average times between consecutive votes after 7:00 PM (match the average time in each machine with its precinct)
    
    for key in mapMachines:
        pMap.setdefault(precinctNumMap[key],[]).append(mapMachines[key])
    
    for key in pMap:
        print key, np.average(pMap[key]), np.std(pMap[key])
    
    pTimeVotesA = {}#key-> precinct number, value-> average time between consecutive votes after 7:00 PM
    
    for location in pMap:
        pTimeVotesA[location] = round(np.average(pMap[location]),1)
    
     #calculate average time between consecutive votes before 7 PM in each machine.
    for machine in mapMachinesB:
        try:
            mapMachinesB[machine] = round((mapMachinesB[machine] / mapCountCVB[machine]), 1)
        except:
            continue

    pMapB = {} #key-> precinct number, value-> list of average times between consecutive votes before 7:00 PM (match the average time in each machine with its precinct)
    for key in mapMachinesB:
        if mapMachines.has_key(key):
            pMapB.setdefault(precinctNumMap[key],[]).append(mapMachinesB[key])
    
    pTimeVotesB = {} #key-> precinct number, value-> average time between consecutive votes before 7:00 PM
    for location in pMapB:
        pTimeVotesB[location] = round(np.average(pMapB[location]),1)
     
    return (pTimeVotesA, pTimeVotesB)

def graphTimePoll(pollTime):
    print pollTime[0]
    print pollTime[1]
    import matplotlib.pyplot as plt
    import numpy as np
    mapRange = {}
    
    tMax = 10
    tMin = 0
    
    while tMin <= tMax:
        mapRange[tMin] = 0
        tMin += 1
    
    for average in pollTime[1]:
        for key in mapRange:
            if key <= average < key+1:
                mapRange[key] += 1
    print round(np.average(pollTime[1]), 1)
    plt.bar(mapRange.keys(), mapRange.values(), .98)
    plt.axis([0, max(mapRange.keys())+1, 0, max(mapRange.values())+1])
    plt.yticks(np.arange(0,max(mapRange.values())+1, 1))
    plt.xticks(np.arange(0,max(mapRange.keys())+1,1))
    plt.grid(True)
    plt.ylabel('Number of ocurrences')
    plt.xlabel('Range time (minutes)')
    plt.title('Time vs. Number of ocurrences between consecutive votes in precinct '+ pollTime[0])
    plt.show()
    return
def graphTimeVotes(mapVotes, time):
    import matplotlib.pyplot as plt
    
    mapRange = {}
    for key in mapVotes:
        mapRange[mapVotes[key]] = 0
    
    for average in mapRange:
        for location in mapVotes:
            if mapVotes[location] == average:
                mapRange[average] += 1
   
    plt.bar(mapRange.keys(), mapRange.values(), .1)
    plt.axis([0, max(mapRange.keys())+1, 0, max(mapRange.values())+1])
    plt.grid(True)
    plt.ylabel('Number of precincts')
    plt.xlabel('Average time between votes events (minutes)')
    plt.title('Time between consecutive votes '+ time +' 7 PM')
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
pA, pB = consecutiveVotes(parsedLog, parsedBallotImage, validMachines, pollOpenLate)
#for key, value in sorted(pA.iteritems(), key=lambda (k,v): (v,k), reverse = False):
    #print "%3s                 %s" % (key, value)

#print map['24']
graphTimeVotes(pA, 'after')
graphTimeVotes(pB, 'before')
#graphTimePoll(pCount.items()[6])
