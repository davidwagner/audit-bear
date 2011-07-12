#!/usr/bin/python
from __future__ import division
def consecutiveVotes(parsedLog, ballotImage, validMachines, pollingLate):
    import collections as col
    import dateutil.parser as dp
    import datetime
    mapMachines = {}
    mapCountCV = {}

    mapMachinesB = {}
    mapCountCVB = {}
    #mapCountTR = {}
    td = datetime.timedelta(0)
    precinctNumMap = parsedBallotImage.getPrecinctNumMap()
    pCountA = {}
    pCountB = {}
    for i in range(0, len(parsedLog)-1):
        if not (parsedLog[i][0] in validMachines and precinctNumMap.has_key(parsedLog[i][0]) and precinctNumMap[parsedLog[i][0]] in pollingLate.keys()):
            continue
        if not parsedLog[i][0] in mapMachines:
            #mapMachines[parsedLog[i][0]] = 0
            #mapCountCV[parsedLog[i][0]] = 0
            #mapCountTR[parsedLog[i][0]] = []

            #mapMachinesB[parsedLog[i][0]] = 0
            #mapCountCVB[parsedLog[i][0]] = 0

            delta = datetime.timedelta(0)
        if parsedLog[i][4] in ("0001510", "0001511") and parsedLog[i+1][4] in ("0001510", "0001511"):
            if parsedLog[i+1][3][11:] < "19:00:00":
                t1 = dp.parse(parsedLog[i][3])
                t1 = datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
                
                t2 = dp.parse(parsedLog[i+1][3])
                t2 = datetime.timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
                delta1 = t2 - t1
                
                #mapMachinesB[parsedLog[i][0]] += round(delta1.seconds/60,1)
                #mapCountCVB[parsedLog[i][0]] += 1
                
                mapMachinesB[parsedLog[i][0]] = mapMachinesB.get(parsedLog[i][0], 0) + round(delta1.seconds/60,1)
                mapCountCVB[parsedLog[i][0]] = mapCountCVB.get(parsedLog[i][0], 0) + 1

                pCountB.setdefault(precinctNumMap[parsedLog[i][0]],[]).append(round(delta1.seconds/60,1))
        
        if parsedLog[i][4] in ("0001510", "0001511") and parsedLog[i+1][4] in ("0002810") and parsedLog[i+2][4] in ("0001510", "0001511"):
            if parsedLog[i+1][3][11:] < "19:00:00":
                t1 = dp.parse(parsedLog[i][3])
                t1 = datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
                
                t2 = dp.parse(parsedLog[i+2][3])
                t2 = datetime.timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
                delta1 = t2 - t1
                
                #mapMachinesB[parsedLog[i][0]] += round(delta1.seconds/60,1)
                #mapCountCVB[parsedLog[i][0]] += 1
                
                mapMachinesB[parsedLog[i][0]] = mapMachinesB.get(parsedLog[i][0], 0) + round(delta1.seconds/60,1)
                mapCountCVB[parsedLog[i][0]] = mapCountCVB.get(parsedLog[i][0], 0) + 1

                pCountB.setdefault(precinctNumMap[parsedLog[i][0]],[]).append(round(delta1.seconds/60,1))

        if parsedLog[i][4] in ("0001510", "0001511") and parsedLog[i+1][4] in ("0002810") and parsedLog[i+2][4] in ("0001510", "0001511"):
            if parsedLog[i][3][11:] >= "19:00:00":
               
                t1 = dp.parse(parsedLog[i][3])
                t1 = datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
                
                t2 = dp.parse(parsedLog[i+2][3])
                t2 = datetime.timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
                delta1 = t2 - t1
                
                mapMachines[parsedLog[i][0]] = mapMachines.get(parsedLog[i][0], 0) + round(delta1.seconds/60,1)
                mapCountCV[parsedLog[i][0]] = mapCountCV.get(parsedLog[i][0], 0) + 1
                pCountA.setdefault(precinctNumMap[parsedLog[i][0]],[]).append(round(delta1.seconds/60,1))
    
    #for key in pCount:
        #print key, pCount[key]

    #calculate average time between consecutive votes after 7 PM in each machine.
    for machine in mapMachines:
        try:
            mapMachines[machine] = round((mapMachines[machine] / mapCountCV[machine]), 1)
        except:
            continue

    #calculate average time between consecutive votes before 7 PM in each machine.
    for machine in mapMachinesB:
        try:
            mapMachinesB[machine] = round((mapMachinesB[machine] / mapCountCVB[machine]), 1)
        except:
            continue
    #tomorrow: calculate the average in the pCountA and pCountB maps values, and store the average in pTimeVotesA and pTimeVotesB.    
    pMap = {}
    for key in mapMachines:
        #if precinctNumMap.has_key(key) and precinctNumMap[key] in pollingLate.keys():
        pMap.setdefault(precinctNumMap[key],[]).append(mapMachines[key])
    
    for key in pMap:
        print key, pMap[key]

    pTimeVotes = {}
    for location in pMap:
        t = 0
        for time in pMap[location]:
            t += time

        a = round(t/len(pMap[location]),1)
        pTimeVotes[location] = a
    
    pTimeVotes2 = {}
    for key in pTimeVotes:
        if pTimeVotes[key] != 0.0:
            pTimeVotes2[key] = pTimeVotes[key]
            #print key, pTimeVotes2[key]
    return (pCountA, pTimeVotes2)

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
def graphTimeVotes(mapVotes):
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
    plt.title('Time between consecutive votes after 7 PM')
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
pCount, map = consecutiveVotes(parsedLog, parsedBallotImage, validMachines, pollOpenLate)
#print map['24']
graphTimeVotes(map)
#graphTimePoll(pCount.items()[6])
