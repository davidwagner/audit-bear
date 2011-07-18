# FILE ANOMALIES ANALYSES MODULE
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

def checkFiles(aLog, bLog, eLog, r):
        r.addTitle("File Discrepancies")
        if getTotalVotes(aLog, bLog, eLog) == getPrecinctVotes(aLog, bLog, eLog):
            print isUploadedAll(aLog, bLog, eLog)[1]
            if len(checkMachines(aLog, bLog, eLog)) != 0 or len(checkMachines2(aLog, bLog, eLog)) != 0:
                r.addTextBox("The votes match, but the machines don't match.")
                r.addTextBox(" ")
            r.addTextBox("There aren't any file discrepancies!")
            r.addTextBox(" ")
        else:
            PEBmachineMap = getPEBmachines(aLog, bLog, eLog)
            PEBprecinctMap = getPrecinctPEBs(aLog, bLog, eLog)
            PEBs = getPEBs(aLog, bLog, eLog)
            #this must mean that provisional vote(s) were rejected
            if len(checkMachines(aLog, bLog, eLog)) == 0 and len(checkMachines2(aLog, bLog, eLog)) == 0:
                print "----------------------------Rejected Provisional Vote(s)-------------------------------"
                r.addTextBox("\nThere are %d rejected provisional votes." % (getTotalVotes(aLog, bLog, eLog) - getPrecinctVotes(aLog, bLog, eLog),))

            #machines in ballot images and not in event log
            elif len(checkMachines(aLog, bLog, eLog)) == 0:
                b = True
                for x in checkMachines2(aLog, bLog, eLog):
                    if b == True:
                        r.addTextBox(" ")
                        r.addTextBox("\nThe following machines were in the ballot images, but not in the event log:")
                        b = False
                    r.addTextBox(x)
                PEBmap = getPEBs(aLog, bLog, eLog)
                #check electionID
                if checkIDs(aLog, bLog, eLog) == True:
                    print 'good'
                else:
                    r.addTextBox(" ")
                    r.addTextBox("\nThese files are from different elections")
                #check if any machines weren't closed
                delPEB = None
                delMachine = None
                for x in PEBs:
                    if len(PEBs[x]) < 2:
                        r.addTextBox(" ")
                        r.addTextBox("\nMachine %s was not closed." % (x, ))
                        delMachine = x
                if delMachine != None:
                    del PEBs[delMachine]
                #check for differing open/close PEBs (then cross check this against the non-master PEB analysis)
                b2 = True
                for x in PEBmap:
                    if PEBmap[x][0] != PEBmap[x][0]:
                        if b2 == True:
                            r.addTextBox(" ")
                            r.addTextBox("\nThe following machines were opened and closed with different PEBs:")
                            b2 = False
                        r.addTextBox("Machine %s was opened with PEB %s and closed with PEB %s" % (x, PEBmap[x][0], PEBmap[x][1]))
                    #cross check with non-master PEB list
                #check for uploading
                b3 = True
                print isUploadedAll(aLog, bLog, eLog)[1]
                for x in isUploadedAll(aLog, bLog, eLog)[1]:
                    if b3 == True:
                        r.addTextBox(" ")
                        r.addTextBox("\nThe following PEBs were not uploaded:")
                        b3 = False
                    r.addTextBox("PEB %s closed machine(s) %s and was not uploaded" % (x, PEBmachineMap[x]))
                #check if votes match up (w/ uncounted machines included)
                if checkVotes(aLog, bLog, eLog) == False:
                    r.addTextBox(" ")
                    r.addTextBox("\nThe votes and ballots would not match up even if the uncounted machines were included.")

            #machines in event log and not in ballot images
            elif len(checkMachines2(aLog, bLog, eLog)) == 0:
                b = True
                for x in checkMachines(aLog, bLog, eLog):
                    if b == True:
                        r.addTextBox(" ")
                        r.addTextBox("The following machines were in the event log, but not in the ballot images:")
                        b = False
                    print x
                PEBmap = getPEBs(aLog, bLog, eLog)
                #check electionID
                if checkIDs(aLog, bLog, eLog) == True:
                    print "The electionIDs match."
                else:
                    r.addTextBox(" ")
                    r.addTextBox("These files are from different elections")
                #check if any machines weren't closed
                delPEB = None
                delMachine = None
                for x in PEBs:
                    if len(PEBs[x]) < 2:
                        r.addTextBox(" ")
                        r.addTextBox("Machine %s was not closed." % (x, ))
                        delMachine = x
                        for x2 in PEBmachineMap:
                            if PEBmachineMap[x2] == x:
                                delPEB = x2
                if delPEB != None:
                    del PEBmachineMap[delPEB]
                    del PEBprecinctMap[delPEB]
                if delMachine != None:
                    del PEBs[delMachine]
                #check for differing open/close PEBs (then cross check this against the non-master PEB analysis)
                b2 = True
                for x in PEBmap:
                    if PEBmap[x][0] != PEBmap[x][0]:
                        if b2 == True:
                            r.addTextBox(" ")
                            r.addTextBox("\nThe following machines were opened and closed with different PEBs:")
                            b2 = False
                        r.addTextBox("Machine %s was opened with PEB %s and closed with PEB %s" % (x, PEBmap[x][0], PEBmap[x][1]))
                    #cross check with non-master PEB list
                #check for uploading
                b3 = True
                print isUploadedAll(aLog, bLog, eLog)[1]
                for x in isUploadedAll(aLog, bLog, eLog)[1]:
                    if b3 == True:
                        r.addTextBox(" ")
                        r.addTextBox("\nThe following PEBs were not uploaded:")
                        b3 = False
                    r.addTextBox("PEB %s closed machine(s) %s and was not uploaded" % (x, PEBmachineMap[x]))
                #check if votes match up (w/ uncounted machines included)
                if checkVotes(aLog, bLog, eLog) == False:
                    r.addTextBox(" ")
                    r.addTextBox("The votes and ballots would not match up even if the uncounted machines were included.")

            #machines in event log and not in ballot images and machines in ballot images and not in event log
            else:
                b = True
                for x in checkMachines(aLog, bLog, eLog):
                    if b == True:
                        r.addTextBox(" ")
                        r.addTextBox("The following machines were in the ballot images, but not in the event log:")
                        b = False
                    r.addTextBox(x)
                b = True
                for x in checkMachines2(aLog, bLog, eLog):
                    if b == True:
                        r.addTextBox(" ")
                        r.addTextBox("The following machines were in the event log, but not in the ballot images:")
                        b = False
                    r.addTextBox(x)
                PEBmap = getPEBs(aLog, bLog, eLog)
                #check electionID
                if checkIDs(aLog, bLog, eLog) == True:
                    print "good"
                else:
                    r.addTextBox(" ")
                    r.addTextBox("These files are from different elections")
                #check if any machines weren't closed
                delPEB = None
                delMachine = None
                for x in PEBs:
                    if len(PEBs[x]) < 2:
                        r.addTextBox(" ")
                        r.addTextBox("Machine %s was not closed." % (x, ))
                        delMachine = x
                        for x2 in PEBmachineMap:
                            if PEBmachineMap[x2] == x:
                                delPEB = x2
                if delPEB != None:
                    del PEBmachineMap[delPEB]
                    del PEBprecinctMap[delPEB]
                if delMachine != None:
                    del PEBs[delMachine]
                #check for differing open/close PEBs (then cross check this against the non-master PEB analysis)
                b2 = True
                for x in PEBmap:
                    if PEBmap[x][0] != PEBmap[x][0]:
                        if b2 == True:
                            r.addTextBox(" ")
                            r.addTextBox("\nThe following machines were opened and closed with different PEBs:")
                            b2 = False
                        r.addTextBox("Machine %s was opened with PEB %s and closed with PEB %s" % (x, PEBmap[x][0], PEBmap[x][1]))
                    #cross check with non-master PEB list
                #check for uploading
                b3 = True
                print isUploadedAll(aLog, bLog, eLog)[1]
                for x in isUploadedAll(aLog, bLog, eLog)[1]:
                    if b3 == True:
                        r.addTextBox(" ")
                        r.addTextBox("\nThe following PEBs were not uploaded:")
                        b3 = False
                    r.addTextBox("PEB %s closed machine(s) %s and was not uploaded" % (x, PEBmachineMap[x]))
                #check if votes match up (w/ uncounted machines included)
                if checkVotes(aLog, bLog, eLog) == False:
                    r.addTextBox(" ")
                    r.addTextBox("The votes and ballots would not match up even if the uncounted machines were included.")
        return r

