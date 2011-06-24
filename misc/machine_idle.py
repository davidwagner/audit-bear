#!/usr/bin/python

#The program determines the time that each machine was idle, and matches
#the times to the precinct of each machine.
import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    
from auditLog import AuditLog
from ballotImage import BallotImage

import datetime
import dateutil.parser

path = sys.argv[1]
path2 = sys.argv[2]
fh = AuditLog(open(path, 'r'))
parsedBallotImage = BallotImage(open(path2, 'r'))

term_open = False
dic_idle = {}
dic2 = {}
idle = False

for entry in fh:
    if not entry[0] in dic2:
        term_open = False
        idle = False
        dic2[entry[0]]=[]        
    if entry[4] == "0001672":
        term_open = True
        time1 = dateutil.parser.parse(entry[3])
        continue
    if entry[4] != "0001633" and term_open and not idle:
        time1 = dateutil.parser.parse(entry[3])
        
    if entry[4] == "0001633" and term_open and not idle:
        idle = True
        
    if entry[4] != "0001633" and term_open and idle:
        idle = False
        time2 = dateutil.parser.parse(entry[3])
        delta = time2 - time1
        dic2[entry[0]].append(delta)
        time1= time2
        
dicM = {}
for machine in dic2:
    s = datetime.timedelta(0)
    for time in dic2[machine]:
        s += time
        dicM[machine] = str(s)
        #print s

dicNew = {}
earlyVotingList = parsedBallotImage.getEarlyVotingList()

for key in dicM:
    if not key in earlyVotingList:
        dicNew[key] = dicM[key]

for key in dicNew:
    print "Machine #"+ key+" was idle for "+ dicM[key] +" (hh:mm:ss)."

precinctNumMap = parsedBallotImage.getPrecinctNumMap()
pMap = {}
for key2 in dicNew:
    if precinctNumMap.has_key(key2):
        pMap.setdefault(precinctNumMap[key2],[]).append(dicNew[key2])

for key in pMap:
    print "Precinct #"+key+" had machines idle for the times: "+str(pMap[key])       
#print "Early voting " + str(len(earlyVotingList))
#print "dicM " + str(len(dicM))
#print "dicNew " + str(len(dicNew))
#parsedBallotImage.getEarlyVotingList()

