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
    
    l = dateMod.check(data, dateclass.eday, dateclass.pday) 
    return r

def edayCorrections(data,eday, ballotclass):
    plot.ioff()
    r = report.Report()
    t = report.Table()
    r.addTitle('Machines with Election day corrections')

    #report Machines that had dates corrected ON election day
    r.addTextBox('<p><i>This report identifies machines that recorded manual date changes to iVotronic machines that occured during election AND while the machine was opened for voting.  Machines are grouped by precinct.</p><p> This may identify precincts with systematic date problems or errors by pollworkers.  If an date change event is seen with a timedelta of less then 1 minutes, it is ignored.  Additionally, the average reported is an average of the absolute values of the time changes. </i></p>')

    times, adjustedL = dateMod.timeopen(data, eday)
    if len(adjustedL) == 0:
        print 'Report on election day time adjustments not included'
        return []
    else:
        precinctMap = ballotclass.getPrecinctNameMap()
        d = {}
        for tup in adjustedL:
            if abs(tup[1]) > datetime.timedelta(0,0,0,0,1): #Adjusted by 1 minute or more?
                if tup[0] in precinctMap:
                    key = precinctMap[tup[0]]
                elif tup[0] in ballotclass.getEarlyVotingList():
                    key = 'Absentee'
                elif tup[0] in ballotclass.getFailsafeList():
                    key = 'Failsafe'
                else:
                    print 'Red Flag! Machine',tup[0],'not listed in any precinct'
                    key = tup[0]
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

def earlyVotes(data, dateclass, ballotclass):
    r = report.Report()
    t = report.Table()

    r.addTitle('Early Voting')
    #report extra early voting by precinct AND check for correct dates
    r.addTextBox('<i>This report determines the precincts that have votes cast more then 15 days prior to election day.</i>')

    machines = dateclass.voteEarly(data)
    precinctMap = ballotclass.getPrecinctNameMap()
    if len(machines) == 0:
        print 'earlyVotes analysis empty: Skipped'
        return []

    #Group by precinct: {Precinct:(#Machines, #Votes, #Start, #Last)}
    d = {}
    
    for k,v in machines.iteritems():
        if k in precinctMap:
            key = precinctMap[k]
        elif k in ballotclass.getEarlyVotingList():
            key = 'Absentee'
        elif k in ballotclass.getFailsafeList():
            key = 'Failsafe'
        else:
            print 'Important! Machine',k,'not listed in any precinct'
            key = k
        if key in d:
            if d[key][2] < v[1]: v[1] = d[key][2]
            if d[key][3] > v[2]: v[2] = d[key][3]

            d[key] = [d[key][0]+1, d[key][1]+v[0], v[1], v[2]]
        else:
            d.update({key:[1, v[0], v[1], v[2]]})

    t.addHeader('Precinct')
    t.addHeader('# of Machines')
    t.addHeader('Total Votes')
    t.addHeader('Range Min')
    t.addHeader('Range Max')

    for k,v in d.iteritems():
        t.addRow([k] + [str(x) for x in v])

    r.addTable(t)
    return [r]

def machines():
    pass
    #report machines that are recording events on bad dates(2009, 2053) after being opened.  This includes 00 dates and future dates. 

def voteRange():
    #Only display precincts that exhibit early votes OR that display votes late. Could add in closed status and whether voted on election day.
    pass


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

