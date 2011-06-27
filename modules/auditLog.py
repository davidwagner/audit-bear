# coding: utf8
import re

class AuditLogEntry:
    serialNumber = 0
    PEBNumber = 0
    entryType = ''
    dateTime = ''
    eventNumber = 0
    eventDescription = ''

    def __init__(self, l):
        if len(l) < 6:
            raise Exception('length of given entry list < 6')

        self.serialNumber = l[0]
        self.PEBNumber = l[1]
        self.entryType = l[2]
        self.dateTime = l[3]
        self.eventNumber = l[4]
        self.eventDescription = l[5]
        
    def __str__(self):
        return '' + self.serialNumber + ', ' + self.PEBNumber + ', ' + self.entryType + ', ' + self.dateTime + \
                ', ' + self.eventNumber + ', ' + self.eventDescription

    def __getitem__(self, index):
        return [self.serialNumber, self.PEBNumber, self.entryType, self.dateTime, self.eventNumber, \
            self.eventDescription][index]

class AuditLog:
    runDate = ''
    electionID = ''
    entryList = []

    def parse(self, fh):
        """Parse the given audit log file into a list of entries"""

        linePattern = r"^(\d*?)\s+(\d*?)\s+(\w+?)\s+(\d+?/\d+?/\d+?\s+\d+?:\d+?:\d+?)\s+(\d+?)\s+(.*?)\s+$"
        lineRe = re.compile(linePattern)
        parsed = []
        
        for line in fh:
            r = lineRe.match(line)
            parsedLine = []
            if r:
                for i in range(0, 6):
                    parsedLine.append(r.group(i + 1) if not r.group(i + 1) == '' else lastParsedLine[i])
                parsed.append(AuditLogEntry(parsedLine))
                lastParsedLine = parsedLine
        return parsed

    def parseHeader(self, fh):
        headerPattern = r"^RUN DATE:(.*?)\s+?(.*?)\s+?([APM]{2})\s+?ELECTION ID:\s(\d+?)\s+$"
        headerRe = re.compile(headerPattern, re.IGNORECASE)
        for line in fh:
            r = headerRe.match(line)
            if r:
                return (r.group(1) + ' ' + r.group(2) + ' ' + r.group(3), r.group(4))

        return '0', '0'

    def __init__(self, fh = None):
        # constructor / parser
        if fh != None:
            self.entryList = self.parse(fh)
            fh.seek(0)
            self.runDate, self.electionID = self.parseHeader(fh)

    def __iter__(self):
        #iterator for entries
        return iter(self.entryList)

    def isEmpty(self):
        return len(self.entryList) == 0

    def getEntryList(self):
        return self.entryList

    def getEntry(self, index):
        return self.entryList[index]

    def __getitem__(self, index):
        return self.entryList[index]

    def __len__(self):
        return len(self.entryList)
