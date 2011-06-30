#!/usr/bin/python

#This function lists the election day terminals closed on a non-master PEB.
def close_nm_PEB():
    
    import os, sys
    cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
    if cmd_folder not in sys.path:
        sys.path.insert(0, cmd_folder)
    from auditLog import AuditLog   #imports audit log class
    from ballotImage import BallotImage  #imports ballot image class

    path = sys.argv[1]
    path2 = sys.argv[2]

    parsedLog = AuditLog(open(path, "r"))
    parsedBallotImage = BallotImage(open(path2, 'r'))

    import dateutil.parser
    import datetime
    mapNM = {} # new machine temp map
    mapM = {}
    # machine# -> PEB#, DateTime, vote count
    non_master = False
    master = False
    countMachine = 0
#This for loop finds the machines closed on a non-master PEB and master PEB, then creates 
#a dictionary which includes serial number (key) and values of PEB 
#serial number, date and time and total votes cast on the machine
    for line in parsedLog:
        if not line[0] in mapNM:
            countMachine += 1
            count = 0
            non_master = False
            master = False
            mapNM[line[0]] = []
            mapM[line[0]] = []
        if line[4] == "0001206":
            non_master = True
            mapNM[line[0]].append(line[1])
        if line[4] == "0001510" or line[4] == "0001511":
            count += 1
        if line[4] == "0001673" and non_master:
            mapNM[line[0]].append(line[3])
            mapNM[line[0]].append(count)
        if line[4] == "0001673" and not non_master:
            mapM[line[0]].append(line[1])
            mapM[line[0]].append(line[3])
            mapM[line[0]].append(count)

    newMapNM = {}
    newMapM = {}
 
#This for loop verifies the machines that have the event 0001206 and stores it
#in a mapNM, the machines that don't have the event 0001206 are stored in mapM.
    for key in mapNM:
        if len(mapNM[key]) is not 0:
            newMapNM[key] = mapNM[key]
        if len(mapM[key]) is not 0:
            newMapM[key] = mapM[key]
    
    map2_NM = {}
    map2_M = {}
    earlyVotingList = parsedBallotImage.getEarlyVotingList()

#This for loop excludes the early voting machines, and stored the other machines
#in another maps. 
    for key in newMapNM:
        if not key in earlyVotingList:
            map2_NM[key] = newMapNM[key]
            #print key, newMapNM[key]

    for key2 in newMapM:
        if not key2 in earlyVotingList:
            map2_M[key2] = newMapM[key2]
            #print key2, newMapM[key2] 
    precinctNumMap = parsedBallotImage.getPrecinctNumMap()

#This for loop finds the precinct number of each machine in map2_NM and map2_M, and
#append it in both maps.
    for key in map2_NM:
        if precinctNumMap.has_key(key):
            map2_NM[key].append(precinctNumMap[key])
        #print key, map2_NM[key]

    for key2 in map2_M:
        if precinctNumMap.has_key(key2):
            map2_M[key2].append(precinctNumMap[key2])
        #print key2, map2_M[key2]
    # added by samuel
    #for key in sorted(precinctNumMap):
        #print key + ' ' + precinctNumMap[key]

    combinedMap = parsedBallotImage.getCombinedMap()
    
    listPEB = []
    for key in map2_M:
        if not map2_M[key][0] in listPEB:
            listPEB.append(map2_M[key][0])
    for key in map2_NM:
        if not map2_NM[key][0] in listPEB:
            listPEB.append(map2_NM[key][0])
    print listPEB
    print len(listPEB)
    #for key in sorted(combinedMap):
        #print key + ' ' + combinedMap[key]

    #return map3
    #key, map3[key][0]
    #print "------------------------------------------------------------"
    #mmp = parsedBallotImage.getMachinesPerPrecinct()
    #for key in map3:
     #   for key2 in mmp:
      #      for i in range(len(mmp[key2])):
       #         if mmp[key2][i] == key:
        #            map3[key].append(key2)
        #print key, map3[key]
            
#TEST THE FUNCTION
close_nm_PEB()
