#!/usr/bin/python

#This function lists the election day terminals closed on a non-master PEB.
def closeNM_PEB(parsedLog, parsedBallotImage):
    precinctNumMap = parsedBallotImage.getPrecinctNumMap()
    PEBs = {}
    non_master = False
    for line in parsedLog:
        if precinctNumMap.has_key(line[0]):
            if not precinctNumMap[line[0]] in PEBs:
                PEBs[precinctNumMap[line[0]]] = []
                non_master = False
            if line[4] == "0001206":
                non_master = True
                PEBs[precinctNumMap[line[0]]].append(line[1])
                PEBs[precinctNumMap[line[0]]].append(non_master)
            if line[4] == "0001673" and not non_master:
                PEBs[precinctNumMap[line[0]]].append(line[1])
                PEBs[precinctNumMap[line[0]]].append(non_master)
        else:
            continue
    
    for location in PEBs:
        print location, PEBs[location]
    pMaster = {}
    pNonMaster = {}
    return
    #return (pMaster, pNonMaster)

import os, sys

cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from auditLog import AuditLog   #imports audit log class
from ballotImage import BallotImage  #imports ballot image class
import dateMod

path = sys.argv[1]
path2 = sys.argv[2]
path3 = sys.argv[3]

parsedLog = AuditLog(open(path, 'r'))
parsedBallotImage = BallotImage(open(path2, 'r'), AuditLog(open(path, 'r')), open(path3, 'r'))
closeNM_PEB(parsedLog, parsedBallotImage)
