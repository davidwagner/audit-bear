# this is the dispatcher function
# it will call all analysis programs with the given files
# and collect the resulting Report structures
from eventAnomaliesAnalyses import *
import dateMod
import myanalyses
import closedLate
from fileAnomalies import *
from pollWorkerEval import *
#from pollWorkerEval import *

def dispatcher(el152=None, el155=None, el68a=None):
    #list of report objects
    results = []

    if el155 != None and el152 != None and el68a != None:
        dateclass = dateMod.DateMod(el152, el68a.electionDate)

        results.append(notUploadedPEBs(el152, el155, el68a, dateclass, report.Report()))
        results.append(notClosedMachines(el152, el155, el68a, dateclass, report.Report()))
        results.append(mismatchVotesMachines(el152, el155, el68a, report.Report()))
        #polling locations open late
        results.extend(closedLate.closedLate(el152, el155, el68a, dateclass))
        #long lines
        #results.extend(myanalyses.earlyVotes(el152,dateclass,el155))
        results.append(getCalibrationEvents2(el152, el155, dateclass, report.Report()))
        results.append(getCalibrationEvents3(el152, el155, dateclass, report.Report()))
        results.append(lowBatteryMachines(el152,el155, dateclass, report.Report()))
        results.append(getTerminalClosedEarlyEvents(el152, el155, dateclass, report.Report()))
        results.extend(myanalyses.edayCorrections(el152,dateclass.eday,el155))
        results.append(machineOpenCloseDiff(el152, el155, el68a, dateclass, report.Report()))
        results.append(checkZeroTapes(el152, el155, dateclass, report.Report()))
        results.append(pebActivateBallot(el152, el155, el68a, dateclass, report.Report()))
        results.append(getVoteCancelledEvents(el152,el155, dateclass, report.Report()))
        results.append(getUnknownEvents(el152, el155, dateclass, report.Report()))
        del dateclass
        return dict(message='files recieved', results=results)
        
    elif el155 != None and el152 != None and el68a == None:
        dateclass = dateMod.DateMod(el152, None)
        #polling locations open late
        #polling locations that close late
        #long lines
        results.append(getCalibrationEvents2(el152, el155, dateclass, report.Report()))
        results.append(getCalibrationEvents3(el152, el155, dateclass, report.Report()))
        results.append(lowBatteryMachines(el152,el155, dateclass, report.Report()))    
        results.append(getTerminalClosedEarlyEvents(el152, el155, dateclass, report.Report()))
        results.append(checkZeroTapes(el152, el155, dateclass, report.Report()))
        results.append(getVoteCancelledEvents(el152,el155, dateclass, report.Report()))
        results.append(getUnknownEvents(el152, el155, dateclass, report.Report()))
        return dict(message='files recieved', results=results)
    else:
        return dict(message='LOLCAT')
