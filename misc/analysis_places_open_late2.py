#!/usr/bin/python
#read the audit log file and store each line in the data list.

#def readData(path):
    #return parsedLog

#create two dictionaries which keys are the serial numbers and the values of the first one is a list with the time of each vote cast by voter or poll worker.
#The second dictionary contains the serial numbers as keys and the difference between the last vote and the closing time (7:00 PM) as values,
#to determine if the machine was open late (after 7:00PM).
def open_late():
    import os, sys
    cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
    if cmd_folder not in sys.path:
        sys.path.insert(0, cmd_folder)

    from auditLog import AuditLog
    from ballotImage import BallotImage
    
    path = sys.argv[1]
    path2 = sys.argv[2]

    parsedLog = AuditLog(open(path, "r"))
    parsedBallotImage = BallotImage(open(path2, 'r'))

    import dateutil.parser
    import datetime
    dic = {}
    dic2 = {}
    
    for line in parsedLog:
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
            #print "Machine #"+ key + " was open late: " + str(mapM[key])+ " hours."
    
    precinctNumMap = parsedBallotImage.getPrecinctNumMap()
    pMap = {}
    
    # match the times that the machines were open late with their precincts
    for key2 in mapM:
        if precinctNumMap.has_key(key2):
            pMap.setdefault(precinctNumMap[key2],[]).append(mapM[key2])
    
    #for key in pMap:
        #print key, pMap[key]
    
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
        
        pMapAv[int(precinct)] = str(totalTime)
    
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
    import numpy as np
    import matplotlib.pyplot as plt
    dicRange = {'0:00:00':0, '0:10:00':0, '0:20:00':0, '0:30:00':0, '0:40:00':0, '0:50:00':0, '1:00:00':0, '1:10:00':0, '1:20:00':0, '1:30:00':0, '1:40:00':0, '1:50:00':0, '2:00:00':0}
    for s in dic:
        if ('0:00:00' <= dic[s] < '0:10:00'):
            dicRange['0:00:00']+=1
        elif '0:10:00' <= dic[s] < '0:20:00':
            dicRange['0:10:00']+=1
        elif '0:20:00' <= dic[s] < '0:30:00':
            dicRange['0:20:00']+=1
        elif '0:30:00' <= dic[s] < '0:40:00':
            dicRange['0:30:00']+=1
        elif '0:40:00' <= dic[s] < '0:50:00':
            dicRange['0:40:00']+=1
        elif '0:50:00' <= dic[s] < '1:00:00':
            dicRange['0:50:00']+=1
        elif '1:00:00' <= dic[s] < '1:10:00':
            dicRange['1:00:00']+=1
        elif '1:10:00' <= dic[s] < '1:20:00':
            dicRange['1:10:00']+=1
        elif '1:20:00' <= dic[s] < '1:30:00':
            dicRange['1:20:00']+=1
        elif '1:30:00' <= dic[s] < '1:40:00':
            dicRange['1:30:00']+=1
        elif '1:40:00' <= dic[s] < '1:50:00':
            dicRange['1:40:00']+=1
        elif '1:50:00' <= dic[s] < '2:00:00':
            dicRange['1:50:00']+=1

    kList = []
    vList = []
    
    for k in sorted(dicRange.keys()):
        kList.append(k)
        vList.append(dicRange[k])
        
    N = 13
    ind = np.arange(N)
    width = 0.70
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, vList, .98, color='r')
    ax.set_xticks(ind+width/100.)
    ax.set_xticklabels(kList)
    ax.set_yticks(np.arange(0,max(vList)+2, 2))
    ax.set_ylabel('Number of units')
    ax.set_xlabel('Time Opened')
    ax.set_title('Precincts stayed open after 7:00PM')
    plt.grid(True)
    plt.show()
    return

#main program
#TEST THE FUNCTIONS
map1 = open_late()
graphOpenLate(map1)
