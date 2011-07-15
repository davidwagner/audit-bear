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
    
    listTimeVotes = [] #store all the times between consecutive votes after 7 PM
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
                
                listTimeVotes.append(round(delta1.seconds/60,1))
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
     
    return (mapMachinesAllTimes, mapMachinesAllTimesB, listTimeVotes, pTimeVotesA, pTimeVotesB)

def longLine(parsedBallotImage, mapAllTimesA, mapAllTimes):
    precinctNumMap = parsedBallotImage.getPrecinctNumMap()
    pollingLocations7 = {}
    pollingLocations8 = {}
    pollingLocations9 = {}
    pollingLocations10 = {}
    pollingLocations11 = {}
    pollingLocations12 = {}
    pollingLocations13 = {}
    pollingLocations14 = {}
    pollingLocations15 = {}
    pollingLocations16 = {}
    pollingLocations17 = {}
    pollingLocations18 = {}
    pollingLocations19 = {}
    for machine in mapAllTimes:
        for value in mapAllTimes[machine]:
            #t1 = value[1].split(':')
            #t2 = value[2].split(':')
            if value[1][:1] == '7' and value[2][:1] == '7':
                pollingLocations7.setdefault(precinctNumMap[machine],[]).append(value[0])
            if value[1][:1] == '8' and value[2][:1] == '8':
                pollingLocations8.setdefault(precinctNumMap[machine],[]).append(value[0])
            if value[1][:1] == '9' and value[2][:1] == '9':
                pollingLocations9.setdefault(precinctNumMap[machine],[]).append(value[0])
            if value[1][:2] == '10' and value[2][:2] == '10':
                pollingLocations10.setdefault(precinctNumMap[machine],[]).append(value[0])
            if value[1][:2] == '11' and value[2][:2] == '11':
                pollingLocations11.setdefault(precinctNumMap[machine],[]).append(value[0])
            if value[1][:2] == '12' and value[2][:2] == '12':
                pollingLocations12.setdefault(precinctNumMap[machine],[]).append(value[0])
            if value[1][:2] == '13' and value[2][:2] == '13':
                pollingLocations13.setdefault(precinctNumMap[machine],[]).append(value[0])
            if value[1][:2] == '14' and value[2][:2] == '14':
                pollingLocations14.setdefault(precinctNumMap[machine],[]).append(value[0])
            if value[1][:2] == '15' and value[2][:2] == '15':
                pollingLocations15.setdefault(precinctNumMap[machine],[]).append(value[0])
            if value[1][:2] == '16' and value[2][:2] == '16':
                pollingLocations16.setdefault(precinctNumMap[machine],[]).append(value[0])
            if value[1][:2] == '17' and value[2][:2] == '17':
                pollingLocations17.setdefault(precinctNumMap[machine],[]).append(value[0])
            if value[1][:2] == '18' and value[2][:2] == '18':
                pollingLocations18.setdefault(precinctNumMap[machine],[]).append(value[0])
    for machine in mapAllTimesA:
        for value in mapAllTimesA[machine]:
            #print value[1], value[2]
            pollingLocations19.setdefault(precinctNumMap[machine],[]).append(value[0])

    #for key in pollingLocations18:
        #print key, pollingLocations18[key]
    return (pollingLocations7,pollingLocations8,pollingLocations9,pollingLocations10,pollingLocations11,pollingLocations12,pollingLocations13,pollingLocations14,pollingLocations15,pollingLocations16,pollingLocations17,pollingLocations18,pollingLocations19)
def createMapRangePoll(pollTime, timewindow):
    print pollTime[0]
    print pollTime[1]
    
    mapRange = {}
    
    for time in pollTime[1]:
        mapRange[time] = 0
    
    for time in mapRange:
        for t2 in pollTime[1]:
            if t2 == time:
                mapRange[time] += 1
    
    graph(mapRange, 'Time between consecutive vote cast events (minutes)', 'Number of vote cast event pairs', 'Time vs Number of vote cast in precinct #'+pollTime[0]+' at '+timewindow)
    return
def createMapRange(mapVotes, time):
    
    mapRange = {}
    for key in mapVotes:
        mapRange[mapVotes[key]] = 0
    
    for average in mapRange:
        for key in mapVotes:
            if mapVotes[key] == average:
                mapRange[average] += 1
    graph(mapRange, 'Average time between votes events (minutes)', 'Number of precincts', 'Time between consecutive votes ' + time +' 7 PM')
    return
def graph(mapRange, x, y, title):
    import matplotlib.pyplot as plt
    import numpy as np
    plt.bar(mapRange.keys(), mapRange.values(), .1)
    plt.axis([0, max(mapRange.keys())+1, 0, max(mapRange.values())+1])
    plt.xticks(np.arange(0,max(mapRange.keys())+1,1))
    plt.yticks(np.arange(0,max(mapRange.values())+1, 1))
    plt.grid(True)
    plt.ylabel(y)
    plt.xlabel(x)
    plt.title(title)
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
#import random as rnd
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
mapMachA, mapMachB, lTV, pA, pB = consecutiveVotes(parsedLog, parsedBallotImage, validMachines, pollOpenLate)
#for key, value in sorted(pA.iteritems(), key=lambda (k,v): (v,k), reverse = False):
    #print "%3s                 %s" % (key, value)

mapTimeVotes = {}
for time in lTV:
    if not time in mapTimeVotes:
        mapTimeVotes[time] = 1
    else:
        mapTimeVotes[time] += 1
#rnd.seed()
pollLoc7, pollLoc8, pollLoc9, pollLoc10, pollLoc11, pollLoc12, pollLoc13, pollLoc14, pollLoc15, pollLoc16, pollLoc17, pollLoc18, pollLoc19 = longLine(parsedBallotImage, mapMachA, mapMachB)
#generate a random position to choose a random polling location
#pos = rnd.randint(0, len(pollLoc7)-1)
i = 0
for key in pollLoc19:
    i += 1
    if key == '26':
        #print key
        pos = i - 1
        break
createMapRangePoll(pollLoc19.items()[pos], '7:00 PM to close time')

#print map['24']
#createMapRange(pA, 'after')
#graph(mapTimeVotes, 'Time between consecutive vote cast events (minutes)', 'Number of vote cast event pairs', 'Time between votes vs Number of votes')
#graphTimeVotes(pB, 'before')
#graphTimePoll(pCount.items()[6])
