import numpy as np
import matplotlib.pyplot as plt
import string as stri
import dateutil.parser
import datetime
import matplotlib
import math
import operator

class AnomalousEvents:
	def __init__(self, string, string2):
		file = open(string, 'r')
		currentMachine = None
		list = []
		dataList = []
		for line in file:
			list.append(line)
		for l in list:
			s = l.split(" ")
			if len(s[0]) == 7:
				currentMachine = s[0]
				if len(s[2]) < 6:
					tempList = []
					tempList.extend([currentMachine, s[12], s[13], s[16]])
					dataList.append(tempList)
				elif len(s[2]) == 6:
					tempList = []
					tempList.extend([currentMachine, s[7], s[8], s[11]])
					dataList.append(tempList)
			elif len(s) > 10 and len(s[9]) == 6:
				tempList = []
				tempList.extend([currentMachine, s[14], s[15], s[18]])
				dataList.append(tempList)
			elif len(s) > 10 and s[9] == '0':
				tempList = []
				tempList.extend([currentMachine, s[19], s[20], s[23]])
				dataList.append(tempList)
			elif s[0:17] == ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''] and len(s[17]) == 3:
				if s[20] == '00/00/00':
					tempList = []
					tempList.extend([currentMachine, s[20], s[23], s[26]])
					dataList.append(tempList)
				else:
					tempList = []
					tempList.extend([currentMachine, s[20], s[21], s[24]])
					dataList.append(tempList)
		self.list = dataList

	def getList(self):
		return self.list

	def getNumMachinesWithEvents(self):
		emMap = {}
		emMap2 = {}
		emList = []
		labelSequence = ()
		spaceSequence = ()
		currSpace = 0
		for x in self.list:
			if emMap.has_key(x[3]):
				if x[0] in emMap[x[3]]:
					continue
				else:
					emMap[x[3]] += [x[0]]
			else:
				emMap[x[3]] = [x[0]]
		for x2 in emMap:
			emMap2[x2] = len(emMap[x2])
		fig = plt.figure(figsize=(22,14))
		ax2 = fig.add_axes([0.15, 0.1, .7, .8])
		n, bins, patches = plt.hist(emMap2.values(), bins=20, range=(0,400))	
		for i,b in enumerate(bins):
			incr = (bins[len(bins)-1])/(len(bins)-1)
			if i == 0:
				spaceSequence += (incr/2,)
				currSpace = incr/2
				continue
			else:			
				s = '%.0f-%.0f' % (bins[i-1], bins[i]-1)
				tempTuple = (s)
				labelSequence += (tempTuple,)
				spaceSequence += ((currSpace+(incr)),)
				currSpace = currSpace+(incr)
		ax2.set_xticklabels(labelSequence)
		ax2.set_xticks(spaceSequence)	
		ax2.set_xlabel('# of Machines')
		ax2.set_ylabel('# of Events')
		ax2.set_title('Machines with each Event')	
		plt.show()
		#for y in emMap:
		#	print y, emMap[y]

	def getNumMachinesPerEvent(self):
		emMap = {}
		emMap2 = {}
		emList = []
		for x in self.list:
			if emMap.has_key(x[3]):
				if x[0] in emMap[x[3]]:
					continue
				else:
					emMap[x[3]] += [x[0]]
			else:
				emMap[x[3]] = [x[0]]
		for x2 in emMap:
			emMap2[x2] = len(emMap[x2])

		emList = sorted(emMap2.iteritems(), key=operator.itemgetter(1))

		for x3 in emList:
			#print x3[0], x3[1]
			if x3[1] == 1:
				print "Machine %s has 1 occurence of event %s" % (emMap[x3[0]][0], x3[0])
		
		#fig = plt.figure(figsize=(22,10))
		#ax2 = fig.add_axes([0.1, 0.1, .8, .8])
		#matplotlib.pyplot.plot(emMap2.keys(), emMap2.values(), '.')
		#ax2.set_xlabel('Event')
		#ax2.set_ylabel('# of Machines')
		#ax2.set_title('Number of Machines with Each Event')	
		#plt.show()
	
	def getThroughput(self):
		mpMap = self.b.getMachinesPerPrecinct()
		throughputMap = {}
		locationMap = self.b.machinePrecinctNumMap
		locationMap2 = self.b.getMachinesPerPrecinct()
		for x in self.list:
			#if not locationMap.has_key(x[0]):
			#	print x[0]
			if x[1] == '11/02/2010':
				if x[3] == '0001510'and locationMap.has_key(x[0]) or x[3] == '0001511' and locationMap.has_key(x[0]):
					if x[1] != '11/02/2010':
						print x[1]
					location = locationMap[x[0]]
					if throughputMap.has_key(location):
						s1 = x[2].split(":")
						if throughputMap[locationMap[x[0]]].has_key(stri.atoi(s1[0])):
							temp = throughputMap[locationMap[x[0]]][stri.atoi(s1[0])]
							temp = temp + 1
							throughputMap[locationMap[x[0]]][stri.atoi(s1[0])] = temp
						else:
							throughputMap[locationMap[x[0]]][stri.atoi(s1[0])] = 1
					else:
						s2 = x[2].split(":")
						tempMap = {}
						tempMap[stri.atoi(s2[0])] = 1
						throughputMap[locationMap[x[0]]] = tempMap
		for y in throughputMap:
			for y2 in throughputMap[y]:
				t = throughputMap[y][y2]
				t = t/len(locationMap2[y])
				throughputMap[y][y2] = t
		fig = plt.figure(figsize=(22,10))
		ax2 = fig.add_axes([0.1, 0.1, .8, .8])
		matplotlib.pyplot.plot(throughputMap[throughputMap.keys()[15]].keys(), throughputMap[throughputMap.keys()[15]].values())
		ax2.set_xlabel('Time')
		ax2.set_ylabel('# of Votes Per Machine')
		ax2.set_title('Throughput for Precinct %s Every Hour' % (throughputMap.keys()[15],))	
		plt.show()
		#for z in throughputMap:
		#	print z, throughputMap[z]

	def eventParser(self, string):
		file = open(string, 'r')
		list = []
		eList = []
		eMap = {}
		for line in file:
			list.append(line)
		for l in list:
			t = l.split("   ")
			s = l.split(" ")
			if len(s[0]) == 7:
				if s[7] == '00/00/00':
					if t[3] in eList:
						continue
					else:
						eList.append(t[3])
				elif len(s[2]) < 6 and len(t) > 7:
					if t[7] in eList:
						continue
					else:
						eList.append(t[7])
				elif len(s[2]) == 6:
					if t[2] in eList:
						continue
					else:
						eList.append(t[2])
			elif len(s) > 10 and len(s[9]) == 6:
				if t[5] in eList:
					continue
				else:
					eList.append(t[5])
			elif len(s) > 10 and s[9] == '0':
				if t[4] in eList:
					continue
				else:
					eList.append(t[4])
			elif s[0:17] == ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''] and len(s[17]) == 3:
				if s[20] == '00/00/00':
					if t[8] in eList:
						continue
					else:
						eList.append(t[8])
				else:
					if t[7] in eList:
						continue
					else:
						eList.append(t[7])


		for x in eList:
			temp = ''
			y = x.split(" ")
			n = y[0]
			del y[0]
			for x2 in y:
				temp += x2+" "
			d = temp
			eMap[n] = d

		self.eMap = eMap
		fi = open("events", 'w')
		fi.write("These are the event codes and their descriptions.\n\n")
		for k in eMap:
			if k == '':
				continue
			else:
				l = "%s  :  %s\n" % (k, eMap[k])
				fi.write(l)
		
	#def getEventCountOrderedList(self):
		

	def getShutdownTimes(self):
		#sdTimePlotMap = {}
		sdTimeMap = {}	#<time, # of occurrences>
		sdMachineTimeMap = {}	#<machine, time of shutdown>
		count = 0
		for x in self.list:
			if x[3] == '0001628':
				t = x[2].split(":")
				if stri.atoi(t[0]) > 7 and stri.atoi(t[0]) < 19:
					sdMachineTimeMap[x[0]] = x[2]
					count = count + 1
				if sdTimeMap.has_key(x[2]):
					temp = sdTimeMap[x[2]]
					temp = temp + 1
					sdTimeMap[x[2]] = temp
				else:
					sdTimeMap[x[2]] = 1
		print count
		for m in sdMachineTimeMap:
			print m, sdMachineTimeMap[m]
