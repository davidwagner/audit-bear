#!/usr/bin/python
"""
-----Date Module-----
-Scope: This module is a collection of related functions that are hopfully useful in dealing with date anomalies and splitting up the main data structure based on Election-Day Voting, Pre-Voting Days, and Other days

-Usage: The "main" function serves as a usage example  You can import this module in any file you might want access to the functions.

-Class DateMod:  Init this class with an AuditLog object and a path to the 68a file.
Update:  This file didn't prove as univerally useful as intended.  Updated to take out aspects that were not being used.

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
        
    def __init__(self,data, date):
        #These Variables are dependant on a valid path and date parse from the 68a text file
        self.eday = ''  #Parsed Election Date from 68.lst file 
        self.pday = ''  #Election Day Minus 15


        if not isinstance(data, auditLog.AuditLog):
            raise Exception('Must pass valid AuditLog object')

        if self.daygrab(data, date): print 'Election Date Retrieved from 68a'
        else: print 'No 68a Supplied or unable to parse. Inferring Election Day...'

        self.pday = self.eday - datetime.timedelta(15)

    def __del__(self):
        del self.pday
        del self.eday
 
    """
    Gets date from l68a file or infer eday
    """
    def daygrab(self, data, date):
        print date
        if not date:
            self.inferEday(data)
            return False
        else:
            self.eday = date.date()
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
    Returns information about particulary early voting
    """
    def voteEarly(self,data):
        #Holds machines:# of votes, first vote, last vote
        machines = {}

        for line in data:
            try: cday = dateutil.parser.parse(line.dateTime).date()
            except ValueError: cday = self.eday
        
            if (cday < self.pday) and (line.eventNumber == '0001511' or line.eventNumber == '0001510'):
                if line.serialNumber in machines:
                    v = machines[line.serialNumber]
                    if v[1] > cday: v[1] = cday
                    if v[2] < cday: v[2] = cday
                    machines[line.serialNumber] = [v[0]+1, v[1], v[2]]
                else:
                    machines.update({line.serialNumber:[1,cday,cday]})
        return machines
 
"""
-Checks for the following day anomolies:
    -Votes before designated pre-voting day
    -Any dates after election day
    -Unparsible datetimes
-Can be passed either a normal full set of data or just the odata


"""
def check(data, eday, pday):

    #Dictionarys to record anomolies.  Use event and day as key, occurances as value
    #d1 holds events after election day
    d1 = {}
    #d2 holds votes before Prevoting
    d2 = {}
    #d3 holds unparsible datetimes
    d3 = {}
 
    ostate = False
    temp = data[0].serialNumber

    for line in data:
        if temp != line.serialNumber:
            ostate = False 
        if line.eventNumber == '0001672':
            ostate = True
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
            #Past Election Day and machine has been opened (Not at factory)
            if (cday > eday) and ostate == True:
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
def timeopen(data,eday):
    temp = data[0].serialNumber
    times = {}
    a = []
    ostate = False 
    eventseen = False 
    timeset = False
    startset = False
    for line in data:
        if line.serialNumber != temp:
            #Machine Neither Closed Nor Opened
            if not eventseen:
                times.update({temp:(3, None, None, None)})
                    
                
            #Machine Closed Sucessfully
            elif not ostate:
                if timeset:
                    times.update({temp:(0,start-diff, end, end-start+diff)})
                    a.append((temp, diff))
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
            try: start = dateutil.parser.parse(line.dateTime)
            except ValueError: print 'Value Error line 196'
            else:
                ostate = 1
                eventseen = True
        elif line.eventNumber == '0001673':
            eventseen = True
            if ostate == 1:
                try: end = dateutil.parser.parse(line.dateTime)
                except ValueError: print 'Value Error Line 204'
                else: ostate  = 0
            #Machine Closed without an Open
            elif ostate == 0:
                times.update({temp:(1, None, end, None)})

        #If time was adjusted while machine was open, account for that
        elif line.eventNumber == '0000117' and ostate == 1:
            try:diff = dateutil.parser.parse(line.dateTime)
            except ValueError: pass
            else:
                startset = True
        elif line.eventNumber == '0001656' and startset:
            if diff.date() == eday or dateutil.parser.parse(line.dateTime).date() == eday:

                diff =  diff - dateutil.parser.parse(line.dateTime)
                timeset = True
            startset = False
            
    return times, a


"""
This function takes the dictionary from timesopen and decides if the datestamp is beleavable.  Also tries to determine which machines really don't have the correct date.
Alot of machines are not sorted into valid or invalid.  As this function becomes more robust it will know what to do with more machines.
"""
def timecheck(times):
    #Catch all machines open more then 12 hours, check for reasonable opening
    valid = {}
    invalid = {}
    #Machine must be open by this time to be assumed valid if open for 12 hours+
    timeopen = dateutil.parser.parse('07:30:00')
    for k,v in times.iteritems():
        if v[0] == 0:
            if v[3] > datetime.timedelta(hours=12) and v[1] < timeopen:
                valid.update({k:v})
            else: pass
    return valid

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

    dateclass = DateMod(data, None)
    
    f = open(path3, 'r')
    f6 = open(path2, 'r')
    ballotclass = ballotImage.BallotImage(f, data, f6)
    f.close()
    f6.close()

