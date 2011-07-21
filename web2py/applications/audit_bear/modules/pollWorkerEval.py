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

def checkZeroTapes(data, ballot, r):
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
        elif x.eventNumber == '0002010' and (s[0] == '11/02/2010' or s[0] == '06/08/2010'):
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
    print "NONZEROLIST"      
    print nonZeroList
    if len(nonZeroList2) < 1:
        r.addTextBox("No problem found.")
    for m2 in nonZeroList2:
        r.addTextBox("%s (#%s)   %s" % (ballot.machinePrecinctNameMap[m2], ballot.machinePrecinctNumMap[m2], m2))
    return r
