#test the functions of analysis_places_open_late2
import dateutil.parser
import datetime
from auditLog import AuditLog
from ballotImage import BallotImage
from el68a import EL68A
import dateMod
import report

def closedLate(parsedLog, parsedBallotImage, parsedEL68A, dateModObject):
    r = report.Report()
    r.addTitle("Machines that closed late")

    times, a = dateMod.timeopen(parsedLog, dateModObject.eday)
    mmap = dateMod.timecheck(times)
    validMachines = mmap.keys()
    mapOpenLateTime = open_late(parsedLog, parsedBallotImage, validMachines)

    #FORMAT OUTPUT
    now = datetime.datetime.now()
    r.addTextBox("<i>NOTE: This report doesn't include early voting terminals nor the precincts that were closed before 7:30 PM</i>")
    table = report.Table()
    table.addHeader("#")
    table.addHeader("Precinct")
    table.addHeader("Average close time after 7:30 PM")
    
    #sort in descending order the dictionary by value.
    thresholdValue = datetime.timedelta(hours=7, minutes=30)
    precinctMap = parsedBallotImage.getPrecinctMap()
    i = 0
    for key, value in sorted(mapOpenLateTime.iteritems(), key=lambda (k,v): (v,k), reverse = True):
        if value > thresholdValue:
            i += 1
            table.addRow([key, precinctMap[key], str(value)])

    if i == 0:
        return []

    r.addTable(table)
    return [r]


#read the audit log file and store each line in the data list.

#create two dictionaries which keys are the serial numbers and the values of the first one is a list with the time of each vote cast by voter or poll worker.
#The second dictionary contains the serial numbers as keys and the difference between the last vote and the closing time (7:00 PM) as values,
#to determine if the machine was open late (after 7:00PM).
def open_late(parsedLog, parsedBallotImage, validMachines):
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
                t2 = datetime.timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)

                t1 = dateutil.parser.parse(dic[line[0]][0][:10]+ " 19:00:00")
                t1 = datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
            except:
                continue
            else:
                delta = (t2 - t1) + datetime.timedelta(hours=7)
                dic2[line[0]] = delta

    earlyVotingList = parsedBallotImage.getEarlyVotingList()
    mapM = {}    
    for key in dic2:
        if not key in earlyVotingList and str(dic2[key])[:1] >= "7":
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
        pMapAv[precinct] = t
        
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
        
        pMapAv[precinct] = totalTime
    
    return pMapAv

#creates the graph, which shows how many precincts were open late.
def graphOpenLate(dic):
    import numpy as np
    import matplotlib.pyplot as plt
    dicRange = {}
    
    tMax = datetime.timedelta(hours = 9)
    tMin = datetime.timedelta(hours = 7)
    
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
    ax.set_ylabel('Number of precincts')
    ax.set_xlabel('Close time (hh:mm:ss)')
    ax.set_title('Precincts closed after 7:00PM')
    plt.grid(True)
    plt.show()
    return
