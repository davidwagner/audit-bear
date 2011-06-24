import analysis_places_open_late
import ballotImageParser
import analysis

class locationsOpenLate:
	def __init__(self, string152, string155, path):
		self.b = ballotImageParser.BallotImageParser(string155,string152)
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
