class BallotImage:

    """
    Parses the ballot images and creates the datastructure(s).  The argument passed to this constructor is an already opened el155 file.
    """ 
    def __init__(self, fh=None):
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
        Gets the correct run date and election ID.
        """
        for line in file:
            list.append(line)
        for i,l in enumerate(list):
            s = l.split("  ")
            t = l.split(" ")
            for c in t:
                if c == '*':
                    voteCount = voteCount + 1
            """
            If the first string in the line is 'RUN', then the current precinct is updated.
            """
            if t[0] == 'RUN':

                if t[32] == 'Absentee' or t[32] == 'Failsafe' or t[32] == 'ABSENTEE' or t[32] == 'FAILSAFE':
                    currentPrecinct = t[32]
                elif s[13] == '':
                    currentPrecinct = s[14]
                else:
                    currentPrecinct = s[13]
                #for x in machinePrecinctMap.values():
                #    newName = ''
                #    isSameLocation = False
                #    r = x.split(" - ")
                #    r2 = currentPrecinct.split(" - ")
                #    if r[1]:
                #        r = r[1].split(" ")
                #        if len(r2) > 1:
                #            length = 0
                #            r2 = r2[1].split(" ")
                #            for i,c in enumerate(r):
                #                if i == (len(r)-1):
                #                    continue
                #                elif r[i] == r2[i]:
                #                    newName += r[i]+" "
                #                    length = i
                #                    isSameLocation = True
                #                elif r[i] != r2[i]:
                #                    isSameLocation = False
                #                    break
                #            if isSameLocation == True:
                                #if newName not in newNameList:
                                    #newNameList.append((newName, length))
                                #if pCombinedMap.has_key(currentPrecinct):
                                    #if x not in pCombinedMap[currentPrecinct]:
                                        #pCombinedMap[currentPrecinct] += [x]
                                #else:
                                    #pCombinedMap[currentPrecinct] = [x]
                                #if pCombinedMap.has_key(x):
                                    #if currentPrecinct not in pCombinedMap[x]:
                                        #pCombinedMap[x] += [currentPrecinct]
                                #else:
                                    #pCombinedMap[x] = [currentPrecinct]
                 #               currentPrecinct = x
                                
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
                        print 'HERE'
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

        """
        Counts the number of votes per precinct and votes per machine.
        """
        for v in precinctVotesMap.values():
            votes1 = votes1 + v
        for v2 in machineVotesMap.values():
            votes2 = votes2 + v2

        print votes1
        print votes2
        print voteCount
        #print "the length is %d" % (len(self.machinePrecinctNumMap),)
        #print "the number of precincts is %d" % (len(self.precinctMap),)
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

