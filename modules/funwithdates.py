"""
-----Fun With Dates!-----
-Scope: This module is a collection of related functions that are hopfully useful in dealing with date anomalies and splitting up the main data structure based on Election-Day Voting, Pre-Voting Days, and Other days

-Usage: The "main" function serves as a usage example  You can import this module in any file you might want access to the functions.  It requies auditLog.py to have been imported.

    -Class DateMod:  Init this class with an AuditLog object and a path to the 68a file.
    This will duplicate the memory to store the AuditLog, but give you access to the variables below
    

    -Variable Names: These can all be accessed once an DateMod object is created.
        pdata: main data structure split into pre-election voting
        edata: events only from election day
        odata: events neither in the pre-voting or election voting

    -Functions: Commented out for the time being

-TO-DO: I'll update this as we figure out the easiest and most useful ways to share functions

-Note:
    -Currently Creating a DateMod instance will duplicate the data set and this might have to change in the future

------------------------
"""
    

import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import auditLog
import datetime
import dateutil.parser


class DateMod:
        #These Variables are dependant on a valid path and date parse from the 68a text file
    pdata = [] #AuditLog Object for all Pre-Voting
    edata = [] #AuditLog Object for all Election-Day Voting
    odata = [] #AuditLog Object for all days after election days and > 15 days before
    eday = ''  #Parsed Election Date from 68.lst file 
    pday = ''  #Election Day Minus 15
    
    def __init__(self, data, path):

        if not isinstance(data, auditLog.AuditLog):
            raise Exception('Must pass valid AuditLog object')

        if self.daygrab(path):
             self.splitDays(data, self.eday, self.pday)
        else:
            raise Exception('Path to l68a bad or date was not parsed')
 
    """
    Gets date from l68a file or returns blank string. Its a little ugly, but it works for now
    TO-DO: Would be more robust with regex but still avoid reading entire file (Sammy!?)
    """
    def daygrab(self,f):
        line = [f.next() for x in xrange(4)]
        try:
            self.eday = dateutil.parser.parse(' '.join(line[3].split()[0:3])).date()
        except ValueError:
            print 'Could not parse date from 168.lst'
            return False
        else:
            self.pday = self.eday - datetime.timedelta(15)
            return True 
    """
    Creates 3 AuditLog objects based on pdate and edate.
    """
    def splitDays(self, data, eday, pday):
        edata = []
        pdata = []
        odata = []
        daystring = str(eday.month).zfill(2) + '/' + str(eday.day).zfill(2) + '/' + str(eday.year)
    
        for line in data:
            if line.dateTime[0:10] == daystring:
                self.edata.append(line)
            else:
                try: 
                    temp = dateutil.parser.parse(line.dateTime).date()
                except ValueError:
                    self.odata.append(line)
                else:
                    if temp < eday and temp >= pday: self.pdata.append(line)
                    else: self.odata.append(line)
                    
        return True

"""
-Checks for the following day anomolies:
    -Votes before designated pre-voting day
    -Any dates after election day
    -Unparsible datetimes
-Can be passed either a normal full set of data or just the odata

-Trim option: modifies the data set passed (NOT IMPLEMENTED)
    -0: Do not trim
    -1: Trim anomolous days by event
    -2: Trim anomolous days by machine with occurances

"""
def check(odata, eday, pday):

    #Dictionarys to record anomolies.  Use event and day as key, occurances as value
    #d1 holds events after election day
    d1 = {}
    #d2 holds unparsible datetimes
    d2 = {}
    #d3 holds votes before Prevoting
    d3 = {}
 
    for line in odata:
        key = (line.serialNumber, line.dateTime[0:10])
        try:
            cday = dateutil.parser.parse(line.dateTime).date()
        except ValueError:
            #Unparsible Datetime
            if key in d3:
                d3[key] += 1
            else:
                d3.update({key: 1}) 
        else:
            #Past Election Day
            if (cday > eday):
                if key in d1:
                    d1[key] += 1
                else:
                    d1.update({key: 1})
            #Votes before Prevoting Day
            elif (cday < pday) and (line.eventNumber == '0001511' or line.eventNumber == '0001510'):
                if key in d2:
                    d2[key] +=1
                else:
                    d2.update({key:1})
                
    return [d1,d2,d3]
