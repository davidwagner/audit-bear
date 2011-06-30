#!/usr/bin/python
"""
Adding my analysis here for now.  Each one should result a result object.
"""

import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import auditLog
import funwithdates
import ballotImage
import report

from math import ceil
import matplotlib.pyplot as plot

"""
#Anderson
path1 = os.getenv('HOME') + '/audit-bear/data/anderson/anderson_co_01_14_11_el152.txt'
path2 = os.getenv('HOME') + '/audit-bear/data/anderson/anderson_co_03_07_11_el68a.txt'
path3 = os.getenv('HOME') + '/audit-bear/data/anderson/anderson_co_01_14_11_el155.txt'
#Berkeley
"""
path1 = os.getenv('HOME') + '/audit-bear/data/berkeley/berkeley_co_11_10_10_el152.lst'
path2 = os.getenv('HOME') + '/audit-bear/data/berkeley/berkeley_co_11_10_10_el68a.LST'
path3 = os.getenv('HOME') + '/audit-bear/data/berkeley/berkeley_co_11_10_10_el155.lst'

#Init
f = open(path1, 'r')
data = auditLog.AuditLog(f)
f.close()
"""
f = open(path3, 'r')
ballot = ballotImage.BallotImage(f)
f.close()
"""

f = open(path2, 'r')
dateclass = funwithdates.DateMod(data, f)
f.close()

#Dispatch:
def main():
    dateanomalies()
    openmachines()
    #ballottest()

def openmachines(bins=10):
    print "-------------Machine Open Times Analysis ------------------"
    o = funwithdates.timeopen(dateclass.edata)
    x = []
    for k,v in o.iteritems():
        if v[0] == 1:
            print 'Machine',k,'open since pre-voting'
        elif v[0] == 0:
            x.append(float(str(v[3]).split(':')[0]) + float(str(v[3]).split(':')[1])//60)



    binsize=ceil((max(x)-min(x))/bins)
    maximum = bins*binsize+min(x)
    r = (min(x),maximum) 
    
    plot.hist(x, bins=bins, range=r, color='g', rwidth=1)
    plot.xlabel('Hours a Machine Stayed Open')
    plot.ylabel('# of Machines in Range')
    plot.grid(True)
    plot.xticks([i for i in range(int(min(x)), int(maximum+binsize), int(binsize))])
    plot.title('Histogram: Hours Machines Were Opened on Election Day')
    plot.show()
    print "This data was based only on events that occured on the election.  It is assumed that machines that weren't opened were opened for pre-voting and left open"

def dateanomalies():
    print"-------------Date Anomaly Analysis #1 --------------------"
    l = funwithdates.check(dateclass.odata, dateclass.eday, dateclass.pday)
    if len(l[0]) >0:
        print "These machines had events after Election Day:"
        for k,v in l[0].iteritems():
            print '    Machine',k[0],'had',v,'events on',k[1]

    if len(l[1]) == 0:
        print "No Machines Voted before Pre-Voting"
    else:
        print "These machines had votes 16 days or more before Election Day:"
        for k,v in l[1].iteritems(): print '  Machine',k[0],'had',v,'votes on',k[1]

    if len(l[2]) == 1:
        print l[2]
    else:
        print "These machines had events with date errors"
        for k,v, in l[2].iteriterms():
            print 'Machine',k[0],'had',v,'events on',k[1]

def ballottest():
    ballot.getPrecinctNumMap()
    ballot.getPrecinctNameMap()
    print ballot.getPrecinctMap() 


if __name__ == "__main__":
    main()