#		for t in sdTimeMap.keys():
#			datetime = "11/11/1111 "+t
#			dt = matplotlib.dates.date2num(dateutil.parser.parse(datetime))
#			sdTimePlotMap[dt] = sdTimeMap[t]
#		fig = plt.figure(figsize=(22,10))
#		ax2 = fig.add_axes([0.1, 0.1, .8, .8])
#		matplotlib.pyplot.plot_date(sdTimePlotMap.keys(), sdTimePlotMap.values())
#		ax2.set_xlabel('Time')
#		ax2.set_ylabel('Frequency')
#		ax2.set_title('Machine Shutdown Times')	
#		plt.show()

	def getAnomalousEvents(self, string):
		#events to check for:
			#0001518 Vote cancelled - terminal problem
			#0002400 PEB access failed
			#0001635 Terminal shutdown - IPS exit
			#0000712 Election ID data mismatch - PEB vs CF
			#0000706 Failed to retrieve EQC from PEB
			#0001003 Failed to get PEB ballot header block
			#0000713 Failed to get PEB EQC block
			#0002406 Failed to get PEB revision
			#0002405 Failed to get PEB type
			#0001302 Failed to get PEB vote header block
			#0001702 Invalid PEB for procedure
			#0001656 Set terminal date and/or time
			#0001655 Terminal touch-screen recalibrated
			#0002210 PEB block CRC error
			#0001725 PEB not prepared for polls
			#0001634 Terminal shutdown - DIE exit

			#0001718 PEB pulled during PEB block read
			#0001720 PEB pulled during PEB block verify
			#0001721 PEB pulled while getting PEB type

			#0001628 Warning - terminal closed early
			#0001703 Warning - PEB I/O flag set
			#0001704 Warning - I/O flagged PEB will be used
			#0001651 Warning - cannot read terminal screen
		eventOccurrencesMap = {}
		anomalousEventsMap = {}
		meMap = {}
		mean = 0
		p = 0
		stdev = 0
		for x in self.list:
			if x[3] == '0001518' or x[3] == '0002400' or x[3] == '0001635' or x[3] == '0000712' or x[3] == '0000706' or x[3] == '0001003' or x[3] == '0000713' or x[3] == '0002406' or x[3] == '0002405' or x[3] == '0001302' or x[3] == '0001702' or x[3] == '0001656' or x[3] == '0001655' or x[3] == '0002210' or x[3] == '0001725' or x[3] == '0001634' or x[3] == '0001718' or x[3] == '0001720' or x[3] == '0001721' or x[3] == '0001628' or x[3] == '0001703' or x[3] == '0001704' or x[3] == '0001651':
				if meMap.has_key(x[0]):
					if meMap[x[0]].has_key(x[3]):
						temp = meMap[x[0]][x[3]]
						temp = temp + 1
						meMap[x[0]][x[3]] = temp
					else:
						meMap[x[0]][x[3]] = 1
				else:
					tMap = {}
					tMap[x[3]] = 1
					meMap[x[0]] = tMap
			if eventOccurrencesMap.has_key(x[3]) and x[3] != '0001510':
				temp = eventOccurrencesMap[x[3]]
				temp = temp + 1
				eventOccurrencesMap[x[3]] = temp
			elif x[3] != '0001510':
				eventOccurrencesMap[x[3]] = 1
		for m in eventOccurrencesMap.values():
			mean = mean + m
		mean = mean / len(eventOccurrencesMap.values())
		for m2 in eventOccurrencesMap.values():
			p = p + ((m2-mean)**2)
		stdev = math.sqrt(p/len(eventOccurrencesMap.values()))
		for e in eventOccurrencesMap:
			if eventOccurrencesMap[e] < (mean-(4*stdev)) or eventOccurrencesMap[e] > ((4*stdev)+mean):
				anomalousEventsMap[e] = eventOccurrencesMap[e]
		self.eventParser(string)
		f = open("eventAnomalies", 'w')
		f.write("This is an Anomalous Events Report for Anderson County\n\n")
		for me in meMap:
			l1 = "There may be a problem with machine %s because it exhibited the following behavior:\n" % (me,)
			f.write(l1)
			print "There may be a problem with machine %s because it exhibited the following behavior:\n" % (me,)
			for me2 in meMap[me]:
				l2 = "%d instances of event %s : %s" % (meMap[me][me2], me2, self.eMap[me2])
				f.write(l2)
				print "%d instances of event %s : %s" % (meMap[me][me2], me2, self.eMap[me2])
			print "\n"
			f.write("\n")
			#print me, meMap[me]
		