"""
Return Structure: Returns a dictionary as follows:
  {machineID:(code, timeopen, timeclosed, totaltime)}
  {string:(int, datetime, datetime, timedelta)
  timeopen and totaltimeopen are automatically adjusted if date is changed

Codes:
 0 - Machine was opened and closed
 1 - Machine was closed but not open (for pdata: left open from earlyvoting)
     Has None for timeopen and totaltime
 2 - Machine was opened but not closed
     has none for totaltime and timeclosed
 3 - Machine was neither opened or closed
     Has none for all times


Limitations:  Will not handle unparsible dates.  This will work with edata, pdata, or both sets combined.  Will not deal with a machine with multible openings or closings.
"""
def timeopen(edata):
    temp = edata[0].serialNumber
    times = {}
    ostate = False 
    eventseen = False 
    timeset = False
    startset = False
    for line in edata:
        if line.serialNumber != temp:
            #Machine Neither Closed Nor Opened
            if not eventseen:
                times.update({temp:(3, None, None, None)})
                    
                
            #Machine Closed Sucessfully
            elif not ostate:
                times.update({temp:(0,start-diff, end, end-start+diff)})
                print 'Machine:',temp,'adjusted by:', diff, 'from', (end-start)
            #Machine Opened and Not Closed
            else: 
                times.update({temp:(2, start-diff, end, None)})

            temp = line.serialNumber
            eventseen = False
            timeset = False
        if line.eventNumber == '0001672': 
            ostate = 1
            start = dateutil.parser.parse(line.dateTime)
            eventseen = True
        elif line.eventNumber == '0001673':
            eventseen = True
            if ostate == 1:
                ostate  = 0
                end = dateutil.parser.parse(line.dateTime)
            #Machine Closed without an Open
            elif ostate == 0:
                times.update({temp:(1, None, end, None)})

        #If time was adjusted while machine was open, account for that
        elif line.eventNumber == '0000117' and ostate == 1:
            diff = dateutil.parser.parse(line.dateTime)
            startset = True
        elif line.eventNumber == '0001656' and startset:
            diff =  diff - dateutil.parser.parse(line.dateTime)
            timeset = True
            startset = False
        if not timeset: diff = datetime.timedelta(0)
            
    return times



"""
---Main---
This only executes if you run this file as a script.  This serves more as an example then anything else. I also have a test file under /misc/patrick that has more updated uses of this module.
----------
"""
        
if __name__== "__main__":


    path1 = "/home/patrick/documents/data/anderson_co_01_14_11_el152.txt"
    path2 = "/home/patrick/documents/data/anderson_co_03_07_11_el68a.txt"

    f = open(path1, 'r')
    data = auditLog.AuditLog(f)
    f.close()

    print data[0]

    f = open(path2, 'r')
    dateclass = DateMod(data, f)
    f.close()
    print dateclass.eday
    print dateclass.pday

    print 'Election Day:', dateclass.eday
    for x in xrange(10): print dateclass.edata[x] 
    print 'PreVoting Days:',dateclass.pday, '+'
    for x in xrange(10): print dateclass.pdata[x]
    print 'Other Dates:' 
    for x in xrange(10): print dateclass.odata[x]



"""""

#Checks data for any events not in increaseing order by time stamp
def eventsinorder(data):
    events = []
    lastmachine = '0'
    for line in data:
        currenttime = ' '.join(line[3:5])
        if line[0] != lastmachine:
            lastmachine = line[0]
            lasttime = datetime.datetime.min
        try:
            eventtime = dateutil.parser.parse(currenttime)
        except ValueError:
            flag = False
            events.append(line)
        else:
            if (eventtime - lasttime) < datetime.timedelta(0):
                events.append(line)
            lasttime = dateutil.parser.parse(currenttime)

    return events

#Returns list of times of day in minutes for each opening
def datesopened(data): #histogram2
    minutes = [] 
    for line in data:
        if line[5] == '0001672':
            minutes.append(int(line[4][0:2])*60 + int(line[4][3:5]))
    return minutes
"""

