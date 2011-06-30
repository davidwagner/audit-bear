import re
import dateutil.parser
from collections import deque

class EL68AEntry:
    # an entry will contain only some of the information, others will be none
    date = actionString = countedInfoString = precinct = bals = tot = \
    auditedMachine = pebRetrieved = None
    isError289 = False

    def __init__(self, electionDate, dateString, sysString):
        dateString += str(electionDate.year)
        self.date = dateutil.parser.parse(dateString)
        sysString = sysString.strip()
        r = re.search(r"PRC\s+(\d+)", sysString)

        if r: # every counted information string starts with PRC
            self.countedInfoString = sysString
            self.precinct = r.group(1)
            r = re.search(r"BALS=(\d+)\s+TOT=(\d+)", sysString)
            if r:
                self.bals = int(r.group(1))
                self.tot = int(r.group(2))
        else: # there is either a sysAction string or counted info string
            self.actionString = sysString
            r = re.search(r"V(\d+)\.SPV created", self.actionString, re.IGNORECASE)
            if r:
                self.auditedMachine = r.group(1)
            else:
                r = re.search(r"PEB votes retrieved for P0(\d+)", self.actionString, re.IGNORECASE)
                if r:
                    self.pebRetrieved = r.group(1)
        self.checkError(sysString) # set attribute if error INCOMPLETE

    def checkError(self, s):
        r = re.match(r"0289.*(Reply was: Don't update)", s, re.IGNORECASE)
        if r:
            self.isError289 = True

    def __str__(self):
        s = str(self.date)
        if self.actionString:
            s += (' ' + self.actionString)
        if self.countedInfoString:
            s += (' ' + self.countedInfoString)

        return s
    
class EL68A:
    electionDate = ''
    electionID = ''
    runDate = ''
    entryList = []
    pebToPrecinctCountMap = {}
    auditedMachines = []

    def __init__(self, fh):
        # parse election date, run date and election id
        self.electionDate = self.parseElectionDate(fh)
        self.electionID = self.parseElectionID(fh)
        self.runDate = self.parseRunDate(fh)

        # fill up entry lists
        entryPattern = r"(\d{2}-\d{2}\s+?\d{2}:\d{2}\s+?\w{2})(.*)"
        entryRe = re.compile(entryPattern)
        for line in fh:
            r = entryRe.search(line)
            if r:
                # electionDate, date and time, sys action string
                entry = EL68AEntry(self.electionDate, r.group(1), r.group(2))
                self.entryList.append(entry)
            else:
                # TODO check for two line event... not that urgent
                pass

        # all entries are parsed, fill up needed maps, counts, etc.
        retrievedPEBs = deque()
        accumulationStartDate = self.parseAccumulationStartDate()

        for entry in self.entryList:
            if entry.date < accumulationStartDate:
                # disregard everything before the start of actual accumulation
                continue

            # if it has an audited machine, store it
            if entry.auditedMachine:
                if not entry.auditedMachine in self.auditedMachines:
                    self.auditedMachines.append(entry.auditedMachine)
            elif entry.pebRetrieved:
                retrievedPEBs.append(entry.pebRetrieved)
            elif entry.isError289:
                try:
                    retrievedPEBs.popleft()
                except:
                    print "Pop on empty deque, entry = " + str(entry)
            elif entry.tot and entry.precinct and len(retrievedPEBs) > 0:
                # TODO check if there were multiple accesses to this PEB
                self.pebToPrecinctCountMap[retrievedPEBs.popleft()] = (entry.precinct, entry.tot)

    def parseAccumulationStartDate(self):
        lastClearedEntry = None
        for entry in self.entryList:
            if (not entry.actionString) or entry.date < self.electionDate:
                continue

            # look for cleared and start accumulation data afterwards
            r = re.search(r"CLEARED", entry.actionString, re.IGNORECASE)
            if r:
                lastClearedEntry = entry
            else:
                r = re.search(r"START PROCESS PEBS", entry.actionString, re.IGNORECASE)
                if r and lastClearedEntry:
                    return entry.date

        return self.electionDate

    def parseElectionDate(self, fh):
        fh.seek(0)
        electionDatePattern = r"(\w+\s+\d+,\s+\d+)"
        electionDateRe = re.compile(electionDatePattern)

        for line in fh:
            r = electionDateRe.search(line)
            if r:
                return dateutil.parser.parse(r.group(1))

    def parseElectionID(self, fh):
        fh.seek(0)
        electionIDPattern = r"ELECTION\s+ID:\s+(\d+)"
        electionIDRe = re.compile(electionIDPattern, re.IGNORECASE)

        for line in fh:
            r = electionIDRe.search(line)
            if r:
                return r.group(1)

    def parseRunDate(self, fh):
        fh.seek(0)
        runDatePattern = r"RUN\s+DATE:(.*)\s+ELECTION"
        runDateRe = re.compile(runDatePattern, re.IGNORECASE)

        for line in fh:
            r = runDateRe.search(line)
            if r:
                return dateutil.parser.parse(r.group(1))

