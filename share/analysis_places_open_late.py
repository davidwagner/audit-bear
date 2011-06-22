#Created by Keishla and Ana

#read the audit log file and store each line in the data list.
def readData(path):
    data = []
    inputFile = open(path, "r")
    for line in inputFile:
        if line[0] == "5":
            data.append(line.split())
            last = line.split()[0:2]
        elif line[0] == ' ':
            if '0' < line[9] <= '9':
                data.append([last[0]] + line.split())
            elif line[9] == ' ':
                data.append(last[0:2] + line.split())
        else:
            continue
    inputFile.close()
    return data

#create two dictionaries which keys are the serial numbers and the values of the first one is a list with the time of each vote cast by voter or poll worker.
#The second dictionary contains the serial numbers as keys and the difference between the last vote and the closing time (7:00 PM) as values,
#to determine if the machine was open late (after 7:00PM).
def open_late(data):
    
    import dateutil.parser
    import datetime
    dic = {}
    dic2 = {}
    
    for line in data:
        if not line[0] in dic:
            dic[line[0]] = []
            dic2[line[0]] = ""
        if line[5] in "0001510" or line[5] in "0001511":
            dic[line[0]].insert(0, line[3] + " "+line[4])
            try:
                t2 = dateutil.parser.parse(dic[line[0]][0])
                t1 = dateutil.parser.parse(dic[line[0]][0][:10]+ " 19:00:00")
            except:
                continue
            else:
                delta = t2 - t1
                dic2[line[0]] = str(delta)
    return dic2

#creates the graph, which shows how many machines were open late.
def graphOpenLate(dic):
    import numpy as np
    import matplotlib.pyplot as plt
    c = 0
    dicRange = {'0:00:00':0, '0:15:00':0, '0:30:00':0, '0:45:00':0, '1:00:00':0, '1:15:00':0, '1:30:00':0, '1:45:00':0, '2:00:00':0, '2:15:00':0, '2:30:00':0, '2:45:00':0}
    for s in dic:
        if dic[s][:2] == '' or dic[s][:2] == "-1":
            c+=1
        elif ('0:00:00' <= dic[s] < '0:15:00'):
            dicRange['0:00:00']+=1
        elif '0:15:00' <= dic[s] < '0:30:00':
            dicRange['0:15:00']+=1
        elif '0:30:00' <= dic[s] < '0:45:00':
            dicRange['0:30:00']+=1
        elif '0:45:00' <= dic[s] < '1:00:00':
            dicRange['0:45:00']+=1
        elif '1:00:00' <= dic[s] < '1:15:00':
            dicRange['1:00:00']+=1
        elif '1:15:00' <= dic[s] < '1:30:00':
            dicRange['1:15:00']+=1
        elif '1:30:00' <= dic[s] < '1:45:00':
            dicRange['1:30:00']+=1
        elif '1:45:00' <= dic[s] < '2:00:00':
            dicRange['1:45:00']+=1
        elif '2:00:00' <= dic[s] < '2:15:00':
            dicRange['2:00:00']+=1
        elif '2:15:00' <= dic[s] < '2:30:00':
            dicRange['2:15:00']+=1
        elif '2:30:00' <= dic[s] < '2:45:00':
            dicRange['2:30:00']+=1

    kList = []
    vList = []
    
    for k in sorted(dicRange.keys()):
        kList.append(k)
        vList.append(dicRange[k])
        
    N = 12
    ind = np.arange(N)
    width = 0.70
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, vList, .98, color='r')
    ax.set_xticks(ind+width/100.)
    ax.set_xticklabels(kList)
    ax.set_yticks(np.arange(0,max(vList)+10, 10))
    ax.set_ylabel('Number of units')
    ax.set_xlabel('Time Opened')
    ax.set_title('Machines stayed open after 7:00PM')
    plt.grid(True)
    plt.show()
    return

#main program
import dateutil.parser
import datetime
data = readData("greenville_co_03_08_11_el152.txt")
dicTC = open_late(data)
graphOpenLate(dicTC)

for key in dicTC:
   if dicTC[key] == '' or dicTC[key][:2] == "-1":
       continue
   else:
       print "Machine #"+ key + " was open late " + dicTC[key]+ " hours."
