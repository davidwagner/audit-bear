import dateutil.parser
import datetime
import re

# map is as follows
# Polling Location -> Serial Number -> Time Window -> Relevant Event Count

def inferLines(auditLog, ballotImage, validMachines):
    busyPollingLocationsMap = {}
    incorrectMachine = ''

    for line in auditLog:
        if incorrectMachine == line.serialNumber:
            continue
        elif not line.serialNumber in validMachines:
            incorrectMachine = line.serialNumber
            continue
        else:
            # machine is correct
            incorrectMachine = ''

            # get machine's polling Location and add to map
            try:
                pollingLocation = ballotImage.machinePrecinctNumMap[line.serialNumber]
            except:
                if line.serialNumber in ballotImage.earlyVotingList:
                    pollingLocation = '750'
                elif line.serialNumber in ballotImage.failsafeList:
                    pollingLocation = '850'
                else:
                    incorrectMachine = line.serialNumber
                    continue

            if not pollingLocation in busyPollingLocationsMap:
                busyPollingLocationsMap[pollingLocation] = {}
            
            if not line.serialNumber in busyPollingLocationsMap[pollingLocation]:
                busyPollingLocationsMap[pollingLocation][line.serialNumber] = initMachineTimeWindowMap()

            if not isImportantEvent(line.eventNumber):
                continue
            else:
                # the event is important, sum its count
                try:
                    window = correspondingTimeWindow(line.dateTime)
                except:
                    continue

                busyPollingLocationsMap[pollingLocation][line.serialNumber][window] +=1

    # finished! now do other stuff...
    # determine busy polling locations


    finishedBPLMap = initFinishedMap(busyPollingLocationsMap.keys())
    eventThreshold = 3
    for pollingLocation in finishedBPLMap:
        for window in finishedBPLMap[pollingLocation]:
            count = 0.0

            for machine in busyPollingLocationsMap[pollingLocation]:
                count += busyPollingLocationsMap[pollingLocation][machine][window]

            count /= len(busyPollingLocationsMap[pollingLocation])
            finishedBPLMap[pollingLocation][window] = count

    return finishedBPLMap 

def initFinishedMap(pollingLocations):
    pollMap = {}
    for pollingLocation in pollingLocations:
        pollMap[pollingLocation] = initMachineTimeWindowMap()

    return pollMap

def initMachineTimeWindowMap():
    machineMap = {}
    for window in generateTimeWindows():
        machineMap[window] = 0

    return machineMap

def isImportantEvent(event):
    #r = re.search(r"000151[013456789]", event)
    r = re.search(r"000151[01]", event)
    if r:
        return True
    else:
        return False

def correspondingTimeWindow(t):
    dt = dateutil.parser.parse(t)
    td = datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
    t1 = t2 = None
    for window in generateTimeWindows():
        if td >= window[0] and td < window[1]:
            t1 = window[0]
            t2 = window[1]

    if not t1 or not t2:
        raise Exception("LOLLLLL!!!!! YOUR TIME IS OUT OF BOUNDS OH LOOK A SQUIRREL")

    return (t1, t2)


def generateTimeWindows():
    time = datetime.timedelta(hours = 7) # starting time
    td = datetime.timedelta(minutes=15)  # increment
    mtime = datetime.timedelta(hours=21) # finishing time

    windows = []
    while time + td <= mtime:
        windows.append((time, time+td))
        time += td

    return windows

def strTimeWindow(window):
    return '[' + str(window[0]) + ' -> ' + str(window[1]) + ']'

