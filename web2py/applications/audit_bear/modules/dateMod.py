#!/usr/bin/python
"""
-----Date Module-----
-Scope: This module is a collection of related functions that are hopfully useful in dealing with date anomalies and splitting up the main data structure based on Election-Day Voting, Pre-Voting Days, and Other days

-Usage: The "main" function serves as a usage example  You can import this module in any file you might want access to the functions.

-Class DateMod:  Init this class with an AuditLog object and a path to the 68a file.
Update:  This file didn't prove as univerally useful as intended.  Updated to take out aspects that were not being used.

------------------------
"""
    

import sys
import datetime
import dateutil.parser
import auditLog
import ballotImage

    
class DateMod:
        
    def __init__(self,data, date):
        #Dependant on a valid path and date parse from the 68a text file
        self.eday = ''  #Parsed Election Date from 68.lst file 
        # Filled with dateNoms()
        self.D1 = {}
        self.D2 = {}
        self.D3 = {}
        self.valid = {}


        if not isinstance(data, auditLog.AuditLog):
            raise Exception('Must pass valid AuditLog object')

        if self.daygrab(data, date):
            #print 'Election Date Retrieved from 68a'
            pass
        else:
            #print 'No 68a Supplied or unable to parse. Inferring Election Day...'
            pass

        self.dateNoms(data)
        self.validParse()
        return

    def daygrab(self, data, date):
        """
        Gets date from l68a file or infer eday
        """

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
        return

    def validDate(self, date):
        """
        Helper function for dateNoms.  Test if opening/closing date is reasonable.
        """
        if date == None: return False
        elif date.date() > self.eday: return False
        elif date.date() < (self.eday - datetime.timedelta(33)): return False
        else: return True


    def dateNoms(self, data):
        """
    This function provides a dictionary/list of machines that experiance a variety
    of different date issues.  The machines are divided into 3 distinct categories
    to be furthur parsed into intelligent reports.

    -Type 1:
        Returns machines who closed on election day but had manual adjustments made
        to their datetime. Includes all machines who were never adjusted until
        election day and those who were off by an hour.
    -Type 2:
        Returns machines which needed adjustments made to their date, but it was 
        never done.  This really means machines opened and closed on impossible 
        dates. It won't catch machines who needed adjusting by an hour or so. 
    -Type 3:
        Returns machines that had date bugs.  This means that the date randomly 
        leaped forward or backward in time or decided its date was 00/00/00 for
        some amount of events.  Sometimes the date is manually changed back or
        sometimes it jumps back on its own, these are all listed because more 
        importantly, the machine was experiancing some serious bugs.
        """

        """
        State that tracks opening and closing events.
        This ensures that only the last opening closing states of a machine
        are saved.  This is because pre-voting opening and closing times are
        not considered in this analysis. State is overwritten with 1 when last
        opening occurs (election day usually).  These are the times used.
        """
        ostate = 0
            #0: Machine never opened or closed
            #1: Machine Opened
            #2: Machine Opened and Closed Sucessfully
            #3: Machine Closed without an Open

        timeset,startset = False, False
        start, end = None, None
        
        jump = False
        jumpEvents = 0
        jumpB, jumpF, jumpZ = False, False, False

        temp = data[0].serialNumber
        lastTime = data[0].dateTime
        for line in data:
            try:
                cTime = dateutil.parser.parse(line.dateTime)
            except ValueError:
                cTime = None 
        
            #--New Machine, process last one--
            if line.serialNumber != temp: 
               
                if ostate == 2:
                    #Populate D1
                    if end != None and end.date() == self.eday:
                        if not self.validDate(start):
                            self.D1.update({temp:(start, end, 'N/A')})

                        elif start.date() == self.eday:
                            if timeset: 
                                start = start - diff 
                                self.D1.update({temp:(start, end, end-start)})
                            self.valid.update({temp:(start, end, end-start)})
                    #Populate D2
                        """
                        Note: I check for invalid opening as well.  This is because
                        It is more likely that something ending on a invalid date
                        without opening on one resulted from a date jump and goes 
                        with D3
                        """
                    elif (not self.validDate(end)) and (not self.validDate(start)):
                        self.D2.update({temp:(start, end, end-start)})

                    #Populate D3
                    if jump:
                        self.D3.update({temp:(startJ,jumpValue,jumpEvents)})
                       
                #Machine Neither Closed Nor Opened
                if ostate == 0: print 'Machine ', temp , ' not closed nor opened'
                #Machine Opened and Not Closed
                elif ostate == 1: print 'Machine', temp, ' Not closed'

                temp = line.serialNumber
                timeset, startset = False, False
                end, start, diff = None, None, None
                ostate = 0

                jump = False
                jumpB, jumpF, jumpZ = False, False, False
                jumpEvents = 0

            #--Record opening state and times--
            if line.eventNumber == '0001672': #Open Event
                ostate = 1
                start = cTime
            elif line.eventNumber == '0001673': #Machine Close
                if ostate == 1:
                    end = cTime
                    ostate = 2
                #Machine Closed without an Open
                elif ostate == 0:
                    ostate = 3
                    print 'Machine ', temp,' closed without open event?!'

            #--If time was adjusted while machine was open record delta--
            elif line.eventNumber == '0000117' and (ostate==1 or ostate==2):
                startset = True

            elif line.eventNumber == '0001656' and startset:
                #Mark changes occuring when open and on eday
                if cTime != None and cTime.date() == self.eday:
                    if lastTime == None:
                        diff = datetime.timedelta(0)
                        timeset = True
                    else:
                        diff =  lastTime - cTime
                        #We don't care for changes less then 1 minute
                        if abs(diff) > datetime.timedelta(0,60):
                            timeset = True
                        else: 
                            timeset = False
                startset = False

            #--Find any date jumping and record date anomalies resulting from bugs--
            """
            This currently doesn't really adapt well to machines experiancing
            many different jumps.  This could be added, but might not be all 
            that useful.  A machine experiencing date bugs is a machine 
            experiencing date bugs. Event count is cumulative among multiple
            jumps however.
            """

            if ostate == 1:
                if line.eventNumber != '0001656' and not jumpB and not jumpF and not jumpZ:
                    #00/00/00 Jump
                    if cTime == None:
                        jump, jumpZ = True, True
                        startJ = lastTime
                        jumpValue = 'Invalid Date'
                    #Backword Jump
                    elif lastTime > cTime:
                        jump,jumpB = True, True
                        startJ = lastTime
                        jumpValue = cTime
                    #Forward Jump (Threshold is arbitrary but works OK)
                    elif (cTime-lastTime) > datetime.timedelta(33):
                        jump,jumpF = True, True
                        startJ = lastTime
                        jumpValue = cTime
                    
                if jumpB:
                    if cTime > startJ:
                        jumbB = False
                    else:
                        jumpEvents += 1
                if jumpF:
                    if cTime.date() == startJ.date():
                        jumpF = False
                    else:
                        jumpEvents += 1
                if jumpZ:
                    if cTime != None:
                        jumpZ = False
                    else:
                        jumpEvents += 1
            elif ostate == 2:
                jumpF, jumpB, jumpZ = False, False, False
                
            lastTime = cTime
                
        return 

    def validParse(self):
        """
        This function takes the dictionary from dateNoms and decides if the 
        datestamp is beleavable.  Uses pretty simple heuristics but works
        well to create a list of valid machines for analysis that monitors
        poll closing times
        """

        d = {}

        #Machine must be open by this time to be assumed valid if open for 12 hours+
        timeopen = dateutil.parser.parse('07:30:00')

        for k,v in self.valid.iteritems():
            if v[0] == 0:
                if v[2] > datetime.timedelta(hours=12) and v[0] < timeopen:
                    d.update({k:v})
                else: pass

        self.valid = d
        return 


    def __del__(self):
        del self.eday
        del self.D1
        del self.D2
        del self.D3
        del self.valid
        return
def count(data):
    d={}
    for line in data:
       d.update({line.serialNumber:1}) 

    return len(d)

if __name__== "__main__":

    path = sys.argv[1]

    try: f = open(path, 'r')
    except:
        print 'Invalid arg'
        exit()

    data = auditLog.AuditLog(f)
    f.close()


    dateclass = DateMod(data, dateutil.parser.parse('11/02/2010'))
    count = count(data)

    for k,v in dateclass.D1.iteritems():
        print k, v[0], v[1], v[2]
    for k,v in dateclass.D2.iteritems():
        print k,v[0], v[1], v[2]
    for k,v in dateclass.D3.iteritems():
        print k,v[0], v[1], v[2]
    print 'Lengths', len(dateclass.D1), len(dateclass.D2), len(dateclass.D3)
    print 'Count', count, '\n'
