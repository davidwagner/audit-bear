# EVENT ANOMALIES ANALYSES MODULE
import auditLog
import ballotImage
import dateMod
import dateutil.parser
import report

import operator
import string as stri
import math
import StringIO
import matplotlib
import matplotlib.pyplot as plt

from dateutil.parser import parse

def eventAnomalies(data, r):
    emMap = {}
    emMap2 = {}
    emList = []
    for x in data.getEntryList():
        if emMap.has_key(x.eventNumber):
            if x.serialNumber in emMap[x.eventNumber]:
                continue
            else:
                emMap[x.eventNumber] += [x.serialNumber]
        else:
            emMap[x.eventNumber] = [x.serialNumber]
    for x2 in emMap:
        emMap2[x2] = len(emMap[x2])
    emList = sorted(emMap2.iteritems(), key=operator.itemgetter(1))
    for x3 in emList:
        if x3[1] == 1:
            r.addTextBox("Machine %s has 1 occurence of event %s" % (emMap[x3[0]][0], x3[0]))
    return r
    
def lowBatteryMachines(data, ballot, r):
    lowBatteryList = []
    lowBatteryMap = {}
    for x in data.getEntryList():
        s = x.dateTime.split(" ")
        t = s[1].split(":")
        if t[0] == '':
            continue
        elif x.eventNumber == '0001635' and s[0] == '11/02/2010' and stri.atoi(t[0]) > 7 and stri.atoi(t[0]) < 19:
            if x.serialNumber not in lowBatteryList and not lowBatteryMap.has_key(x.serialNumber):
                lowBatteryList.append(x.serialNumber)
                r.addTextBox(x.serialNumber)
                lowBatteryMap[x.serialNumber] = 1
            elif lowBatteryMap.has_key(x.serialNumber):
                temp = lowBatteryMap[x.serialNumber]
                temp = temp + 1
                lowBatteryMap[x.serialNumber] = temp
    return r
    
