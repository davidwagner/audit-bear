import os
import sys
cmd_folder = os.getenv('HOME') + '/audit-bear/misc'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import analysis_places_open_late2
cmd_folder2 = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder2 not in sys.path:
    sys.path.insert(0, cmd_folder2)
import ballotImage
import auditLog

class locations:
    def __init__(self, fha, fhb):
        self.a = auditLog.AuditLog(fha)
        self.b = ballotImage.BallotImage(fhb)
        path = '/home/annie/audit-bear/misc/annie/colleton_co_02_01_11_el152.lst'
        self.data = analysis_places_open_late.readData(path)

    def openLatePrecinctNum(self):
        m = analysis_places_open_late.open_late(self.data)
        pMap = {}
        for key in m:
            if self.b.machinePrecinctNumMap.has_key(key):
                pMap[self.b.machinePrecinctNumMap[key]] = m[key]
        for key2 in pMap:
            print key2, pMap[key2]
