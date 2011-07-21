import string as stri

class BallotImage:

    def __del__(self):
        del self.electionID
        del self.machinePrecinctNumMap
        del self.problemMap
        del self.machinePrecinctNameMap
        del self.precinctMap
        del self.combinedMap
        del self.earlyVotingList
        del self.failsafeList
        del self.machineVotesMap
        del self.precinctVotesMap
        del self.newNameList
        del self.machinesPerPrecinct
        

    """
    First constructor in the case that the el68a is not available.  Parses the ballot images and creates the datastructure(s).  The argument passed to this constructor is an already opened el155 file.
    """ 
    def __init__(self, fh=None, aLog=None, el68a=None):
        """
        The variables used in creating the data structures.
        """
        file = fh
        list = []
        machinePrecinctMap = {}
        machinePrecinctNameMap = {}
        machinePrecinctNumMap = {}
        precinctMap = {}
        problemMap = {}     
        pCombinedMap = {}
        machineVotesMap = {}
        precinctVotesMap = {}
        voteCount = 0
        earlyVotingList = []
        failsafeList = []
        newNameList = []
        currentPrecinct = None
        pCurrentPrecinct = None
        votes1 = 0
        votes2 = 0
        runDate = ''
        electionID = ''
        """
        Parses the Ballot Images and fills the maps appropriately.
        """
        for l in file:
            s = l.split("  ")
            t = l.split(" ")
            for c in t:
                if c == '*':
                    voteCount = voteCount + 1
            """
            If the first string in the line is 'RUN', then the current precinct is updated.
            """
            if t[0] == 'RUN':
                electionID = t[len(t)-1]
                electionID = electionID.strip()
                if t[32] == 'Absentee' or t[32] == 'Failsafe' or t[32] == 'ABSENTEE' or t[32] == 'FAILSAFE':
                    currentPrecinct = t[32]
                elif s[13] == '':
                    currentPrecinct = s[14]
                else:
                    currentPrecinct = s[13]
                                
            """
            If the first string in the line is 7 characters long and an asterisk is present, then the vote count per machine and per precinct is adjusted accordingly.
            """
            if len(s[0]) == 7:
                if t[5] == '*' or t[4] == '*' or t[3] == '*':
                    if precinctVotesMap.has_key(currentPrecinct):
                        temp = precinctVotesMap[currentPrecinct]
                        temp = temp + 1
                        precinctVotesMap[currentPrecinct] = temp
                    else:
                        precinctVotesMap[currentPrecinct] = 1

                    if machineVotesMap.has_key(s[0]):
                        temp = machineVotesMap[s[0]]
                        temp = temp + 1
                        machineVotesMap[s[0]] = temp
                    else:
                        machineVotesMap[s[0]] = 1
                """
                If the current precinct is Absentee (early voting), then the machine serial number is added to the early voting list.  Else if the current precinct is Failsafe (provisional votes), then the machine serial number is added to the failsafe list.  In any other case (than the ones mentioned), where the first string is still 7 characters long, the machine serial number is put into the correct locations in the maps.
                """
                if currentPrecinct == 'Absentee' or currentPrecinct == 'ABSENTEE':
                    if s[0] in earlyVotingList:
                        continue
                    else:
                        earlyVotingList.append(s[0])
                elif currentPrecinct == 'Failsafe' or currentPrecinct == 'FAILSAFE':
                    if s[0] in failsafeList:
                        continue
                    else:
                        failsafeList.append(s[0])
                elif machinePrecinctMap.has_key(s[0]):
                    if machinePrecinctMap[s[0]] != currentPrecinct: 
                        if problemMap.has_key(s[0]):
                            if currentPrecinct in problemMap[s[0]]:
                                continue
                            else:
                                problemMap[s[0]] += [currentPrecinct]
                            if machinePrecinctMap[s[0]] in problemMap[s[0]]:
                                continue
                            else:
                                problemMap[s[0]] += [machinePrecinctMap[s[0]]]
                        else:
                            problemMap[s[0]] = [currentPrecinct, machinePrecinctMap[s[0]]]
                else:
                    machinePrecinctMap[s[0]] = currentPrecinct
        """
        If there were precincts that were combined, their numbers are combined and they are viewed as a single precinct.
        """
        #for f in problemMap:
        #    pCurrentPrecinct = problemMap[f][0]
        #    if not pCombinedMap.has_key(pCurrentPrecinct):
        #        pCombinedMap[pCurrentPrecinct] = []
        #        for sf in problemMap[f]:
        #            pCombinedMap[pCurrentPrecinct] += [sf]
        #    for f2 in problemMap:
        #        if pCurrentPrecinct in problemMap[f2]:
        #            problemMap[f2] = [pCurrentPrecinct]
        #            machinePrecinctMap[f2] = pCurrentPrecinct
        """
        Parses the name and number of the precincts for the various mappings.
        """
        for m in machinePrecinctMap:
            x = ''
            y = ''
            t = machinePrecinctMap[m]
            t = t.split(" ")
            u = machinePrecinctMap[m]
            u = u.split(" - ")
            u2 = u[0]
            u2 = u2.split(" ")
            if len(u2) > 1:
                y = u2[1]
            else:
                y = u2[0]
            if len(u) > 2:
                x = u[1]+" - "+u[2]
            else:
                x = u[1]
            machinePrecinctNumMap[m] = y
            machinePrecinctNameMap[m] = x
            precinctMap[y] = x     
        """
        Creates the global variables of the maps.
        """ 
        self.electionID = electionID
        self.machinePrecinctNumMap = machinePrecinctNumMap
        self.problemMap = problemMap
        self.machinePrecinctNameMap = machinePrecinctNameMap
        self.precinctMap = precinctMap
        self.combinedMap = pCombinedMap
        self.earlyVotingList = earlyVotingList
        self.failsafeList = failsafeList
        self.machineVotesMap = machineVotesMap
        self.precinctVotesMap = precinctVotesMap
        self.newNameList = newNameList

        machinePEBMap = {}
        for x in aLog.getEntryList():
            if machinePEBMap.has_key(x.serialNumber):
                if x.eventNumber == '0001672':
                    if len(machinePEBMap[x.serialNumber]) == 1:
                        machinePEBMap[x.serialNumber] = [x.PEBNumber]
                    if len(machinePEBMap[x.serialNumber]) == 2:
                        #print "This shouldn't be happening"
                        pass
                elif x.eventNumber == '0001673':
                    if len(machinePEBMap[x.serialNumber]) == 1:
                        if stri.atoi(machinePEBMap[x.serialNumber][0]) != stri.atoi(x.PEBNumber):
                            #print "on machine %s it was %s but now it is %s" % (x.serialNumber, machinePEBMap[x.serialNumber][0], x.PEBNumber)
                            pass
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
                   pass

        PEBprecinctMap = {}
        for x in machinePEBMap:
            if self.machinePrecinctNumMap.has_key(x):
                if PEBprecinctMap.has_key(machinePEBMap[x][0]):
                    if PEBprecinctMap[machinePEBMap[x][0]] != self.machinePrecinctNumMap[x]:
                        #print "PROBLEM WITH PEB: %s because it was found in precinct %s and %s on machine %s" % (machinePEBMap[x][0], PEBprecinctMap[machinePEBMap[x][0]], self.machinePrecinctNumMap[x], x) 
                        pass
                else:
                    PEBprecinctMap[machinePEBMap[x][0]] = self.machinePrecinctNumMap[x]
            else:
                #print "Machine %s is not in the ballot images file." % (x,)
                pass

        list1 = []
        list2 = []
        combineList = []
        #check if all machines that consistently occur in the same multiple precincts are the only ones in those precincts and if they all occur in each precinct
        #for k in self.problemMap:
        #    for k2 in self.problemMap:
        #        if self.problemMap[k] == self.problemMap[k2] and k != k2:
        #            if k not in combineList:
        #                combineList.append(k)
        #            if k2 not in combineList:
        #                combineList.append(k2)

        
        #check if there are subsets in the problemMap
        isSubsetList = []
        isSubsetMachineList = []
        groupedSubsets = []
        for k in self.problemMap:
            for k2 in self.problemMap:
                isSubset = True
                currentIndividualLocation = None
                currentSubset = []
                for k3 in self.problemMap[k]:
                    if k3 in self.problemMap[k2] and k != k2:
                        currentIndividualLocation = self.problemMap[k2][0]
                        currentSubset = self.problemMap[k2]
                        continue
                    elif k3 not in self.problemMap[k2] and k != k2:
                        isSubset = False
                if isSubset == True and k != k2:
                    if k not in isSubsetMachineList:
                        isSubsetMachineList.append(k)
                        isSubsetList.append((k, currentIndividualLocation))
                        if currentSubset not in groupedSubsets:
                            groupedSubsets.append(currentSubset)
           
        for p in problemMap.keys():
            if p in problemMap.keys() and p not in isSubsetMachineList:
                if p not in list2:
                    list2.append((p, problemMap[p]))
        
        for j in isSubsetList:
            del self.problemMap[j[0]]        

        #check if machines in problem map were just used for testing?
        doNotIncludeList = []
        isInFile = False
        onlyInstance = []
        for machine in self.problemMap.keys():
            if el68a != None:
                #check if PEB is uploaded
                for z in el68a.entryList:
                    if z.pebRetrieved == machinePEBMap[machine][0]:
                        continue
                        #yes-check error message (parser does not include this info)
                    else:
                        #no-don't include
                        if machine not in doNotIncludeList:
                            #print "Machine %s was not uploaded" % (machine, )
                            doNotIncludeList.append(machine)
            else:
                for z2 in aLog.getEntryList():
                    date = z2.dateTime.split(" ")[0]
                    if z2.PEBNumber == machinePEBMap[machine][0] and z2.serialNumber != machine and (date == '11/02/2010' and date == '06/08/2010'):
                        isInFile = True
                    elif z2.serialNumber == machine and z2.eventNumber == '0001672' and (date == '11/02/2010' or date == '06/08/2010'):
                        isinFile = True
                        onlyInstance.append(machine)
                        if self.problemMap[machine] not in groupedSubsets:
                            isSubsetList.append((machine, self.problemMap[machine][0]))
                            groupedSubsets.append(self.problemMap[machine])
                    else:
                        continue
                if isInFile == False:
                    if machine not in doNotIncludeList and machine not in onlyInstance:
                        doNotIncludeList.append(machine)

        for machine in doNotIncludeList:
            del self.machinePrecinctNumMap[machine]
            del self.machinePrecinctNameMap[machine]
            del machinePrecinctMap[machine]

        for j in isSubsetList:
            if j[0] in self.problemMap:
                del self.problemMap[j[0]]  

        for sub in isSubsetList:
            machinePrecinctMap[sub[0]] = sub[1]
            x = ''
            y = ''
            t = machinePrecinctMap[sub[0]]
            t = t.split(" ")
            u = machinePrecinctMap[sub[0]]
            u = u.split(" - ")
            u2 = u[0]
            u2 = u2.split(" ")
            if len(u2) > 1:
                y = u2[1]
            else:
                y = u2[0]
            if len(u) > 2:
                x = u[1]+" - "+u[2]
            else:
                x = u[1]
            self.machinePrecinctNumMap[sub[0]] = y
            self.machinePrecinctNameMap[sub[0]] = x
            self.precinctMap[y] = x  

        #print "THE DONOTINCLUDELIST: "
        #print doNotIncludeList

        """
        Counts the number of votes per precinct and votes per machine.
        """
        for v in precinctVotesMap.values():
            votes1 = votes1 + v
        for v2 in machineVotesMap.values():
            votes2 = votes2 + v2

        """
        Creates a map from the other maps.  It is of the format <precinct number, [list of machine serial numbers]>.
        """
        mpnMap = self.machinePrecinctNumMap
        machinesPerPrecinct = {}
        for x in mpnMap:
            if machinesPerPrecinct.has_key(mpnMap[x]):
                machinesPerPrecinct[mpnMap[x]] += [x]
            else:
                machinesPerPrecinct[mpnMap[x]] = [x]
        self.machinesPerPrecinct = machinesPerPrecinct


    """
    Returns the map of the format <machine serial number, precinct number>
    """    
    def getPrecinctNumMap(self):
        return self.machinePrecinctNumMap

    """
    Returns the map of the format <machine serial number, precinct name>
    """
    def getPrecinctNameMap(self):
        return self.machinePrecinctNameMap 

    """
    Returns the map of the format <precinct number, precinct name>
    """
    def getPrecinctMap(self):
        return self.precinctMap 

    """
    Returns the map of the format <precinct name and number, [list of precincts name and number in the same location]>
    """
    def getCombinedMap(self):
        return self.combinedMap

    """
    Returns the map of the format <precinct number, [list of machines]>
    """
    def getMachinesPerPrecinct(self):
        return self.machinesPerPrecinct

    """
    Returns the list of machines used in the Absentee precincts (early voting).
    """
    def getEarlyVotingList(self):
        return self.earlyVotingList

    """
    Returns the list machines used in the Failsafe precincts (provisional votes).
    """
    def getFailsafeList(self):
        return self.failsafeList
