class CheckFiles:
    
    def __init__(self, fha, fhb):
        self.a = auditLog.AuditLog(fha)
        self.b = ballotImage.BallotImage(fhb)

    """

    """
    def getMachineVotes(self):
        votes = 0
        for v2 in machineVotesMap.values():
            votes = votes + v2
        return votes

    """
    
    """
    def getPrecinctVotes(self):
        votes = 0
        for v in self.b.precinctVotesMap.values():
            votes = votes + v
        return votes

    """
    This function compares electionIDs between the audit log and the ballot images to verify that both files are from the same election.
    """
    def checkElectionIDs(self):
        if a.electionID == b.electionID:
            return true
        else:
            print "The election ID is not the same on all files."
            return False

    """
    This function returns a map of the number of votes per machine in a county.  Keys: machines    Values: # of votes
    """
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
        #for y in machineToVotes:
        #    print y, machineToVotes[y]
        return machineToVotes

    """
    This function compares the number votes on machine x in the event log to the number of votes on the same machine in the ballot images.
    """
    def compareVotesPerMachine(self):
        ballotsPerMachine = self.b.machineVotesMap
        votesPerMachine = self.getVotesPerMachine()
        noBallots = self.checkMachines()
        noVotes = self.checkMachines2()
        #print '***************************************************************************************'
        for x in votesPerMachine:
            for y in ballotsPerMachine:
                if x == y:
                    if votesPerMachine[x] != ballotsPerMachine[y]:
                        print "For machine %s, the audit log has recorded %d votes, but the ballot images has recorded %d ballots" % (x, votesPerMachine[x], ballotsPerMachine[x])
                    if y in noVotes:
                        print "For machine %s, the audit log had no record of votes, but the ballot images recorded %d votes" % (y, ballotsPerMachine[y])
            if x in noBallots:
                print "For machine %s, the audit log recorded %d votes, but the ballot images had no record of this machine" % (x, votesPerMachine[x])

    """
    This function returns the number of votes in the audit log (both voter and poll worker votes).
    """
    def getTotalVotes(self):
        count = 0
        for x in self.a.getEntryList():
            if x.eventNumber == '0001510' or x.eventNumber == '0001511':
                count = count + 1  
        #print count
        return count

    """
    This function checks if there are any machines listed in the ballot images that are not found in the event log.
    """
    def checkMachines2(self):
        ballotImageMachines = self.b.machinePrecinctNumMap.keys()
        for x in self.a.getEntryList():
            if x.serialNumber in ballotImageMachines:
                ballotImageMachines.remove(x.serialNumber)
        for y in ballotImageMachines:
            print y
        return ballotImageMachines

    """
    This function checks if there are any machines listed in the event log that are not found in the ballot images.
    """
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
