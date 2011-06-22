#Created by Keishla and Ana
#read the audit log file
def readData():
    data = []
    inputFile = open("anderson_co_01_14_11_el152.txt", "r")
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

#count the votes
def castVotes(listData):
    totalVotes = 0
    
    for line in listData:
        if(line[5] == "0001510" or line [5] == "0001511"):
            totalVotes += 1
    return totalVotes

#count the iVotronics
def totalMachines(listData):
    d = {}
    AllmachineList = [None] * len(listData)
    
    for x in range (len(listData)):
        AllmachineList[x] = listData[x][0]
    
    machineList = set(AllmachineList)

    return len(machineList)

#count the votes per machine
def votesPerMachine(listData):
    dic = {}
    for line in listData:
        if not line[0] in dic:
            dic[line[0]] = 0
        if line[5] in ("0001510", "0001511"):
            dic[line[0]] += 1
    return dic
#determine if the terminals were opened and/ or closed.
def machines_not_closed(listData):
    dicM = {}
    
    for line in listData:
        if not line[0] in dicM:
            dicM[line[0]] = -1
        if line[5] in ("0001672"):
            dicM[line[0]] = 0
        elif line[5] in ("0001673"):
            dicM[line[0]] = 1
    return dicM

def votesRange(sDic):
    count = {}
    rangeD = {0:0, 50:0, 100:0, 150:0, 200:0, 250:0, 300:0, 350:0, 400:0, 450:0, 500:0, 550:0, 600:0, 650:0}
    for s in sDic:
        if 0 <= sDic[s] < 50:
            rangeD[0] += 1
        elif 50 <= sDic[s] < 100:
            rangeD[50] += 1
        elif 100 <= sDic[s] < 150:
            rangeD[100] += 1
        elif 150 <= sDic[s] < 200:
            rangeD[150] += 1
        elif 200 <= sDic[s] < 250:
            rangeD[200] += 1
        elif 250 <= sDic[s] < 300:
            rangeD[250] += 1
        elif 300 <= sDic[s] < 350:
            rangeD[300] += 1
        elif 350 <= sDic[s] < 400:
            rangeD[350] += 1
        elif 400 <= sDic[s] < 450:
            rangeD[400] += 1
        elif 450 <= sDic[s] < 500:
            rangeD[450] += 1
        elif 500 <= sDic[s] < 550:
            rangeD[500] += 1
        elif 550 <= sDic[s] < 600:
            rangeD[550] += 1
        elif 600 <= sDic[s] < 650:
            rangeD[600] += 1
        elif 650 <= sDic[s] < 700:
            rangeD[650] += 1
        else:
            continue
        
    return rangeD
#Main
import string

serialList = []
votesList = []
countOpCl = 0
countOp = 0
ivo = 0 #count the machines

#invoke the functions
d = readData()
countVote = castVotes(d)
ivo = totalMachines(d)
snDic = votesPerMachine(d)
dicM = machines_not_closed(d)
dicRange = votesRange(snDic)

#print the results
for sn in snDic:
    print str(sn) + " has " + str(snDic[sn]) + " votes."
print "The total of cast votes is: ", countVote
print "The total of iVotronics used in the election is: ", ivo
for oM in dicM:
    if dicM[oM] == 0:
        print "The terminal serial number ",str(oM) + " was opened but not closed."
        countOp += 1
    elif dicM[oM] == 1:
     #   print "The terminal serial number ",str(oM) + " was opened and closed."
       countOpCl += 1
print "The total of the terminals that were opened but not closed is :", countOp
print "The total of the terminals that were opened and closed is :", countOpCl
print dicRange.items()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.figure as fig
import matplotlib.axis


plt.bar(dicRange.keys(), dicRange.values(), 50, 1)
plt.yticks(np.arange(0,max(dicRange.values())+1,10))
plt.xticks(np.arange(0,max(dicRange.keys())+51,50))
plt.ylabel('Unit range')
plt.xlabel('Total votes cast per unit')
plt.title('Histogram of machine usage')
plt.show()
