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

class analysis2:
    def __init__(self, fha, fhb):
        self.a = auditLog.AuditLog(fha)
        self.b = ballotImage.BallotImage(fhb)
        print self.b.machinesPerPrecinct

    def getVotesPerMachine(self):
        machineToVotes = {}
        for x in self.a.getEntryList():
            if x.eventNumber == '0001510' or x.eventNumber == '0001511':
                if machineToVotes.has_key(x.serialNumber):
                    temp = machineToVotes[x.serialNumber]
                    temp = temp + 1
                    machineToVotes[x.serialNumber] = temp
                else:
                    machineToVotes[x.serialNumber] = 1
        for y in machineToVotes:
            print y, machineToVotes[y]
        return machineToVotes

    def compareVotesPerMachine(self):
        ballotsPerMachine = self.b.machineVotesMap
        votesPerMachine = self.getVotesPerMachine()
        noBallots = self.checkMachines()
        noVotes = self.checkMachines2()
        print '***************************************************************************************'
        for x in votesPerMachine:
            for y in ballotsPerMachine:
                if x == y:
                    if votesPerMachine[x] != ballotsPerMachine[y]:
                        print "For machine %s, the audit log has recorded %d votes, but the ballot images has recorded %d ballots" % (x, votesPerMachine[x], ballotsPerMachine[x])
                    if y in noVotes:
                        print "For machine %s, the audit log had no record of votes, but the ballot images recorded %d votes" % (y, ballotsPerMachine[y])
            if x in noBallots:
                print "For machine %s, the audit log recorded %d votes, but the ballot images had no record of this machine" % (x, votesPerMachine[x])

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

    def getThroughput(self):
        mpMap = self.b.getMachinesPerPrecinct()
        throughputMap = {}
        locationMap = self.b.machinePrecinctNumMap
        locationMap2 = self.b.getMachinesPerPrecinct()

        for x in self.a.getEntryList():
            d = x.dateTime.split(" ")
            date = d[0]
            time = d[1]
            if date == '11/02/2010':
                if (x.eventNumber == '0001510' and locationMap.has_key(x.serialNumber)) or (x.eventNumber == '0001511' and locationMap.has_key(x.serialNumber)):
                    location = locationMap[x.serialNumber]
                    if throughputMap.has_key(location):
                        s1 = time.split(":")
                        if throughputMap[locationMap[x.serialNumber]].has_key(stri.atoi(s1[0])):
                            temp = throughputMap[locationMap[x.serialNumber]][stri.atoi(s1[0])]
                            temp = temp + 1
                            throughputMap[locationMap[x.serialNumber]][stri.atoi(s1[0])] = temp
                        else:
                            throughputMap[locationMap[x.serialNumber]][stri.atoi(s1[0])] = 1
                    else:
                        s2 = time.split(":")
                        tempMap = {}
                        tempMap[stri.atoi(s2[0])] = 1
                        throughputMap[locationMap[x.serialNumber]] = tempMap
        for y in throughputMap:
            for y2 in throughputMap[y]:
                t = throughputMap[y][y2]
                t = t/len(locationMap2[y])
                throughputMap[y][y2] = t 
        for z in throughputMap:
           print z, throughputMap[z]
        fig = plt.figure(figsize=(22,10))
        ax2 = fig.add_axes([0.1, 0.1, .8, .8])
        matplotlib.pyplot.plot(throughputMap[throughputMap.keys()[15]].keys(), throughputMap[throughputMap.keys()[15]].values())
        ax2.set_xlabel('Time')
        ax2.set_ylabel('# of Votes Per Machine')
        ax2.set_title('Throughput for Precinct %s Every Hour' % (throughputMap.keys()[15],))
        plt.show()

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
        for m in sdMachineTimeMap:
            print m, sdMachineTimeMap[m]

    def getAnomalousEvents(self):
        eventOccurrencesMap = {}
        anomalousEventsMap = {}
        meMap = {}
        mean = 0
        p = 0
        stdev = 0
        badEvents = ['0001518', '0002400', '0001635', '0000712', '0000706', '0001003', '0000713', '0002406', '0002405', '0001302', '0001702', '0001656', '0001655', '0002210', '0001725', '0001634', '0001718', '0001720', '0001721', '0001628', '0001703', '0001704', '0001651']
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
        for me in meMap:
            print "There may be a problem with machine %s because it exhibited the following behavior:\n" % (me, )
            for me2 in meMap[me]:
                print "%d instances of event %s" % (meMap[me][me2], me2)
            print "\n"

    def getTotalVotes(self):
        count = 0
        for x in self.a.getEntryList():
            if x.eventNumber == '0001510' or x.eventNumber == '0001511':
                count = count + 1  
        print count
        return count

    def checkMachines2(self):
        ballotImageMachines = self.b.machinePrecinctNumMap.keys()
        for x in self.a.getEntryList():
            if x.serialNumber in ballotImageMachines:
                ballotImageMachines.remove(x.serialNumber)
        for y in ballotImageMachines:
            print y
        return ballotImageMachines

    def checkMachines(self):
        notCountedList = []
        for x in self.a.getEntryList():
            if x.serialNumber not in self.b.machinePrecinctNumMap and (x.eventNumber == '0001510' or x.eventNumber == '0001511'):
                if x.serialNumber not in self.b.failsafeList and (x.eventNumber == '0001510' or x.eventNumber == '00015110'):
                    if x.serialNumber not in self.b.earlyVotingList and (x.eventNumber == '0001510' or x.eventNumber == '0001511'):
                        if x.serialNumber not in notCountedList:
                            notCountedList.append(x.serialNumber)
        print notCountedList
        return notCountedList
