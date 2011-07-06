#!/usr/bin/python
#read the audit log file and store each line in the data list.

#create two dictionaries which keys are the serial numbers and the values of the first one is a list with the time of each vote cast by voter or poll worker.
#The second dictionary contains the serial numbers as keys and the difference between the last vote and the closing time (7:00 PM) as values,
#to determine if the machine was open late (after 7:00PM).
def open_late(parsedLog, parsedBallotImage, validMachines):
    import dateutil.parser
    import datetime
    dic = {}
    dic2 = {}
    
    for line in parsedLog:
        if not line[0] in validMachines:
            continue        
        if not line[0] in dic:
            dic[line[0]] = []
            dic2[line[0]] = ""
        if line[4] in "0001510" or line[4] in "0001511":
            dic[line[0]].insert(0, line[3])
            try:
                t2 = dateutil.parser.parse(dic[line[0]][0])
                t1 = dateutil.parser.parse(dic[line[0]][0][:10]+ " 19:00:00")
            except:
                continue
            else:
                delta = t2 - t1
                dic2[line[0]] = delta

    earlyVotingList = parsedBallotImage.getEarlyVotingList()
    mapM = {}    
    for key in dic2:
        if not key in earlyVotingList and str(dic2[key])[:2] != "-1":
            mapM[key] = dic2[key]
    
    precinctNumMap = parsedBallotImage.getPrecinctNumMap()
    pMap = {}
    
    # match the times that the machines were open late with their precincts
    for key2 in mapM:
        if precinctNumMap.has_key(key2):
            pMap.setdefault(precinctNumMap[key2],[]).append(mapM[key2])
   
    #calculate the average time in which each precinct was open late.
    pMapAv = {}
    for precinct in pMap:
        t = datetime.timedelta(0)
        pMapAv[int(precinct)] = t
        
        #sum the time in which the last vote was cast in each machine
        for time in pMap[precinct]:
            t += time
        
        #calculate the time average
        a = t/len(pMap[precinct])
        sec = a.seconds
        hours = sec / 3600
        sec = sec % 3600
        minutes = sec / 60
        sec = sec % 60
        totalTime = datetime.timedelta(seconds = sec, minutes = minutes, hours = hours)
        
        pMapAv[int(precinct)] = totalTime
    
    now = datetime.datetime.now()
    
    #FORMAT OUTPUT
    print "RUN DATE:"+now.strftime("%Y-%m-%d %H:%M")
    print "NOTE: This report doesn't include early voting terminals nor the precincts that were closed before 7:00 PM"
    print "Precinct Number    "+" Time Opened after 7:00 PM (hh:mm:ss)"
    #sort in descending order the dictionary by value.
    for key, value in sorted(pMapAv.iteritems(), key=lambda (k,v): (v,k), reverse = True):
        print "%3d                 %s" % (key, value)
    return pMapAv

#creates the graph, which shows how many precincts were open late.
def graphOpenLate(dic):
    import dateutil.parser
    import datetime
    import numpy as np
    import matplotlib.pyplot as plt
    dicRange = {}
    
    tMax = datetime.timedelta(seconds = 0, minutes = 0, hours = 2)
    tMin = datetime.timedelta(0)
    
    while tMin <= tMax:
        dicRange[tMin] = 0
        tMin += datetime.timedelta(minutes=10)
    
    for s in dic:
        for key in dicRange:
            if key <= dic[s] < (key+datetime.timedelta(minutes=10)):
                dicRange[key] += 1
    
    mapRange = {}
    for key in dicRange:
        mapRange[str(key)] = dicRange[key]

    kList = []
    vList = []
    
    for k in sorted(mapRange.keys()):
        kList.append(k)
        vList.append(mapRange[k])
        
    N = 13
    ind = np.arange(N)
    width = 0.70
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, vList, .98, color='r')
    ax.set_xticks(ind+width/100.)
    ax.set_xticklabels(kList)
    ax.set_yticks(np.arange(0,max(vList)+2, 2))
    ax.set_ylabel('Number of polling locations')
    ax.set_xlabel('Time Opened (hh:mm:ss)')
    ax.set_title('Precincts stayed open after 7:00PM')
    plt.grid(True)
    plt.show()
    return

#main program
#TEST THE FUNCTIONS
#import os, sys
#cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
#if cmd_folder not in sys.path:
    #sys.path.insert(0, cmd_folder)

#from auditLog import AuditLog
#from ballotImage import BallotImage
#import dateMod

#path = sys.argv[1]
#path2 = sys.argv[2]
#path3 = sys.argv[3]

#parsedLog = AuditLog(open(path, "r"))
#parsedBallotImage = BallotImage(open(path2, 'r'))
#dateModObject = dateMod.DateMod(parsedLog, open(path3, 'r'))
#mmap = dateMod.timecheck(dateMod.timeopen(dateModObject.edata))
#validMachines = mmap.keys()
#mapOpenLateTime = open_late(parsedLog, parsedBallotImage, validMachines)
#graphOpenLate(mapOpenLateTime)
