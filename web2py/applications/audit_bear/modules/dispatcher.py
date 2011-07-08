# this is the dispatcher function
# it will call all analysis programs with the given files
# and collect the resulting Report structures
from eventAnomaliesAnalyses import *
import dateMod
import myanalyses

def dispatcher(el152=None, el155=None, el68a=None):
    #list of report objects
    results = []

    #Adding some basic analysis stuff
    if el155 != None and el152 != None and el68a != None:
        dateclass = dateMod.DateMod(el152, el68a.electionDate)
        
        #Start running analysis
        results.append(myanalyses.dateanomalies(el152, dateclass))
        results.append(myanalyses.openmachines(dateclass))
        #results.append(eventAnomalies(el152, report.Report()))
        results.append(lowBatteryMachines(el152,el155,report.Report()))
        results.append(getWarningEvents(el152,el155,report.Report()))
        results.append(getVoteCancelledEvents(el152,el155,report.Report()))
        return dict(message='files recieved', results=results)
        
    elif el155 != None and el152 != None and el68a == None:
        dateclass = dateMod.DateMod(el152, None)

        #Start running analysis
        results.append(myanalyses.dateanomalies(el152, dateclass))
        results.append(myanalyses.openmachines(dateclass))
        #results.append(eventAnomalies(el152, report.Report()))
        results.append(lowBatteryMachines(el152,el155,report.Report()))
        results.append(getWarningEvents(el152,el155,report.Report()))
        results.append(getVoteCancelledEvents(el152,el155,report.Report()))
        
        return dict(message='files recieved', results=results)
    else:
        return dict(message='LOLCAT')
