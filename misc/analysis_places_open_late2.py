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
        
        pMapAv[int(precinct)] = totalTime
    now = datetime.datetime.now()

    print "RUN DATE:"+now.strftime("%Y-%m-%d %H:%M")
    print "Precinct Number    "+" Time Opened after 7:00 PM (hh:mm:ss)"
    for p in sorted(pMapAv):
        print str(p) +"              "+"     "+str(pMapAv[p])
    #return dic2

#creates the graph, which shows how many machines were open late.
def graphOpenLate(dic):
    import numpy as np
    import matplotlib.pyplot as plt
    c = 0
    dicRange = {'0:00:00':0, '0:15:00':0, '0:30:00':0, '0:45:00':0, '1:00:00':0, '1:15:00':0, '1:30:00':0, '1:45:00':0, '2:00:00':0, '2:15:00':0, '2:30:00':0, '2:45:00':0}
    for s in dic:
        if dic[s][:2] == '' or dic[s][:2] == "-1":
            c+=1
        elif ('0:00:00' <= dic[s] < '0:15:00'):
            dicRange['0:00:00']+=1
        elif '0:15:00' <= dic[s] < '0:30:00':
            dicRange['0:15:00']+=1
        elif '0:30:00' <= dic[s] < '0:45:00':
            dicRange['0:30:00']+=1
        elif '0:45:00' <= dic[s] < '1:00:00':
            dicRange['0:45:00']+=1
        elif '1:00:00' <= dic[s] < '1:15:00':
            dicRange['1:00:00']+=1
        elif '1:15:00' <= dic[s] < '1:30:00':
            dicRange['1:15:00']+=1
        elif '1:30:00' <= dic[s] < '1:45:00':
            dicRange['1:30:00']+=1
        elif '1:45:00' <= dic[s] < '2:00:00':
            dicRange['1:45:00']+=1
        elif '2:00:00' <= dic[s] < '2:15:00':
            dicRange['2:00:00']+=1
        elif '2:15:00' <= dic[s] < '2:30:00':
            dicRange['2:15:00']+=1
        elif '2:30:00' <= dic[s] < '2:45:00':
            dicRange['2:30:00']+=1

    kList = []
    vList = []
    
    for k in sorted(dicRange.keys()):
        kList.append(k)
        vList.append(dicRange[k])
        
    N = 12
    ind = np.arange(N)
    width = 0.70
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, vList, .98, color='r')
    ax.set_xticks(ind+width/100.)
    ax.set_xticklabels(kList)
    ax.set_yticks(np.arange(0,max(vList)+10, 10))
    ax.set_ylabel('Number of units')
    ax.set_xlabel('Time Opened')
    ax.set_title('Machines stayed open after 7:00PM')
    plt.grid(True)
    plt.show()
    return

#main program
#TEST THE FUNCTION
open_late()
#import dateutil.parser
#import datetime
#import sys
#path = sys.argv[1]
#path = "anderson_co_01_14_11_el152.txt"
#data = readData(path)
#dicTC = open_late(data)
#graphOpenLate(dicTC)

#for key in dicTC:
   #if dicTC[key] == '' or dicTC[key][:2] == "-1":
       #continue
   #else:
       #print "Machine #"+ key + " was open late " + dicTC[key]+ " hours."
