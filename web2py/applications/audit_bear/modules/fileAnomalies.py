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
            #print isUploadedAll(aLog, bLog, eLog)[1]
            if len(checkMachines(aLog, bLog, eLog)) != 0 or len(checkMachines2(aLog, bLog, eLog)) != 0:
                #r.addTextBox("The votes match, but the machines don't match.")
                r.addTextBox(" ")
            #r.addTextBox("There aren't any file discrepancies!")
            r.addTextBox("No problems found.")
            r.addTextBox(" ")
        else:
            PEBmachineMap = getPEBmachines(aLog, bLog, eLog)
            PEBprecinctMap = getPrecinctPEBs(aLog, bLog, eLog)
            PEBs = getPEBs(aLog, bLog, eLog)
            #this must mean that provisional vote(s) were rejected
            if len(checkMachines(aLog, bLog, eLog)) == 0 and len(checkMachines2(aLog, bLog, eLog)) == 0:
                #print "----------------------------Rejected Provisional Vote(s)-------------------------------"
                r.addTextBox("\nThere may be %d rejected provisional votes." % (getTotalVotes(aLog, bLog, eLog) - getPrecinctVotes(aLog, bLog, eLog),))

            #machines in ballot images and not in event log
            elif len(checkMachines(aLog, bLog, eLog)) == 0:
                b = True
                for x in checkMachines2(aLog, bLog, eLog):
                    if b == True:
                        r.addTextBox(" ")
                        r.addTextBox("The following machines were in the ballot images, but not in the event log:")
                        b = False
                    r.addTextBox(x)
                PEBmap = getPEBs(aLog, bLog, eLog)
                #check electionID
                if checkIDs(aLog, bLog, eLog) == True:
                    #print 'good'
                    pass
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
#                b3 = True
#                for x in isUploadedAll(aLog, bLog, eLog)[1]:
#                    if b3 == True:
#                        r.addTextBox(" ")
#                        r.addTextBox("\nThe following PEBs were not uploaded:")
#                        b3 = False
#                    r.addTextBox("PEB %s closed machine(s) %s and was not uploaded" % (x, PEBmachineMap[x]))
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
                    r.addTextBox(x)
                PEBmap = getPEBs(aLog, bLog, eLog)
                #check electionID
                if checkIDs(aLog, bLog, eLog) == True:
                    #print "The electionIDs match."
                    pass
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
#                b3 = True
#                for x in isUploadedAll(aLog, bLog, eLog)[1]:
#                    if b3 == True:
#                        r.addTextBox(" ")
#                        r.addTextBox("\nThe following PEBs were not uploaded:")
#                        b3 = False
#                    r.addTextBox("PEB %s closed machine(s) %s and was not uploaded" % (x, PEBmachineMap[x]))
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
                    #print "good"
                    pass
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
#                b3 = True
#                for x in isUploadedAll(aLog, bLog, eLog)[1]:
#                    if b3 == True:
#                        r.addTextBox(" ")
#                        r.addTextBox("\nThe following PEBs were not uploaded:")
#                        b3 = False
#                    r.addTextBox("PEB %s closed machine(s) %s and was not uploaded" % (x, PEBmachineMap[x]))
                #check if votes match up (w/ uncounted machines included)
                if checkVotes(aLog, bLog, eLog) == False:
                    r.addTextBox(" ")
                    r.addTextBox("The votes and ballots would not match up even if the uncounted machines were included.")
        return r

def pebActivateBallot(data, ballot, el, dc, r):
    r.addTitle('Polling locations where ballots were activated with a master PEB')
    #ballotTable = report.Table()
    mPEBmap = getPEBs(data, ballot, el, dc)
    #printedList = []
    b = True
    for x in data.getEntryList():
        s = x.dateTime.split(" ")
        date = s[0]
        if len(mPEBmap[x.serialNumber]) > 1:
            if (x.eventNumber == '0001510' or x.eventNumber == '0001511') and (x.PEBNumber == mPEBmap[x.serialNumber][0] or x.PEBNumber == mPEBmap[x.serialNumber][1]) and (date == dc.eday):
                if ballot.machinePrecinctNameMap.has_key(x.serialNumber):
                    if b == True:
                        r.addTextBox("Ballots have been activated by a master PEB on the following machines.")
                        r.addTextBox(" ")
                        b = False
                    if ballot.machinePrecinctNumMap[x.serialNumber] not in printedList:
                        r.addTextBox("Ballots were activated with a master PEB in %s (#%s)." % (ballot.machinePrecinctNameMap[x.serialNumber], ballot.machinePrecinctNumMap[x.serialNumber]))
                        #ballotTable.addRow(["In %s (#%s), " % (ballot.machinePrecinctNameMap[x.serialNumber], ballot.machinePrecinctNumMap[x.serialNumber]), "ballots were activated with a master PEB."])
                        printedList.append(ballot.machinePrecinctNumMap[x.serialNumber])
    if b == True:
        r.addTextBox("No problems found.")
    #else:
    #    r.addTable(ballotTable)
    return r

