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
    mapNM = {}
    non_master = False

#This for loop finds the machines closed on a non-master PEB and creates a #dictionary which includes serial number (key) and values of PEB serial number, #date and time and total votes cast on the machine
    for line in parsedLog:
        if not line[0] in mapNM:
            count = 0
            non_master = False
            mapNM[line[0]] = []
        if line[4] in "0001206":
            non_master = True
            mapNM[line[0]].append(line[1])
            mapNM[line[0]].append(line[3])
        if line[4] in "0001510" or line[4] in "0001511":
            count += 1
        if line[4] in "0001673" and non_master:
            mapNM[line[0]].append(count)
    
    map2 = {}
 
#This for loop verifies the machines that have the event 0001206 and stores it #in a new map, the machines that don't have the event 0001206 are excluded if #the condition in the loop is False.
    for key in mapNM:
        if len(mapNM[key]) is not 0:
            map2[key] = mapNM[key]
            #print key, map2[key]

    map3 = {}
    earlyVotingList = parsedBallotImage.getEarlyVotingList()

#This for loop excludes the early voting machines, and stored the other machines
#in another map. 
    for key in map2:
        if not key in earlyVotingList:
            map3[key] = map2[key]
            #print key, map3[key]
    
    precinctNumMap = parsedBallotImage.getPrecinctNumMap()

#This for loop finds the precinct number of each machine in map3, and
#append it in map3.
    for key2 in map3:
        if precinctNumMap.has_key(key2):
            map3[key2].append(precinctNumMap[key2])
        print key2, map3[key2]
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
#close_nm_PEB()
