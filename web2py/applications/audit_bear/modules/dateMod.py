#!/usr/bin/python
"""
-----Date Module-----
-Scope: This module is a collection of related functions that are hopfully useful in dealing with date anomalies and splitting up the main data structure based on Election-Day Voting, Pre-Voting Days, and Other days

-Usage: The "main" function serves as a usage example  You can import this module in any file you might want access to the functions.

    -Class DateMod:  Init this class with an AuditLog object and a path to the 68a file.

    -Variable Names: These can all be accessed once an DateMod object is created.
        pdata: main data structure split into pre-election voting
        edata: events only from election day
        odata: events neither in the pre-voting or election voting

    -Functions: Commented out for the time being

-Note:
    -Currently Creating a DateMod instance will duplicate the data set and this might have to change in the future

------------------------
"""
    

import os, sys
"""
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
"""
import auditLog
import datetime
import dateutil.parser
import ballotImage


class DateMod:
        #These Variables are dependant on a valid path and date parse from the 68a text file
    pdata = [] #AuditLog Object for all Pre-Voting
    edata = [] #AuditLog Object for all Election-Day Voting
    odata = [] #AuditLog Object for all days after election days and > 15 days before
    eday = ''  #Parsed Election Date from 68.lst file 
    pday = ''  #Election Day Minus 15
    
    def __init__(self, data, date):

        if not isinstance(data, auditLog.AuditLog):
            raise Exception('Must pass valid AuditLog object')

        if self.daygrab(data, date): print 'Election Date Retrieved from 68a'
        else: print 'No 68a Supplied or unable to parse. Inferring Election Day...'

        self.pday = self.eday - datetime.timedelta(15)
        self.splitDays(data, self.eday, self.pday)
 
    """
    Gets date from l68a file or returns blank string. Its a little ugly, but it works for now
    TO-DO: Would be more robust with regex but still avoid reading entire file (Sammy!?)
    """
    def daygrab(self, data, date):
        print date
        if not date:
            self.inferEday(data)
            return False
        else:
            self.eday = date.date()
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

    def inferEday(self, data):
        d = {}
        for line in data:
            key = line.dateTime[0:10]
            if key in d:
                d[key] += 1
            else:
                d.update({key: 1}) 

        self.eday = dateutil.parser.parse(max(d.iterkeys(), key=d.get)).date()
        print self.eday
        return
        

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
    #d2 holds votes before Prevoting
    d2 = {}
    #d3 holds unparsible datetimes
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
                if timeset:
                    times.update({temp:(0,start-diff, end, end-start+diff)})
                    print 'Machine:',temp,'adjusted by:', diff, 'from', (end-start)
                else:
                    times.update({temp:(0,start, end, end-start)})

            #Machine Opened and Not Closed
            else: 
                if timeset:
                    times.update({temp:(2, start-diff, end, None)})
                else:
                    times.update({temp:(2, start, end, None)})

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
            
    return times
"""
This function takes the dictionary from timesopen and decides if the datestamp is believeable
"""
def timecheck(times):
    #Catch all machines open more then 12 hours, check for reasonable opening
    valid = {}
    #Machine must be open by this time to be assumed valid if open for 12 hours+
    timeopen = dateutil.parser.parse('07:30:00')
    for k,v in times.iteritems():
        if v[0] == 0:
            if v[3] > datetime.timedelta(hours=12) and v[1] < timeopen:
                valid.update({k:v})
    return valid
"""
Since we are excluding a fair amount of machines (mostly by fact that they were not closed and opened on election day) this will report how many machines we are excluding by polling location. Takes dictionary of machines from timecheck()
"""
def excluded(valid,ballotclass):
    mappy = ballotclass.getMachinesPerPrecinct()
    return mappy
    
    

"""
---Main---
This only executes if you run this file as a script.  This serves more as an example then anything else. I also have a test file under /misc/patrick that has more updated uses of this module.
----------
"""
        
if __name__== "__main__":


    path1 = "/home/patrick/audit-bear/data/anderson/anderson_co_01_14_11_el152.txt"
    path2 = "/home/patrick/audit-bear/data/anderson/anderson_co_03_07_11_el68a.txt"
    path3 = "/home/patrick/audit-bear/data/anderson/anderson_co_01_14_11_el155.txt"
    f = open(path1, 'r')
    data = auditLog.AuditLog(f)
    f.close()

    f = open(path2, 'r')
    dateclass = DateMod(data, f)
    f.close()
    
    f = open(path3, 'r')
    ballotclass = ballotImage.BallotImage(path3)
    f.close()

    d =  timecheck(timeopen(dateclass.edata))
    for k,v in d.iteritems():
        print 'Time open:',v[1], 'For:', v[3]


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