def getWarningEvents(data,ballot,r):
    r.addTitle('Detection of Anomalous Warning Events')
    wMap = {}
    wNumMap = {}
    list1628 = []
    list1651 = []
    list1703 = []
    list1704 = []
    list1404 = []
    totalList = []
    minorTicks = (.5,)
    avg = 0
    maxNumOccurrences = 0   
    stdev = 0.00000000
    ssum = 0.00000000
    ssum2 = 0.00000000     
    wEvents = ['0001628', '0001651', '0001703', '0001704']
    for x in data.getEntryList():
        s = x.dateTime.split(" ")
        t = s[1].split(":")
        if t[0] == '':
            continue
        elif stri.atoi(t[0]) > 7 and stri.atoi(t[0]) < 19 and s[0] == '11/02/2010':
            if x.eventNumber in wEvents:
                if wMap.has_key(x.serialNumber):
                    if wMap[x.serialNumber].has_key(x.eventNumber):
                        temp = wMap[x.serialNumber][x.eventNumber]
                        temp = temp + 1
                        wMap[x.serialNumber][x.eventNumber] = temp
                    else:
                        tempMap = wMap[x.serialNumber]
                        tempMap[x.eventNumber] = 1
                        wMap[x.serialNumber] = tempMap
                else:
                    tempMap = {}
                    tempMap[x.eventNumber] = 1
                    wMap[x.serialNumber] = tempMap
    for y in wMap:
        temp = 0
        for y2 in wMap[y]:
            temp = temp + wMap[y][y2]
        wNumMap[y] = temp
    if len(wMap) < 1:
        r.addTextBox("This county experienced no Warning events.")
        print "This county experienced no 'Warning' events."
    else:
        for z in wMap:
            for z2 in wMap[z]:
                precinctNum = None
                precinctName = None
                if ballot.machinePrecinctNumMap.has_key(z):
                    precinctNum = ballot.machinePrecinctNumMap[z]
                    precinctName = ballot.machinePrecinctNameMap[z]
                elif z in ballot.earlyVotingList:
                    precinctNum = '750'
                    precinctName = 'Absentee'
                elif z in ballot.failsafeList:
                    precinctNum = '850'
                    precinctName = 'Absentee'
                totalList.append((z, precinctNum, precinctName, wMap[z][z2], z2, data.getEventDescription(z2)))
                if wMap[z][z2] > maxNumOccurrences:
                    maxNumOccurrences = wMap[z][z2] 
                if z2 == '0001628':
                    list1628.append(wMap[z][z2])
                elif z2 == '0001651':
                    list1651.append(wMap[z][z2]) 
                elif z2 == '0001703':
                    list1703.append(wMap[z][z2])
                elif z2 == '0001704':
                    list1704.append(wMap[z][z2])
                elif z2 == '0001404':
                    list1404.append(wMap[z][z2])
                    
        warningTable = report.Table()

        isOutlier = True
        for w in totalList:
            avg = avg + w[3]
        avg = avg/len(totalList)
        for w2 in totalList:
            ssum = ssum + ((w2[3]-avg)**2)
        ssum2 = ssum/len(totalList)
        stdev = math.sqrt(ssum2)
        for w3 in totalList:
            if w3[3] >= math.floor(avg + (2.5*stdev)):
                if isOutlier == True:
                    warningTable.addHeader('Precinct Name')
                    warningTable.addHeader('Precinct #')
                    warningTable.addHeader('Machine Serial Number')
                    warningTable.addHeader('Event #')
                    warningTable.addHeader('Event Description')
                    warningTable.addHeader('# of Occurrences (Outlier)')
                    warningTable.addHeader('Possible Reasons/ Suggestions')
                    isOutlier = False
                warningTable.addRow([w3[2], w3[1], w3[0], w3[4], w3[5], repr(w3[3]), 'TODO'])
                #print "%-10s %-5s %-20s %-5d %-7s %s" % (w3[0], w3[1], w3[2], w3[3], w3[4], w3[5])
        warningTable.generateHTML()
        r.addTable(warningTable)
        #r.addTextBox(list1628)
        #r.addTextBox(list1651)
        #r.addTextBox(list1703)
        #r.addTextBox(list1704)
        #r.addTextBox(list1404)
        fig = plt.figure(figsize=(22,14))
        ax2 = fig.add_axes([0.15, 0.1, .7, .8])

        n, bins, patches = plt.hist([list1628, list1651, list1703, list1704, list1404], bins=maxNumOccurrences+1, range=(0,maxNumOccurrences+1), align='left', label=['0001628: '+data.getEventDescription('0001628'), '0001651: '+data.getEventDescription('0001651'), '0001703: '+data.getEventDescription('0001703'), '0001704: '+data.getEventDescription('0001704'), '0001404: '+data.getEventDescription('0001404')])
        
        for b in bins:
            minorTicks += ((b-.5),)
        ax2.set_xticks(minorTicks, minor=True)
        ax2.grid(b=True, which='minor')
        ax2.set_xlabel('Per Machine Occurrences')
        ax2.set_ylabel('# of Machines')
        ax2.set_title('Frequency of Warning Events')
        ax2.legend()  
        stio = StringIO.StringIO()
        plt.savefig(stio)
        im = report.Image(stio, 'Vote Cancelled Events')
        r.addImage(im)                   
    return r
    
