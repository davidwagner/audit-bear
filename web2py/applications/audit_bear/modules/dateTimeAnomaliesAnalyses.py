# DATETIME ANOMALIES THINGY

def dateanomalies(): 
    #HardCode Eday
    eday = parse('November 2, 2011').date()
    #dateData = dateMod.DateMod(data, eday)

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
    
