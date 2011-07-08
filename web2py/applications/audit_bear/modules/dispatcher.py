# this is the dispatcher function
# it will call all analysis programs with the given files
# and collect the resulting Report structures
from eventAnomaliesAnalyses import *
import dateMod
import myanalyses
import el68a as el68aParser

def dispatcher(el152=None, el155=None, el68a=None):
    #list of report objects
    results = []

    #Adding some basic analysis stuff
    if el155 != None and el152 != None and el68a != None:
        #Adding some Init stuff we will all probably need
        data = auditLog.AuditLog(el152)

        parsedEL68 = el68aParser.EL68A(el68a)
        ballot = ballotImage.BallotImage(el155, data, parsedEL68)
        dateclass = dateMod.DateMod(data, parsedEL68.electionDate)
        
        
        #Start running analysis
        results.append(myanalyses.dateanomalies(data, dateclass))
        results.append(myanalyses.openmachines(dateclass))
        #results.append(eventAnomalies(data, report.Report()))
        #results.append(lowBatteryMachines(data,ballot,report.Report()))
        results.append(getWarningEvents(data,ballot,report.Report()))
        results.append(getVoteCancelledEvents(data,ballot,report.Report()))
        return dict(message='files recieved', results=results)
        
    elif el155 != None and el152 != None and el68a == None:
        data = auditLog.AuditLog(el152)
        ballot = ballotImage.BallotImage(el155, data)
        dateclass = dateMod.DateMod(data, None)

        #Start running analysis
        results.append(myanalyses.dateanomalies(data, dateclass))
        results.append(myanalyses.openmachines(dateclass))
        #results.append(eventAnomalies(data, report.Report()))
        #results.append(lowBatteryMachines(data,ballot,report.Report()))
        results.append(getWarningEvents(data,ballot,report.Report()))
        results.append(getVoteCancelledEvents(data,ballot,report.Report()))
        
        return dict(message='files recieved', results=results)
    else:
        return dict(message='LOLCAT')