def getVoteCancelledEvents(data,ballot,r):
    r.addTitle('Detection of Anomalous Vote Cancelled Events')
    vcMap = {}
    vcNumMap = {}
    list1513 = []
    list1514 = []
    list1515 = []
    list1516 = []
    list1517 = []
    list1518 = []
    list1519 = []
    totalList = []
    minorTicks = (.5,)
    maxNumOccurrences = 0
    avg = 0
    count = 0
    stdev = 0.00000000
    ssum = 0.00000000
    ssum2 = 0.00000000
    vcEvents = ['0001513', '0001514', '0001515', '0001516', '0001517', '0001518', '0001519']
    for x in data.getEntryList():
        s = x.dateTime.split(" ")
        t = s[1].split(":")
        if t[0] == '':
            continue
        if stri.atoi(t[0]) > 7 and stri.atoi(t[0]) < 19 and s[0] == '11/02/2010':
            if x.eventNumber in vcEvents:
                if vcMap.has_key(x.serialNumber):
                    if vcMap[x.serialNumber].has_key(x.eventNumber):
                        temp = vcMap[x.serialNumber][x.eventNumber]
                        temp = temp + 1
                        vcMap[x.serialNumber][x.eventNumber] = temp
                    else:
                        tempMap = vcMap[x.serialNumber]
                        tempMap[x.eventNumber] = 1
                        vcMap[x.serialNumber] = tempMap
                else:
                    tempMap = {}
                    tempMap[x.eventNumber] = 1
                    vcMap[x.serialNumber] = tempMap
    for y in vcMap:
        temp = 0
        for y2 in vcMap[y]:
            temp = temp + vcMap[y][y2]
        vcNumMap[y] = temp
    if len(vcMap) < 1:
        r.addTextBox("This county experienced no Vote Cancelled events.")
        print "This county experienced no 'vote cancelled' events."
    else:
        for z in vcMap:
            for z2 in vcMap[z]:
                precinctNum = None
                precinctName = None
                if ballot.machinePrecinctNumMap.has_key(z):
                    precinctNum = ballot.machinePrecinctNumMap[z]
                    precinctName = ballot.machinePrecinctNameMap[z]
                elif z in ballot.earlyVotingList:
                    precinctNum = '750'
                    precinctName = 'Absentee'
                elif z in ballot.failsafeList:
                    precinctNum = '850'
                    precinctName = 'Absentee'
                totalList.append((z, precinctNum, precinctName, vcMap[z][z2], z2, data.getEventDescription(z2)))
                if vcMap[z][z2] > maxNumOccurrences:
                    maxNumOccurrences = vcMap[z][z2] 
                if z2 == '0001513':
                    list1513.append(vcMap[z][z2])
                elif z2 == '0001514':
                    list1514.append(vcMap[z][z2])
                elif z2 == '0001515':
                    list1515.append(vcMap[z][z2])
                elif z2 == '0001516':
                    list1516.append(vcMap[z][z2])
                elif z2 == '0001517':
                    list1517.append(vcMap[z][z2])
                elif z2 == '0001518':
                    list1518.append(vcMap[z][z2])
                elif z2 == '0001519':
                    list1519.append(vcMap[z][z2])
        for w in totalList:
            avg = avg + w[3]
        avg = avg/len(totalList)
        for w2 in totalList:
            ssum = ssum + ((w2[3]-avg)**2)
        ssum2 = ssum/len(totalList)
        stdev = math.sqrt(ssum2)
        voteCancelledTable = report.Table()
        

        isOutlier = True
        #r.addTextBox("%10s %10s %20s %7s %7s %s" % ('Machine #', 'Precinct #', 'Precinct Name', 'Outlier', 'Event #', 'Event Description'))
        for w3 in totalList:
            if w3[3] > (avg + (4*stdev)):
                if isOutlier == True:
                    voteCancelledTable.addHeader('Precinct Name')
                    voteCancelledTable.addHeader('Precinct Number')
                    voteCancelledTable.addHeader('Machine Serial Number')
                    voteCancelledTable.addHeader('Event #')
                    voteCancelledTable.addHeader('Event Description')
                    voteCancelledTable.addHeader('# of Occurences (Outlier)')
                    voteCancelledTable.addHeader('Possible Reasons/ Suggestions')
                    isOutlier = False
                #t = "%10s %5s %20s %5d %7s %s" % (w3[0], w3[1], w3[2], w3[3], w3[4], w3[5])
                voteCancelledTable.addRow([w3[2], w3[1], w3[0], w3[4], w3[5], repr(w3[3]), 'TODO'])
                #voteCancelledTable.addRow("%10s %5s %20s %5d %7s %s" % (w3[0], w3[1], w3[2], w3[3], w3[4], w3[5])) 
        
        voteCancelledTable.generateHTML()
        r.addTable(voteCancelledTable)        
        fig = plt.figure(figsize=(22,14))
        ax2 = fig.add_axes([0.15, 0.1, .7, .8])
        n, bins, patches = plt.hist([list1513, list1514, list1515, list1516, list1517, list1518, list1519], bins=maxNumOccurrences+1, range=(0,maxNumOccurrences+1), align='left', label=['0001513: '+data.getEventDescription('0001513'),'0001514: '+data.getEventDescription('0001514'), '0001515: '+data.getEventDescription('0001515'), '0001516: '+data.getEventDescription('0001516'), '0001517: '+data.getEventDescription('0001517'), '0001518: '+data.getEventDescription('0001518'), '0001519: '+data.getEventDescription('0001519')])
        for b in bins:
            minorTicks += ((b-.5),)
        ax2.set_xticks(minorTicks, minor=True)
        ax2.grid(b=True, which='minor')
        ax2.set_xlabel('Per Machine Occurrences')
        ax2.set_ylabel('# of Machines')
        ax2.set_title('Frequency of Vote Cancelled Events')
        ax2.legend()
        stio = StringIO.StringIO()
        plt.savefig(stio)
        im = report.Image(stio, 'Vote Cancelled Events')
        r.addImage(im)
    return r