def notUploadedPEBs(aLog, bLog, eLog, r):
    if len(isUploadedAll(aLog, bLog, eLog)) < 1:
        r.addTextBox('All appropriate PEBs were uploaded.')
    else:
        PEBmachineMap = getPEBmachines(aLog, bLog, eLog)
        b3 = True
        print "NOTUPLOADEDPEBS"
        print isUploadedAll(aLog, bLog, eLog)[1]
        for x in isUploadedAll(aLog, bLog, eLog)[1]:
            if b3 == True:
                r.addTextBox(" ")
                r.addTextBox("\nThe following PEBs were not uploaded:")
                b3 = False
            r.addTextBox("-----------------------------") 
    return r 

def checkIDs(a, b, e):
        print b.electionID
        print a.electionID
        return b.electionID == a.electionID
        
def checkVotes(a, b, e):
        votesOnBadMachines = 0
        for machine in checkMachines(a, b, e):
            votesOnBadMachines = votesOnBadMachines + getVotesPerMachine(a, b, e)[machine]
        votesOnBadMachines2 = 0
        votesOnBadMachines2 = getTotalVotes(a, b, e) - getPrecinctVotes(a, b, e)
        print votesOnBadMachines
        print votesOnBadMachines2
        return votesOnBadMachines == votesOnBadMachines2
        
