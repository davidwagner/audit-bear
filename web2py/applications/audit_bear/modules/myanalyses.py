#Place to put my analyses for now
import auditLog
import ballotImage
import dateMod
import datetime
import dateutil.parser
import report

def datesUnset(dateclass, ballotclass):
    r = report.Report()
    t1 = report.Table()
    t2 = report.Table()
    
    r.addTitle('Incorrectly Set Dates')

    if not (len(dateclass.D1) or len(dateclass.D2)):
        r.addTextBox('No unset or missset dates found')
    else:
        precinctMap = ballotclass.getPrecinctNameMap()
        r.addTextBox('Description Here')

        t1.addHeader('Machine')
        t1.addHeader('Eday Start')
        t1.addHeader('Eday End')
        t1.addHeader('Manual Adjustment')
        for k,v in dateclass.D1.iteritems():
            t1.addRow([str(k), str(v[0]), str(v[1]), str(v[2])])

        r.addTextBox('Uncorrected Machines')
        t2.addHeader('Machine')
        t2.addHeader('Eday Start')
        t2.addHeader('Eday End')
        for k,v in dateclass.D2.iteritems():
            t2.addRow([str(k), str(v[0]), str(v[1])])

        r.addTable(t1)
        r.addTable(t2)

    return r 
def dateErrors(dateclass, ballotclass):
    r = report.Report()
    t = report.Table()
    
    r.addTitle('Datetime Errors')

    if len(dateclass.D3) == 0:
        r.addTextBox('No date errors found')
    else:

        precinctMap = ballotclass.getPrecinctNameMap()
        r.addTextBox('Description Here')
        t.addHeader('Machine')
        t.addHeader('Pre Jump')
        t.addHeader('Jump Value')
        t.addHeader('Occurances')
        for k,v in dateclass.D3.iteritems():
            t.addRow([str(k), str(v[0]), str(v[1]), str([2])])

        r.addTable(t)

    return r 
