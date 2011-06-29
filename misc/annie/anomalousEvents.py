import operator
import string as stri
import matplotlib.pyplot as plt
import matplotlib
import math
import os
import sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import auditLog
import ballotImage

class AnomalousEvents:
    
    def __init__(self, fha, fhb):
        self.a = auditLog.AuditLog(fha)
        self.b = ballotImage.BallotImage(fhb)

    """
    This function checks for machines that have an early shutdown event between 7am and 7pm.  The early shutdown event has event number 0001628: Warning - terminal closed early.  It returns a map of the format <machine serial number, time of early shutdown event>.
    """
    def getEarlyShutdownTimes(self):
        sdTimeMap = {}
        sdMachineTimeMap = {}
        count = 0
        for x in self.a.getEntryList():
            if x.eventNumber == '0001628':
                s = x.dateTime.split(" ")
                t = s[1].split(":")
                if stri.atoi(t[0]) > 7 and stri.atoi(t[0]) < 19:
                    sdMachineTimeMap[x.serialNumber] = s[1]
                    count = count + 1
                if sdTimeMap.has_key(s[1]):
                    temp = sdTimeMap[s[1]]
                    temp = temp + 1
                    sdTimeMap[s[1]] = temp
                else:
                    sdTimeMap[s[1]] = 1

    def getLowBatteryMachines(self):
        lowBatteryList = []
        for x in self.a.getEntryList():
            if x.eventNumber == '0001635':
                if x.serialNumber not in lowBatteryList:
                    lowBatteryList.append(x.serialNumber)
        return lowBatteryList

    """
    This function gets the events that occurred on the least number of machines.  It only prints the machine serial number and event number for the events that occurred on 1 machine (this can be changed). 
    """
    def getNumMachinesPerEvent(self):
        emMap = {}
        emMap2 = {}
        emList = []
        for x in self.a.getEntryList():
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
                print "Machine %s has 1 occurence of event %s" % (emMap[x3[0]][0], x3[0])

    """
    This function checks the auditLog for the vote cancelled events.  
    """
    def getVoteCancelledEvents(self):
        vcMap = {}
        vcNumMap = {}
        list1513 = []
        list1514 = []
        list1515 = []
        list1516 = []
        list1517 = []
        list1518 = []
        list1519 = []
        minorTicks = (.5,)
        maxNumOccurrences = 0
        vcEvents = ['0001513', '0001514', '0001515', '0001516', '0001517', '0001518', '0001519']
        for x in self.a.getEntryList():
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
            print "This county experienced no 'vote cancelled' events."
        else:
            for z in vcMap:
                for z2 in vcMap[z]:
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

            fig = plt.figure(figsize=(22,14))
            ax2 = fig.add_axes([0.15, 0.1, .7, .8])

            #plt.hist(list1514, bins=10, range=(0,10), label='0001514')
            n, bins, patches = plt.hist([list1513, list1514, list1515, list1516, list1517, list1518, list1519], bins=maxNumOccurrences+1, range=(0,maxNumOccurrences+1), align='left', label=['0001513: '+self.a.getEventDescription('0001513'),'0001514: '+self.a.getEventDescription('0001514'), '0001515: '+self.a.getEventDescription('0001515'), '0001516: '+self.a.getEventDescription('0001516'), '0001517: '+self.a.getEventDescription('0001517'), '0001518: '+self.a.getEventDescription('0001518'), '0001519: '+self.a.getEventDescription('0001519')])
            
            for b in bins:
                minorTicks += ((b-.5),)
            ax2.set_xticks(minorTicks, minor=True)
            ax2.grid(b=True, which='minor')
		    ax2.set_xlabel('# of Occurrences')
		    ax2.set_ylabel('# of Machines')
		    ax2.set_title('Frequency of Vote Cancelled Events')
            ax2.legend()
                
                    
    """
    This function checks the auditLog for the warning events.  
    """
    def getWarningEvents(self):
        wMap = {}
        wNumMap = {}
        list1628 = []
        list1651 = []
        list1703 = []
        list1704 = []
        minorTicks = (.5,)
        maxNumOccurrences = 0        
        wEvents = ['0001628', '0001651', '0001703', '0001704']
        for x in self.a.getEntryList():
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
            print "This county experienced no 'Warning' events."
        else:
            for z in wMap:
                for z2 in wMap[z]:
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

            fig = plt.figure(figsize=(22,14))
            ax2 = fig.add_axes([0.15, 0.1, .7, .8])

            n, bins, patches = plt.hist([list1628, list1651, list1703, list1704], bins=maxNumOccurrences+1, range=(0,maxNumOccurrences+1), align='left', label=['0001628', '0001651', '0001703', '0001704'])
        
            for b in bins:
                minorTicks += ((b-.5),)
            ax2.set_xticks(minorTicks, minor=True)
            ax2.grid(b=True, which='minor')
		    ax2.set_xlabel('# of Occurrences')
		    ax2.set_ylabel('# of Machines')
		    ax2.set_title('Frequency of Warning Events')
            ax2.legend()                     

    """
    This function checks the auditLog for a specific list of events.  It returns a map in the format <machine serial number, <event number, # of instances of this event>>.  
    """
    def getAnomalousEvents(self):
        eventOccurrencesMap = {}
        anomalousEventsMap = {}
        meMap = {}
        badEvents = ['0001635', '0001634', '0001206', '0001625']
        for x in self.a.getEntryList():
            if x.eventNumber in badEvents:
                if meMap.has_key(x.serialNumber):
                    if meMap[x.serialNumber].has_key(x.eventNumber):
                        temp = meMap[x.serialNumber][x.eventNumber]
                        temp = temp + 1
                        meMap[x.serialNumber][x.eventNumber] = temp
                    else:
                        meMap[x.serialNumber][x.eventNumber] = 1
                else:
                    tMap = {}
                    tMap[x.eventNumber] = 1
                    meMap[x.serialNumber] = tMap
            if eventOccurrencesMap.has_key(x.eventNumber) and x.eventNumber != '0001510':
                temp = eventOccurrencesMap[x.eventNumber]
                temp = temp + 1
                eventOccurrencesMap[x.eventNumber] = temp
            elif x.eventNumber != '0001510':
                eventOccurrencesMap[x.eventNumber] = 1
        #for me in meMap:
            #print "There may be a problem with machine %s because it exhibited the following behavior:\n" % (me, )
            #for me2 in meMap[me]:
                #print "%d instances of event %s" % (meMap[me][me2], me2)
            #print "\n"
        return meMap