"""
Creates a map of <machine, (opening PEB#, closing PEB#)>
"""
def getPEBs(a, b, e):
        machinePEBMap = {}
        for x in a.getEntryList():
            if machinePEBMap.has_key(x.serialNumber):
                date = x.dateTime.split(" ")[0]
                if x.eventNumber == '0001672' and (date == '11/02/2010' or date == '06/08/2010'):
                    if len(machinePEBMap[x.serialNumber]) == 1:
                        machinePEBMap[x.serialNumber] = [x.PEBNumber]
                    if len(machinePEBMap[x.serialNumber]) == 2:
                        print "This shouldn't be happening"
                elif x.eventNumber == '0001673':
                    if len(machinePEBMap[x.serialNumber]) == 1:
                        machinePEBMap[x.serialNumber] += [x.PEBNumber]
                    if len(machinePEBMap[x.serialNumber]) == 2:
                        temp = machinePEBMap[x.serialNumber]
                        del temp[1]
                        temp += [x.PEBNumber]
                        machinePEBMap[x.serialNumber] = temp
            else:
                if x.eventNumber == '0001672':
                    machinePEBMap[x.serialNumber] = [x.PEBNumber]
                elif x.eventNumber == '0001673':
                   print "Does this machine have an opening state?"
        return machinePEBMap
        
def getPEBmachines(a, b, e):
        machinePEBmap = getPEBs(a, b, e)
        PEBmachineMap = {}
        for m in machinePEBmap:
            if len(machinePEBmap[m]) < 2:
                print "ONLY 1 PEB USED"
            else:
                if PEBmachineMap.has_key(machinePEBmap[m][1]):
                    if PEBmachineMap[machinePEBmap[m][1]] == [m]:
                        continue
                    else:
                        temp = PEBmachineMap[machinePEBmap[m][1]]
                        temp.append(m)
                        PEBmachineMap[machinePEBmap[m][1]] = temp
                else:
                    PEBmachineMap[machinePEBmap[m][1]] = [m]
        return PEBmachineMap
        
