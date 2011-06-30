#!/usr/bin/python

import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from auditLog import AuditLog   #imports audit log class
from ballotImage import BallotImage  #imports ballot image class
from el68a import EL68A
from closeNonMasterPEB import close_nm_PEB
path = sys.argv[1]
path2 = sys.argv[2]
path3 = sys.argv[3]

parsedLog = AuditLog(open(path, 'r'))
parsedBallotImage = BallotImage(open(path2, 'r'))
parsed68 = EL68A(open(path3, 'r'))

masterPEBs, nonMasterPEBs = close_nm_PEB(parsedLog, parsedBallotImage)
pebToPrecinctCount = parsed68.pebToPrecinctCountMap

strippedMasterPEBsList = []
strippedNonMasterPEBsList = []
allPEBsList = []

for key in masterPEBs:
    peb = masterPEBs[key][0]
    if not peb in strippedMasterPEBsList:
        strippedMasterPEBsList.append(peb)
        allPEBsList.append(peb)

for key in nonMasterPEBs:
    peb = nonMasterPEBs[key][0]
    if not peb in strippedNonMasterPEBsList:
        strippedNonMasterPEBsList.append(peb)
        allPEBsList.append(peb)

excludedPEBs = []
for peb in allPEBsList:
    if not peb in pebToPrecinctCount.keys():
        excludedPEBs.append(peb)
        print "excludedPEBs: " + peb

excludedPEBs2 = []
for peb in pebToPrecinctCount.keys():
    if not peb in allPEBsList:
        excludedPEBs2.append(peb)
        print "excludedPEBs2: " + peb


print "excludedPEBs", len(excludedPEBs)
print "excludedPEBs2", len(excludedPEBs2)
