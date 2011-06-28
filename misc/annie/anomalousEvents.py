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
        #for m in sdMachineTimeMap:
            #print m, sdMachineTimeMap[m]

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
    This function checks the auditLog for a specific list of events.  It returns a map in the format <machine serial number, <event number, # of instances of this event>>.  
    """
    def getAnomalousEvents(self):
        eventOccurrencesMap = {}
        anomalousEventsMap = {}
        meMap = {}
        mean = 0
        p = 0
        stdev = 0
        badEvents = ['0001518', '0002400', '0001635', '0000712', '0000706', '0001003', '0000713', '0002406', '0002405', '0001302', '0001702', '0001656', '0001655', '0002210', '0001725', '0001634', '0001718', '0001720', '0001721', '0001628', '0001703', '0001704', '0001651', '0001206']
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
        for m in eventOccurrencesMap.values():
            mean = mean + m
        mean = mean/len(eventOccurrencesMap.values())
        for m2 in eventOccurrencesMap.values():
            p = p + ((m2-mean)**2)
        stdev = math.sqrt(p/len(eventOccurrencesMap.values()))
        for e in eventOccurrencesMap:
            if eventOccurrencesMap[e] < (mean-(4*stdev)) or eventOccurrencesMap[e] > ((4*stdev)+mean):
                anomalousEventsMap[e] = eventOccurrencesMap[e]
        #for me in meMap:
            #print "There may be a problem with machine %s because it exhibited the following behavior:\n" % (me, )
            #for me2 in meMap[me]:
                #print "%d instances of event %s" % (meMap[me][me2], me2)
            #print "\n"
        return meMap
