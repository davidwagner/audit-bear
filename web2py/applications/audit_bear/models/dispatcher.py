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

from dateutil.parser import parse


def dispatcher(el152=None, el155=None, el68a=None):
    #list of report objects
    results = []

    #Adding some basic analysi
    if el152 != None :
        #Adding some Init stuff we will all probably need
        data = auditLog.AuditLog(el152)

        #HardCode Eday
        eday = parse('November 2, 2011').date()
        #dateData = dateMod.DateMod(data, eday)
        
        #Start running analysis
        #results.append(dateanomalies(data, dateData))
        return dict(message='files recieved')
        
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

