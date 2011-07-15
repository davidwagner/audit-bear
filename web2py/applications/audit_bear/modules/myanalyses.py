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
            r.addTextBox('&nbsp Machine '+str(k[0])+': had '+str(v).zfill(2)+' events on '+str(k[1]))
    return r

def edayCorrections(dateclass, ballotclass):
    plot.ioff()
    r = report.Report()
    t = report.Table()
    r.addTitle('Machines with Election day corrections')

    #report Machines that had dates corrected ON election day
    r.addTextBox('<p><i>This report identifies machines that recorded manual date changes to iVotronic machines that occured during election AND while the machine was opened for voting.  Machines are grouped by precinct.</p><p> This may identify precincts with systematic date problems or errors by pollworkers.  If an date change event is seen with a timedelta of less then 1 minutes, it is ignored.  Additionally, the average reported is an average of the absolute values of the time changes. </i></p>')

    times, adjustedL = dateMod.timeopen(dateclass.edata)
    if len(adjustedL) == 0:
        print 'Report on election day time adjustments not included'
        return []
    else:
        precinctMap = ballotclass.getPrecinctNameMap()
        d = {}
        for tup in adjustedL:
            print abs(tup[1])
            if abs(tup[1]) > datetime.timedelta(0,0,0,0,1): #Adjusted by 1 minute or more?
                if tup[0] in precinctMap:
                    key = precinctMap[tup[0]]
                elif tup[0] in ballotclass.getEarlyVotingList():
                    key = 'Absentee'
                elif tup[0] in ballotclass.getFailsafeList():
                    key = 'Failsafe'
                else:
                    print 'Red Flag! Machine',tup[0],'not listed in any precinct'
                if key in d:
                    d[key] = (d[key][0]+1, d[key][1] + abs(tup[1]))
                else:
                    d.update({key:(1,abs(tup[1]))})
        t.addHeader('Precinct')
        t.addHeader('# of Machines')
        t.addHeader('Average Timedelta') 
        for k,v in d.iteritems():
            t.addRow([k,str(v[0]), str(v[1]/v[0])[:7]])
        r.addTable(t)
    return [r]

def earlyVotes():
    r = report.Report()
    r.addTitle('EXTREME Early Voting! \m/')
    #report extra early voting by precinct AND check for correct dates
    r.addTextBox('<i>This report determines the dates</i>')
    return
def machines():
    pass
    #report machines that are recording events on bad dates(2009, 2053) after being opene



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

