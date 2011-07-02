# this is the dispatcher function
# it will call all analysis programs with the given files
# and collect the resulting Report structures
from eventAnomaliesAnalyses import *

def dispatcher(el152=None, el155=None, el68a=None):
    #list of report objects
    results = []

    #Adding some basic analysis stuff
    if el155 != None and el152 != None:
        #Adding some Init stuff we will all probably need
        data = auditLog.AuditLog(el152)
        ballot = ballotImage.BallotImage(el155)

        #Start running analysis
        results.append(eventAnomalies(data, report.Report()))
        results.append(lowBatteryMachines(data,ballot,report.Report()))
        results.append(getWarningEvents(data,ballot,report.Report()))
        results.append(getVoteCancelledEvents(data,ballot,report.Report()))
        
        return dict(message='files recieved', results=results)
    else:
        return dict(message='LOLCAT')

