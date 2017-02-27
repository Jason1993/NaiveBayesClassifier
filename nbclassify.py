import os
import sys
import re
from math import log

#file1 = open(sys.argv[1], "r")
#test = file1.read().splitlines()

file1 = open("nbtest.txt","r")

file2 = open("nbmodel.txt","r")
index = 0
priorDecptive = 0
priorTruthful = 0
priorPositive = 0
priorNegative = 0
featNum = 0
DecProb = {}
TruProb = {}
PosProb = {}
NegProb = {}

for line in file2:
    line = line.strip()
    if (index == 0):
        priorDecptive = float(line)
    if (index == 1):
        priorTruthful = float(line)
    if (index == 2):
        priorPositive = float(line)
    if (index == 3):
        priorNegative = float(line)
    if (index == 4):
        featNum = int(line)
    if (index > 4 and index < featNum+5):
        item = line.split(" ")
        DecProb[item[0]] = float(item[1])
    if ( index >= featNum+5 and index < 2*featNum+5):
        item = line.split(" ")
        TruProb[item[0]] = float(item[1])
    if ( index >= 2*featNum+5 and index < 3*featNum+5):
        item = line.split(" ")
        PosProb[item[0]] = float(item[1])
    if ( index >= 3*featNum+5 and index < 4*featNum+5):
        item = line.split(" ")
        NegProb[item[0]] = float(item[1])
    index += 1
file2.close()


input_file=open("nboutput.txt", "w")
for line in file1:
    line = line.strip()
    tempword = line.split(" ")
    id  = tempword[0]
    score1 = log(priorDecptive)
    score2 = log(priorTruthful)
    score3 = log(priorPositive)
    score4 = log(priorNegative)

    i = 1
    for i in range(len(tempword)):
        tolower = tempword[i].lower()
        word = re.sub("[^a-z']+","",tolower)
        if (word in DecProb):
            score1 += log(float(DecProb[word]))
            score2 += log(float(TruProb[word]))
        if (word in PosProb):
            score3 += log(float(PosProb[word]))
            score4 += log(float(NegProb[word]))
    if (score1 > score2):
        label1 = "deceptive"
    else:
        label1 = "truthful"
    if (score3 > score4):
        label2 = "positive"
    else:
        label2 = "negative"
    input_file.write(str(id)+" "+label1+" "+label2+"\n")

file1.close()
input_file.close()