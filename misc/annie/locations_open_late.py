import analysis_places_open_late
import os
import sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import ballotImage
import auditLog

class locationsOpenLate:
	def __init__(self, fha, fhb):
        self.a = auditLog.AuditLog(fha)
        self.b = ballotImage.BallotImage(fhb)
        path = '/home/annie/audit-bear/misc/annie/colleton_co_02_01_11_el152.lst'
		self.data = analysis_places_open_late.readData(path)		

	def open_late_precinctNum(self):
		dic2 = analysis_places_open_late.open_late(self.data)
		pMap = {}
		for key in dic2:
			if self.b.machinePrecinctNumMap.has_key(key):
				pMap[self.b.machinePrecinctNumMap[key]] = dic2[key]


		for key2 in pMap:
			print key2, pMap[key2]

		#return pMap
