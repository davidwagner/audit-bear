# this is the dispatcher function
# it will call all analysis programs with the given files
# and collect the resulting Report structures
from eventAnomaliesAnalyses import *
import dateMod
import myanalyses
import closedLate
from fileAnomalies import *
#from pollWorkerEval import *

def dispatcher(el152=None, el155=None, el68a=None):
    #list of report objects
    results = []

    if el155 != None and el152 != None and el68a != None:
        dateclass = dateMod.DateMod(el152, el68a.electionDate)

        results.append(notUploadedPEBs(el152, el155, el68a, report.Report()))
        results.append(notClosedMachines(el152, el155, el68a, report.Report()))
        #results.append(checkFiles(el152, el155, el68a, report.Report()))
        results.append(closedLate.closedLate(el152, el155, el68a, dateclass))
        results.extend(myanalyses.edayCorrections(el152,dateclass.eday,el155))
        results.extend(myanalyses.earlyVotes(el152,dateclass,el155))
        results.append(lowBatteryMachines(el152,el155, report.Report()))
        results.append(getCalibrationEvents(el152, el155, report.Report()))
        results.append(getCalibrationEvents2(el152, el155, report.Report()))
        results.append(getTerminalClosedEarlyEvents(el152, el155, report.Report()))
        results.append(getUnknownEvents(el152, el155, report.Report()))
        results.append(getVoteCancelledEvents(el152,el155, report.Report()))
        #results.append(checkZeroTapes(el152,el155,report.Report()))
        #results.append(checkResultsTapes(el152, el155, report.Report()))
        del dateclass
        return dict(message='files recieved', results=results)
        
    elif el155 != None and el152 != None and el68a == None:
        dateclass = dateMod.DateMod(el152, None)

        results.append(lowBatteryMachines(el152,el155,report.Report()))
        results.append(getCalibrationEvents(el152, el155, report.Report()))
        results.append(getCalibrationEvents2(el152, el155, report.Report()))
        results.append(getTerminalClosedEarlyEvents(el152, el155, report.Report()))
        results.append(getUnknownEvents(el152, el155, report.Report()))
        results.append(getVoteCancelledEvents(el152,el155,report.Report()))
        #results.append(checkZeroTapes(el152, el155, report.Report()))
        #results.append(checkResultsTapes(el152, el155, report.Report()))
        
        return dict(message='files recieved', results=results)
    else:
        return dict(message='LOLCAT')