def notClosedMachines(aLog, bLog, eLog, dc, r):
    r.addTitle("Machines that weren't closed")
    PEBs = getPEBs(aLog, bLog, eLog, dc)
    PEBlist = []
    b = True
    for x in PEBs:
        if len(PEBs[x]) < 2:
            PEBlist.append((bLog.machinePrecinctNumMap[x], bLog.machinePrecinctNameMap[x], x))
    PEBlist.sort()
    for y in PEBlist:
        if b == True:
            r.setWarningIcon(True)
            r.addTextBox("The following machines were not closed.  This means that their vote data was not uploaded and may not have been included in the count.")
            r.addTextBox(" ")
            b = False
        r.addTextBox("In %s (#%s), machine %s was not closed." % (y[1], y[0], y[2]))
    if b == True:
        #r.addTextBox("All machines were closed.")
        r.addTextBox("No problems found.")
    elif b == False:
        r.addTextBox(" ")
        r.addTextBox("We recommend that you consider finding these voting machines, collect their compact flash drives and vote totals, upload the data, and update the final vote tallies.  We recommend that you gather the summary tapes for all machines in this polling location, including the ones identified above, and make sure that all votes listed there have been included in the final vote tallies.")
    return r
    

def notUploadedPEBs(aLog, bLog, eLog, dc, r):
    r.addTitle("Votes that were not uploaded")
    b3 = True
    if len(isUploadedAll(aLog, bLog, eLog, dc)[1]) < 1:
        r.addTextBox('No problems found.')
    else:
        PEBmachineMap = getPEBmachines(aLog, bLog, eLog, dc)
        PEBmachineList = []
        for x in isUploadedAll(aLog, bLog, eLog, dc)[1]:
            precinctName = ''
            precinctNum = ''
            PEBvotes = 0
            mString = ''
            mString2 = ''
            b32 = True
            for machine in PEBmachineMap[x]:
                if b32 == True:
                    mString = machine
                    b32 = False
                else:
                    mString += ', '+machine
                if getVotesPerMachine(aLog, bLog, eLog).has_key(machine):
                    PEBvotes = PEBvotes + getVotesPerMachine(aLog, bLog, eLog)[machine]
                else:
                    continue
                if bLog.machinePrecinctNameMap.has_key(machine):
                    precinctName = bLog.machinePrecinctNameMap[machine]
                    precinctNum = bLog.machinePrecinctNumMap[machine]
                elif machine in bLog.earlyVotingList:
                    precinctName = 'Absentee'
                    precinctNum = '750'
                elif machine in bLog.failsafeList:
                    precinctName = 'Failsafe'
                    precinctNum = '850'
            if len(PEBmachineMap[x]) > 1:
                mString2 = 'machines'
            else: 
                mString2 = 'machine'
            if precinctNum == '' or precinctNum == '750' or precinctNum == '850':
                continue
            else:
                PEBmachineList.append((precinctNum, precinctName, x, mString2, mString, PEBvotes))
        PEBmachineList.sort()
        if len(PEBmachineList) < 1:
            r.addTextBox("No problems found.")
        for p in PEBmachineList:
            if p[5] != 0:
                if b3 == True:
                    r.setWarningIcon(True)
                    r.addTextBox(" ")
                    r.addTextBox("The following PEBs were not uploaded:")
                    r.addTextBox(" ")
                    b3 = False
                r.addTextBox("--In %s (#%s), PEB %s closed %s %s and were not uploaded.  The %d vote(s) on this PEB may not have been included in the certified count.  " % (p[1], p[0], p[2], p[3], p[4], p[5]))
    if b3 == False:
        r.addTextBox(" ")
        r.addTextBox("We recommend that you consider finding these PEB(s), upload them, and update the final vote tallies.  We recommend that you gather the summary tapes for all machines in this polling location, including the ones identified above, and make sure that all votes listed there have been included in the final vote tallies.")
    return r 

