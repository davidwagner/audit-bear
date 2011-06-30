#!/usr/bin/python

#Determine the machines that have 0 votes.
def unusedMachines(parsedLog):
    mapM = {}

    for line in parsedLog:
        if not line[0] in mapM:
            mapM[line[0]] = 0
        if line[4] == "0001510" or line[4] == "0001511":
            mapM[line[0]] += 1
    
    #print mapM.items()
    #append in the macUnused list the machines that have 0 votes.
    macUnused = []
    for key in mapM:
        if mapM[key] == 0:
            macUnused.append(key)

    #print the machines that have 0 votes (if any)
    print "Machines with zero votes"
    if len(macUnused) == 0:
        print "All the machines have votes."
    for m in macUnused:
        print m
    return macUnused


#TEST THE FUNCTION
#import os, sys
#cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
#if cmd_folder not in sys.path:
    #sys.path.insert(0, cmd_folder)

#from auditLog import AuditLog
    
#path = sys.argv[1]
#parsedLog = AuditLog(open(path, "r"))
#pMap = unusedMachines(parsedLog)
