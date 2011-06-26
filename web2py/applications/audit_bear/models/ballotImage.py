class BallotImage:
    def __init__(self, fh=None):    #fh: open el155 file handle
        file = fh
        list = []
        machinePrecinctMap = {}     #<machine serial #, precinct(name+num)>
        machinePrecinctNameMap = {} #<machine serial #, precinct name>
        machinePrecinctNumMap = {}  #<machine serial #, precinct number>
        precinctMap = {}        #<precinct #, precinct name>
        problemMap = {}     
        pCombinedMap = {}       #<precinct (name+num), same location precincts (name+num)> 
        earlyVotingList = []
        failsafeList = []
        currentPrecinct = None
        pCurrentPrecinct = None
        for line in file:
            list.append(line)
        for i,l in enumerate(list):
            s = l.split("  ")
            t = l.split(" ")
            if t[0] == 'RUN':
                if t[32] == 'Absentee' or t[32] == 'Failsafe' or t[32] == 'ABSENTEE' or t[32] == 'FAILSAFE':
                    currentPrecinct = t[32]
                    #break       #stops parsing the file when it reaches absentee and failsafe precincts (they are listed last)
                elif s[13] == '':
                    currentPrecinct = s[14]
                else:
                    currentPrecinct = s[13]
                for x in machinePrecinctMap.values():   #checks for multiple precincts in one location
                    r = x.split(" - ")
                    r2 = currentPrecinct.split(" - ")
                    if r[1]:
                        r = r[1].split(" ")
                        if len(r2) > 1:
                            r2 = r2[1].split(" ")
                            if r[0] in r2[0]:
                                currentPrecinct = x
            if len(s[0]) == 7:
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
                    if machinePrecinctMap[s[0]] != currentPrecinct:     #checks for multiple precincts in one location
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
        for f in problemMap:    #handles precincts that were combined
            pCurrentPrecinct = problemMap[f][0]
            if not pCombinedMap.has_key(pCurrentPrecinct):
                pCombinedMap[pCurrentPrecinct] = []
                for sf in problemMap[f]:
                    pCombinedMap[pCurrentPrecinct] += [sf]
            for f2 in problemMap:
                if pCurrentPrecinct in problemMap[f2]:
                    problemMap[f2] = [pCurrentPrecinct]
                    machinePrecinctMap[f2] = pCurrentPrecinct
        for m in machinePrecinctMap:    #parses name and number for various mappings
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
        self.machinePrecinctNumMap = machinePrecinctNumMap
        self.machinePrecinctNameMap = machinePrecinctNameMap
        self.precinctMap = precinctMap
        self.combinedMap = pCombinedMap
        self.earlyVotingList = earlyVotingList
        self.failsafeList = failsafeList
        
        mpnMap = self.machinePrecinctNumMap
        machinesPerPrecinct = {}
        for x in mpnMap:        #creates a new map: <precinct #, list of machine serial #s>
            if machinesPerPrecinct.has_key(mpnMap[x]):
                machinesPerPrecinct[mpnMap[x]] += [x]
            else:
                machinesPerPrecinct[mpnMap[x]] = [x]
        self.machinesPerPrecinct = machinesPerPrecinct
    
    def getPrecinctNumMap(self):
        return self.machinePrecinctNumMap   #<machine serial #, precinct #>

    def getPrecinctNameMap(self):
        return self.machinePrecinctNameMap  #<machine serial #, precinct name>

    def getPrecinctMap(self):
        return self.precinctMap         #<precinct #, precinct name>

    def getCombinedMap(self):
        return self.combinedMap         #<precinct (name+num), same location precincts (name+num)> 

    def getMachinesPerPrecinct(self):
        return self.machinesPerPrecinct

    def getEarlyVotingList(self):
        return self.earlyVotingList

    def getFailsafeList(self):
        return self.failsafeList
