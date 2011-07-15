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
    r.addTitle("Detection of polling locations that did not print Zero Tapes")
    #check for one instance of event # 0002010 : Print cumulative zeros tape in each polling location
    precinctMap = ballot.machinesPerPrecinct
    machineList = []
    zeroList = []
    nonZeroList = []
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
        r.addTextBox("%s (#%s)   %s" % (ballot.machinePrecinctNameMap[m], ballot.machinePrecinctNumMap[m], m))
    return r

def checkResultsTapes(data, ballot, r):
    r.addTitle("Detection of Polling locations that did not print Results Tapes")
    #check for one instance of event # 0002011 : Print cumulative results tape in each polling location
    precinctMap = ballot.machinesPerPrecinct
    machineList = []
    for x in data.getEntryList():
        s = x.dateTime.split(" ")
        t = s[1].split(":")
        if t[0] == '':
            continue
        elif x.eventNumber == '0002011' and (s[0] == '11/02/2010' or s[0] == '06/08/2010'):
            machineList.append(x.serialNumber)
    for m in machineList:
        r.addTextBox(m)
    return r
