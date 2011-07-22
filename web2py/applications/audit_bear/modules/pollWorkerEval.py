# POLL WORKER EVALUATION ANALYSES MODULE
import auditLog
import ballotImage
import dateMod
import dateutil.parser
import report

import operator
import string as stri
import math
import StringIO
import matplotlib
import matplotlib.pyplot as plt

from dateutil.parser import parse

def checkZeroTapes(data, ballot, dc, r):
    d = str(dc.eday)
    d = d.split("-")
    d2 = d[1]+'/'+d[2]+'/'+d[0]
    r.addTitle("Polling locations that did not print zero tapes")
    #check for one instance of event # 0002010 : Print cumulative zeros tape in each polling location
    precinctMap = ballot.machinesPerPrecinct
    machineList = []
    zeroList = []
    nonZeroList = []
    nonZeroList2 = []
    for x in data.getEntryList():
        s = x.dateTime.split(" ")
        t = s[1].split(":")
        if t[0] == '':
            continue
        elif x.eventNumber == '0002010' and (s[0] == d2):
            machineList.append(x.serialNumber)
    for y in machineList:
        for y2 in precinctMap:
            if y in precinctMap[y2]:
                zeroList.append(y)
    for z in machineList:
        if z in zeroList:
            continue
        else:
            nonZeroList.append(z)
    for m in nonZeroList:
        if ballot.machinePrecinctNameMap.has_key(m):
            nonZeroList2.append(m)
    #print "NONZEROLIST"      
    #print nonZeroList
    if len(nonZeroList2) < 1:
        r.addTextBox("No problems found.")
    b = True
    for m2 in nonZeroList2:
        if b == True:
            r.addTextBox("The following precincts did not print zero tapes on the morning of election day.  We suggest that this be emphasized in future poll worker training.")
            r.addTextBox(" ")
            b = False
        r.addTextBox("%s (#%s)   %s" % (ballot.machinePrecinctNameMap[m2], ballot.machinePrecinctNumMap[m2], m2))
    return r