"""
Creates a map of <PEB#, Precinct>
"""
def getPrecinctPEBs(a, b, e):
        PEBprecinctMap = {}
        machinePEBMap = getPEBs(a, b, e)
        for x in machinePEBMap:
            if b.machinePrecinctNumMap.has_key(x):
                if PEBprecinctMap.has_key(machinePEBMap[x][0]):
                    if PEBprecinctMap[machinePEBMap[x][0]] != b.machinePrecinctNumMap[x]:
                        print "PROBLEM" 
                else:
                    PEBprecinctMap[machinePEBMap[x][0]] = b.machinePrecinctNumMap[x]
            else:
                print "Machine %s is not in the ballot images file." % (x,)
        return PEBprecinctMap  
        
def getPrecinctVotes(a, b, e):
        votes = 0
        for v in b.precinctVotesMap.values():
            votes = votes + v
        return votes
        
"""
This function returns the number of votes in the audit log (both voter and poll worker votes).
"""
def getTotalVotes(a, b, e):
        count = 0
        for x in a.getEntryList():
            if x.eventNumber == '0001510' or x.eventNumber == '0001511':
                count = count + 1  
        return count
        
def isUploadedAll(a, b, e):
        print "BLABLABLAHEHELOLOL"
        print e
        print e.entryList
        uploadedPEBs = e.getUploadedPEBs()
        print "UPLOADEDPEBS"
        print uploadedPEBs
        eventPEBs = getPEBs(a, b, e)
        print "EVENTPEBS"
        print eventPEBs
        notUploaded = []
        notUploadedPEBs = []
        for x in eventPEBs:
            if len(eventPEBs[x]) < 2:
                print "1 PEB"
            elif eventPEBs[x][1] not in uploadedPEBs:
                if eventPEBs[x][1] not in notUploaded:
                    notUploaded.append((x, eventPEBs[x][1]))
        for x in notUploaded:
            if x[1] not in notUploadedPEBs:
                notUploadedPEBs.append(x[1])
        return (notUploaded, notUploadedPEBs)
        
"""
This function checks if there are any machines listed in the ballot images that are not found in the event log.
"""
def checkMachines2(a, b, e):
        ballotImageMachines = b.machinePrecinctNumMap.keys()
        for x in a.getEntryList():
            if x.serialNumber in ballotImageMachines:
                ballotImageMachines.remove(x.serialNumber)
        return ballotImageMachines
        
"""
This function checks if there are any machines listed in the event log that are not found in the ballot images.
"""
def checkMachines(a, b, e):
        notCountedList = []
        for x in a.getEntryList():
            if x.serialNumber not in b.machinePrecinctNumMap and (x.eventNumber == '0001510' or x.eventNumber == '0001511'):
                if x.serialNumber not in b.failsafeList and (x.eventNumber == '0001510' or x.eventNumber == '00015110'):
                    if x.serialNumber not in b.earlyVotingList and (x.eventNumber == '0001510' or x.eventNumber == '0001511'):
                        if x.serialNumber not in notCountedList:
                            notCountedList.append(x.serialNumber)
        return notCountedList
        
"""
This function returns a map of the number of votes per machine in a county.  Keys: machines    Values: # of votes
"""
def getVotesPerMachine(a, b, e):
        machineToVotes = {}
        for x in a.getEntryList():
            if x.eventNumber == '0001510' or x.eventNumber == '0001511':
                if machineToVotes.has_key(x.serialNumber):
                    temp = machineToVotes[x.serialNumber]
                    temp = temp + 1
                    machineToVotes[x.serialNumber] = temp
                else:
                    machineToVotes[x.serialNumber] = 1
        return machineToVotes