def mismatchVotesMachines(data, ballot, el, r):
    r.addTitle("Machines whose vote count differed between files")
    mismatchTable = report.Table()
    #r.addTextBox("The following machines were only in the event log: ")
    #for a in checkMachines(data, ballot, el):
    #    if not getVotesPerMachine(data, ballot, el).has_key(a):
    #        r.addTextBox("Machine %s had no votes on it according to the event log." % (a,))
    #    else:
    #        r.addTextBox("Machine %s had %d votes according to the event log." % (a, getVotesPerMachine(data, ballot, el)[a]))
    #r.addTextBox(" ")
    #r.addTextBox("The following machines were only in the ballot images: ")
    #for b in checkMachines2(data, ballot, el):
    #    if not ballot.machineVotesMap.has_key(b):
    #        r.addTextBox("Machine %s had no votes on it according to the ballot images." % (b,))
    #    else:
    #        r.addTextBox("Machine %s has %d votes according to the ballot images." % (b, ballot.machineVotesMap[b]))
    
    
    #for x in checkMachines(data, ballot, el):
    #    eVotes = 0
    #    bVotes = 0
    #    if getVotesPerMachine(data, ballot, el).has_key(x):
    #        eVotes = getVotesPerMachine(data, ballot, el)[x]
    #    if ballot.machineVotesMap.has_key(x):
    #        bVotes = ballot.machineVotesMap[x]
    #    mismatchTable.addRow(["%s" % (x,), "%s" % (eVotes,), "%s" % (bVotes,)])
    #for y in checkMachines2(data, ballot, el):
    #    if y in ballot.earlyVotingList or y in ballot.failsafeList:
    #        continue
    #    else:
    #        eVotes = 0
    #        bVotes = 0
    #        if getVotesPerMachine(data, ballot, el).has_key(y):
    #            eVotes = getVotesPerMachine(data, ballot, el)[y]
    #        if ballot.machineVotesMap.has_key(y):
    #            bVotes = ballot.machineVotesMap[y]
    #        mismatchTable.addRow(["%s" % (y,), "%s" % (eVotes,), "%s" % (bVotes,)])
    machineVotes = checkMachineVotes(data, ballot, el)
    b = True
    for z in machineVotes:
        if machineVotes[z][0] != machineVotes[z][1]:
            if b == True:
                r.addTextBox("The following machines appear to have inconsistencies across the audit data.  We recommend that you gather vote data from the following machines, upload it, and update the audit data.")
                r.addTextBox(" ")
                mismatchTable.addHeader("Machine Serial #")
                mismatchTable.addHeader("Votes according to event log")
                mismatchTable.addHeader("Votes according to ballot images")
                b = False
            mismatchTable.addRow(["%s" % (z,), "%s" % (machineVotes[z][0],), "%s" % (machineVotes[z][1],)])
    if b == True:
        r.addTextBox("No problems found.")
    else:
        r.addTable(mismatchTable)
    return r
    
def machineOpenCloseDiff(data, ballot, el, dc, r):
    r.addTitle("Machines opened and closed with different PEBs")
    diffTable = report.Table()
    PEBmap = getPEBs(data, ballot, el, dc)
    PEBlist = []
    b = True
    for p in PEBmap:
        if ballot.machinePrecinctNumMap.has_key(p):
            PEBlist.append((ballot.machinePrecinctNumMap[p], ballot.machinePrecinctNameMap[p], p, PEBmap[p]))
    PEBlist.sort()
    for p in PEBlist:
        if len(p[3]) == 2:
            if (p[3][0] != p[3][1]):
                if b == True:
                    r.addTextBox("The following machines were opened and closed with different PEBs.  You may wish to verify that the closing PEB data was uploaded.  ")
                    r.addTextBox(" ")
                    b = False
                #r.addTextBox("In %s (#%s), machine %s was opened with PEB %s and closed with PEB %s. " % (ballot.machinePrecinctNameMap[p], ballot.machinePrecinctNumMap[p], p, PEBmap[p][0], PEBmap[p][1]))
                diffTable.addRow(["In %s (#%s), " % (p[1], p[0]), " machine %s was opened with PEB %s and closed with PEB %s." % (p[2], p[3][0], p[3][1])])
    if b == True:
        r.addTextBox("No problems found.")  
    else:
        r.addTable(diffTable)       
    return r

def checkIDs(a, b, e):
        #print b.electionID
        #print a.electionID
        return b.electionID == a.electionID
        
