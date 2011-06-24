#!/usr/bin/python
"""
Used to test out different analysis and modules within the repository. Sort of like the dispatcher.
"""

import os, sys
cmd_folder = os.getenv('HOME') + '/documents/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import auditLog
import funwithdates

#Anderson
path1 = os.getenv('HOME') + '/documents/audit-bear/data/anderson/anderson_co_01_14_11_el152.txt'
path2 = os.getenv('HOME') + '/documents/audit-bear/data/anderson/anderson_co_03_07_11_el68a.txt'
path3 = os.getenv('HOME') + '/documents/audit-bear/data/anderson/anderson_co_01_14_11_el155.txt'
#Berkeley
"""
path1 = os.getenv('HOME') + '/documents/audit-bear/data/berkeley/berkeley_co_11_10_10_el152.lst'
path2 = os.getenv('HOME') + '/documents/audit-bear/data/berkeley/berkeley_co_11_10_10_el68a.LST'
path3 = os.getenv('HOME') + '/documents/audit-bear/data/berkeley/berkeley_co_11_10_10_el155.lst'
"""
#Init Data
f = open(path1, 'r')
data = auditLog.AuditLog(f)
f.close()

#Test Date Module
dateclass = funwithdates.DateMod(data, path2)
print dateclass.eday
print dateclass.pday

#Timeopen Function. 
d = funwithdates.timeopen(dateclass.edata)
for line in d:
    print 'Machine', line[0], 'was open', line[1],'hours'

#Find anomolous dates and print
l = funwithdates.check(dateclass.odata, dateclass.eday, dateclass.pday)

print "These machines had events after Election Day:"
for k,v in l[0].iteritems():
    print 'Machine',k[0],'had',v,'events on',k[1]
print "These machines had votes 16 days or more before Election Day:"
for k,v in l[1].iteritems():
    print 'Machine',k[0],'had',v,'votes on',k[1]
if len(l[2]) == 1:
    print l[2]
else:
    print "These machines had events with date errors"
    for k,v, in l[2].iteriterms():
        print 'Machine',k[0],'had',v,'events on',k[1]

