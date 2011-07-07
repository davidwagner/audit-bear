#Place to put my analyses for now
import auditLog
import ballotImage
import dateMod
import dateutil.parser
import report

import matplotlib.pyplot as plot



def dateanomalies(data, dateclass): 
    r = report.Report()
    r.addTitle('Date Anomaly Report')
    
    l = dateMod.check(dateclass.odata, dateclass.eday, dateclass.pday) 
    if len(l[0]) == 0:
        r.addTextBox('<b>No Machines had events after Election Day<br></b>')
    else: 
        r.addTextBox('<b>These machines had events after Election Day:<br></b>')
        for k,v in l[0].iteritems(): 
            r.addTextBox('&nbsp Machine '+str(k[0])+' had '+str(v).zfill(2)+' events on '+str(k[1]))
 
    if len(l[1]) == 0: 
        r.addTextBox('<b>No machines voted more then 15 days prior to election day<br></b>')
    else: 
        r.addTextBox('<b>These machines had votes 16 days or more before Election Day:<br></b>')
        for k,v in l[1].iteritems(): 
            r.addTextBox('&nbsp Machine '+str(k[0])+' had '+str(v).zfill(2)+' votes on '+str(k[1]))
 
    if len(l[2]) == 0: 
        r.addTextBox('<b>No events with invalid dates<br></b>')
    else: 
        r.addTextBox('<b>These machines had events with invalid dates<br></b>')
        values = l[2].values()
        for x in l[2].keys():
            r.addTextBox('&nbsp Machine '+str(x[0])+' had '+str(values).zfill(2)+' events on '+str(x[1]))
    return r