def checkVotes(a, b, e, dc):
        votesOnBadMachines = 0
        for machine in checkMachines(a, b, e, dc):
            votesOnBadMachines = votesOnBadMachines + getVotesPerMachine(a, b, e)[machine]
        votesOnBadMachines2 = 0
        votesOnBadMachines2 = getTotalVotes(a, b, e) - getPrecinctVotes(a, b, e)
        return votesOnBadMachines == votesOnBadMachines2
        
"""
Creates a map of <machine, (opening PEB#, closing PEB#)>
"""
def getPEBs(a, b, e, dc):
        machinePEBMap = {}
        for x in a.getEntryList():
            if machinePEBMap.has_key(x.serialNumber):
                date = x.dateTime.split(" ")[0]
                if x.eventNumber == '0001672' and (date == dc.eday):
                    if len(machinePEBMap[x.serialNumber]) == 1:
                        machinePEBMap[x.serialNumber] = [x.PEBNumber]
                    if len(machinePEBMap[x.serialNumber]) == 2:
                        #print "This shouldn't be happening"
                        pass
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
                   #print "Does this machine have an opening state?"
                   pass
        return machinePEBMap
        
def getPEBmachines(a, b, e, dc):
        machinePEBmap = getPEBs(a, b, e, dc)
        PEBmachineMap = {}
        for m in machinePEBmap:
            if len(machinePEBmap[m]) < 2:
                #print "ONLY 1 PEB USED"
                pass
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
def getPrecinctPEBs(a, b, e, dc):
        PEBprecinctMap = {}
        machinePEBMap = getPEBs(a, b, e, dc)
        for x in machinePEBMap:
            if b.machinePrecinctNumMap.has_key(x):
                if PEBprecinctMap.has_key(machinePEBMap[x][0]):
                    if PEBprecinctMap[machinePEBMap[x][0]] != b.machinePrecinctNumMap[x]:
                        #print "PROBLEM" 
                        pass
                else:
                    PEBprecinctMap[machinePEBMap[x][0]] = b.machinePrecinctNumMap[x]
            else:
                #print "Machine %s is not in the ballot images file." % (x,)
                pass
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
        
def isUploadedAll(a, b, e, dc):
        uploadedPEBs = e.getUploadedPEBs()
        #print "UPLOADEDPEBS"
        #print uploadedPEBs
        eventPEBs = getPEBs(a, b, e, dc)
        #print "EVENTPEBS"
        #print eventPEBs
        notUploaded = []
        notUploadedPEBs = []
        for x in eventPEBs:
            if len(eventPEBs[x]) < 2:
                #print "1 PEB"
                pass
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
def checkMachines(a, b, e, dc):
        notCountedList = []
        for x in a.getEntryList():
            s = x.dateTime.split(" ")
            date = s[0]
            if x.serialNumber not in b.machinePrecinctNumMap and (x.eventNumber == '0001510' or x.eventNumber == '0001511') and (date == dc.eday):
                if x.serialNumber not in b.failsafeList and (x.eventNumber == '0001510' or x.eventNumber == '00015110'):
                    if x.serialNumber not in b.earlyVotingList and (x.eventNumber == '0001510' or x.eventNumber == '0001511'):
                        if x.serialNumber not in notCountedList:
                            notCountedList.append(x.serialNumber)
        return notCountedList

"""
This function creates a map of the format <machine, (# of votes according to event log, # of votes according to ballot images)>.
"""
def checkMachineVotes(a, b, e):
    voteMap = {}
    for machine1 in getVotesPerMachine(a, b, e):
        if machine1 in b.earlyVotingList or machine1 in b.failsafeList:
            continue
        else:
            if voteMap.has_key(machine1):
                continue
            else:
                if b.machineVotesMap.has_key(machine1):
                    voteMap[machine1] = (getVotesPerMachine(a, b, e)[machine1], b.machineVotesMap[machine1])
                else:
                    voteMap[machine1] = (getVotesPerMachine(a, b, e)[machine1], 0)
    for machine2 in b.machineVotesMap:
        if machine2 in b.earlyVotingList or machine2 in b.failsafeList:
            continue
        else:
            if voteMap.has_key(machine2):
                continue
            else:
                if getVotesPerMachine(a, b, e).has_key(machine2):
                    votemap[machine2] = (getVotesPerMachine(a, b, e)[machine2], b.machineVotesMap[machine2])
                else:
                    voteMap[machine2] = (0, b.machineVotesMap[machine2])
    return voteMap
      
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
