import os, sys
cmd_folder = os.getenv('HOME') + '/audit-bear/modules'
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import auditLog
import ballotImage

class Bottleneck:

    def __init__(self, fha, fhb):
        self.a = auditLog.AuditLog(fha)
        self.b = ballotImage.BallotImage(fhb)

    """
    This function gets the average throughput per hour of all the machines in one polling location.  It displays the information on a graph.  Currently, the precinct number is hard-coded into the function (this could change).
    """
    def getThroughput(self):
        mpMap = self.b.getMachinesPerPrecinct()
        throughputMap = {}
        locationMap = self.b.machinePrecinctNumMap
        locationMap2 = self.b.getMachinesPerPrecinct()

        for x in self.a.getEntryList():
            d = x.dateTime.split(" ")
            date = d[0]
            time = d[1]
            if date == '11/02/2010':
                if (x.eventNumber == '0001510' and locationMap.has_key(x.serialNumber)) or (x.eventNumber == '0001511' and locationMap.has_key(x.serialNumber)):
                    location = locationMap[x.serialNumber]
                    if throughputMap.has_key(location):
                        s1 = time.split(":")
                        if throughputMap[locationMap[x.serialNumber]].has_key(stri.atoi(s1[0])):
                            temp = throughputMap[locationMap[x.serialNumber]][stri.atoi(s1[0])]
                            temp = temp + 1
                            throughputMap[locationMap[x.serialNumber]][stri.atoi(s1[0])] = temp
                        else:
                            throughputMap[locationMap[x.serialNumber]][stri.atoi(s1[0])] = 1
                    else:
                        s2 = time.split(":")
                        tempMap = {}
                        tempMap[stri.atoi(s2[0])] = 1
                        throughputMap[locationMap[x.serialNumber]] = tempMap
        for y in throughputMap:
            for y2 in throughputMap[y]:
                t = throughputMap[y][y2]
                t = t/len(locationMap2[y])
                throughputMap[y][y2] = t 
        #for z in throughputMap:
           #print z, throughputMap[z]
        fig = plt.figure(figsize=(22,10))
        ax2 = fig.add_axes([0.1, 0.1, .8, .8])
        matplotlib.pyplot.plot(throughputMap[throughputMap.keys()[15]].keys(), throughputMap[throughputMap.keys()[15]].values())
        ax2.set_xlabel('Time')
        ax2.set_ylabel('# of Votes Per Machine')
        ax2.set_title('Throughput for Precinct %s Every Hour' % (throughputMap.keys()[15],))
        plt.show()
