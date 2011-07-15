#Place to put my analyses for now
import auditLog
import ballotImage
import dateMod
import datetime
import dateutil.parser
import report

import matplotlib.pyplot as plot
import StringIO
from math import ceil



def dateanomalies(data, dateclass): 
    plot.ioff()
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
            r.addTextBox('&nbsp Machine '+str(k[0])+' had '+str(v).zfill(2)+' events on '+str(k[1]))
    return r

def precinctStats(dateclass, ballotclass):
    plot.ioff()
    r = report.Report()
    t = report.Table()
    r.addTitle('Precint Date Stats')

    #report Machines that had dates corrected ON election day

    times, adjustedL = dateMod.timeopen(dateclass.edata)
    precinctMap = ballotclass.getPrecinctNameMap()
    d = {}
    for tup in adjustedL:
        print abs(tup[1])
        if abs(tup[1]) > datetime.timedelta(0,0,0,0,1): #Adjusted by 1 minute or more?
            key = precinctMap[tup[0]]
            if key in d:
                d[key] = (d[key][0]+1, d[key][1] + abs(tup[1]))
            else:
                d.update({key:(1,abs(tup[1]))})
    t.addHeader('Precinct')
    t.addHeader('# of Machines')
    t.addHeader('Absolute Average Timedelta') 
    for k,v in d.iteritems():
        t.addRow([k,str(v[0]), str(v[1]/v[0])[:8]])
    r.addTable(t)

    #report early voting by precinct AND check for correct dates
     
    return r

def openmachines(dateclass, bins=10):
    plot.ioff()
    r = report.Report()
    r.addTitle('Machines whose time was corrected during Election Day (and random Hist)')

    o, adjusted = dateMod.timeopen(dateclass.edata)
    x = []
    for k,v in o.iteritems():
        if v[0] == 1:
             r.addTextBox('Machine '+str(k)+' was left open since pre-voting')
        elif v[0] == 0:
            x.append(float(str(v[3]).split(':')[0]) + float(str(v[3]).split(':')[1])//60)

    binsize=ceil((max(x)-min(x))/bins)
    maximum = bins*binsize+min(x)
    rg = (min(x),maximum)

    plot.figure()
    plot.hist(x, bins=bins, range=rg, color='g', rwidth=1)
    plot.xlabel('Hours a Machine Stayed Open')
    plot.ylabel('# of Machines in Range')
    plot.grid(True)
    plot.xticks([i for i in range(int(min(x)), int(maximum+binsize), int(binsize))])
    plot.title('Histogram: Hours Machines Were Opened on Election Day')
    stio = StringIO.StringIO()
    plot.savefig(stio)
    r.addImage(report.Image(stio, 'Plot 1'))

    plot.cla()
    plot.clf()
    plot.close('all')
    
    
    r.addTextBox("<i>This data was based only on events that occured on the election.  It is assumed that machines that weren't opened were opened for pre-voting and left open</i>")

    return r

