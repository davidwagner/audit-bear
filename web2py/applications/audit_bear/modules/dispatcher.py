# this is the dispatcher function
# it will call all analysis programs with the given files
# and collect the resulting Report structures
"""
import os, sys 
cmd_folder = os.getenv('HOME') + '/audit-bear/modules' 
if cmd_folder not in sys.path: 
    sys.path.insert(0, cmd_folder)
"""
import auditLog
import ballotImage
import dateMod
import dateutil.parser
import report

import operator
import string as stri

from dateutil.parser import parse


def dispatcher(el152=None, el155=None, el68a=None):
    #list of report objects
    results = []

    #Adding some basic analysi
    if el155 != None and el152 != None:
        #Adding some Init stuff we will all probably need
        data = auditLog.AuditLog(el152)
        ballot = ballotImage.BallotImage(el155)

        #HardCode Eday
        eday = parse('November 2, 2011').date()
        #dateData = dateMod.DateMod(data, eday)
        
        #Start running analysis
        #results.append(dateanomalies(data, dateData))
        result1 = eventAnomalies(data, report.Report())
        results.append(result1)
        #report2 = lowBatteryMachines(data,ballot)
        
        return dict(message='files recieved', results=results)
        
    else:
        return dict(message='LOLCAT')

def dateanomalies(): 
    r = report.Report()
    r.addTextBox('---------Date Anomaly Analysis #1-----------')
    
    l = dateMod.check(dateclass.odata, dateclass.eday, dateclass.pday) 
    if len(l[0]) == 0:
        r.addTextBox('No Machines had events after Election Day')
    else: 
        r.addTextBox('These machines had events after Election Day:')
        for k,v in l[0].iteritems(): 
            r.addTextBox('  Machine'+k[0]+'had'+v+'events on'+k[1])
 
    if len(l[1]) == 0: 
        r.addTextBox('No machines voted more then 15 days prior to election day')
    else: 
        r.addTextBox('These machines had votes 16 days or more before Election Day:')
        for k,v in l[1].iteritems(): 
            r.addTextBox('  Machine'+k[0]+'had'+v+'votes on'+k[1])
 
    if len(l[2]) == 0: 
        r.addTextBox('No events with invalid dates')
    else: 
        r.addTextBox('These machines had events with invalid dates')
        values = l[2].values()
        for x in l[2].keys():
            r.addTextBox('  Machine'+str(x[0])+'had'+str(values)+'events on'+str(x[1]))
    return r
    
def eventAnomalies(data, r):
    print r
    
    print 'LOLOLOLOLLL', len(r.getTextBoxList())
    emMap = {}
    emMap2 = {}
    emList = []
    for x in data.getEntryList():
        if emMap.has_key(x.eventNumber):
            if x.serialNumber in emMap[x.eventNumber]:
                continue
            else:
                emMap[x.eventNumber] += [x.serialNumber]
        else:
            emMap[x.eventNumber] = [x.serialNumber]
    for x2 in emMap:
        emMap2[x2] = len(emMap[x2])
    emList = sorted(emMap2.iteritems(), key=operator.itemgetter(1))
    for x3 in emList:
        if x3[1] == 1:
            r.addTextBox("Machine %s has 1 occurence of event %s" % (emMap[x3[0]][0], x3[0]))
    return r
