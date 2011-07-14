# this is the dispatcher function
# it will call all analysis programs with the given files
# and collect the resulting Report structures
from eventAnomaliesAnalyses import *
import dateMod
import myanalyses
from fileAnomalies import *

def dispatcher(el152=None, el155=None, el68a=None):
    #list of report objects
    results = []

    if el155 != None and el152 != None and el68a != None:
        dateclass = dateMod.DateMod(el152, el68a.electionDate)
        
        results.append(myanalyses.dateanomalies(el152, dateclass))
        results.append(myanalyses.openmachines(dateclass))
        results.append(myanalyses.precinctStats(dateclass,el155))
        #results.append(eventAnomalies(el152, report.Report()))
        results.append(lowBatteryMachines(el152,el155,report.Report()))
        results.append(getWarningEvents(el152,el155,report.Report()))
        results.append(getVoteCancelledEvents(el152,el155,report.Report()))
        results.append(checkFiles(el152, el155, el68a, report.Report()))
        del dateclass
        return dict(message='files recieved', results=results)
        
    elif el155 != None and el152 != None and el68a == None:
        dateclass = dateMod.DateMod(el152, None)

        results.append(myanalyses.dateanomalies(el152, dateclass))
        results.append(myanalyses.openmachines(dateclass))
        results.append(eventAnomalies(el152, report.Report()))
        results.append(lowBatteryMachines(el152,el155,report.Report()))
        results.append(getWarningEvents(el152,el155,report.Report()))
        results.append(getVoteCancelledEvents(el152,el155,report.Report()))
        
        return dict(message='files recieved', results=results)
    else:
        return dict(message='LOLCAT')
