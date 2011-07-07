#Place to put my analyses for now
import auditLog
import ballotImage
import dateMod
import dateutil.parser
import report

import matplotlib.pyplot as plot
import StringIO
from math import ceil



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
    elif len(l[2]) == 1:
        r.addTextBox('<b>These machines had events with invalid dates<br></b>')
        v = l[2].values()[0]
        k = l[2].keys()[0]
        r.addTextBox('&nbsp Machine '+str(k[0])+' had '+str(v)+' events on '+str(k[1]))
       
    else: 
        r.addTextBox('<b>These machines had events with invalid dates<br></b>')
        for k,v in l[2].iteritems():
            r.addTextBox('&nbsp Machine '+str(x[0])+' had '+str(v).zfill(2)+' events on '+str(x[1]))
    return r


def openmachines(dateclass, bins=10):
    r = report.Report()
    r.addTitle('Hours DREs Stayed Open Election Day')

    o = dateMod.timeopen(dateclass.edata)
    x = []
    for k,v in o.iteritems():
        if v[0] == 1:
             r.addTextBox('Machine '+str(k)+' was left open since pre-voting')
        elif v[0] == 0:
            x.append(float(str(v[3]).split(':')[0]) + float(str(v[3]).split(':')[1])//60)

    binsize=ceil((max(x)-min(x))/bins)
    maximum = bins*binsize+min(x)
    rg = (min(x),maximum)

    plot.hist(x, bins=bins, range=rg, color='g', rwidth=1)
    plot.xlabel('Hours a Machine Stayed Open')
    plot.ylabel('# of Machines in Range')
    plot.grid(True)
    plot.xticks([i for i in range(int(min(x)), int(maximum+binsize), int(binsize))])
    plot.title('Histogram: Hours Machines Were Opened on Election Day')
    stio = StringIO.StringIO()
    plot.savefig(stio)
    r.addImage(report.Image(stio, 'Plot 1'))
    
    
    r.addTextBox("<i>This data was based only on events that occured on the election.  It is assumed that machines that weren't opened were opened for pre-voting and left open</i>")

    return r

