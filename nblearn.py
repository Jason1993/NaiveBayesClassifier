from __future__ import division
import os
import sys
from os import listdir
from os.path import isfile, join
import operator
import re
from math import log


def mutualVal(n11,n01,n10,n00):
    N = n11 + n01 + n10 + n00
    n1p = n10 + n11
    n0p = n00 + n01
    np1 = n01 + n11
    np0 = n10 + n00
    mutemp1 = N*(n11)/(n1p*np1)
    mutemp2 = N*n01/(n0p*np1)
    mutemp3 = N*n10/(n1p*np0)
    mutemp4 = N*n00/(n0p*np0)
    if (n11 == 0):
        restemp1 = 0
    else:
        restemp1 = n11/N*log(mutemp1,2)
    if (n01 == 0):
        restemp2 = 0
    else:
        restemp2 = n01/N*log(mutemp2,2)
    if (n10 == 0):
        restemp3 = 0
    else:
        restemp3 = n10/N*log(mutemp3,2)
    if (n00 == 0):
        restemp4 = 0
    else:
        restemp4 = n00/N*log(mutemp4,2)
    return restemp1+restemp2+restemp3+restemp4

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def getDecFeat(decdoc,trudoc):
    diclist = {}
    for key in decdoc:
        tempdoc = decdoc[key]
        for word in tempdoc:
            if (word in diclist):
                continue
            else:
                num11 = 0
                num10 = 0
                num01 = 0
                num00 = 0
                for item in decdoc:
                    tempcheck = decdoc[item]
                    if (word in tempcheck):
                        num11 += 1
                    else:
                        num01 += 1
                for item2 in trudoc:
                    tempcheck2 = trudoc[item2]
                    if (word in tempcheck2):
                        num10 += 1
                    else:
                        num00 += 1

                val = mutualVal(num11,num01,num10,num00)
                diclist[word] = val
    return diclist

def getPosFeat(posdoc,negdoc):
    diclist = {}
    for key in posdoc:
        tempdoc = posdoc[key]
        for word in tempdoc:
            if (word in diclist):
                continue
            else:
                num11 = 0
                num10 = 0
                num01 = 0
                num00 = 0
                for item in posdoc:
                    tempcheck = posdoc[item]
                    if (word in tempcheck):
                        num11 += 1
                    else:
                        num01 += 1
                for item2 in negdoc:
                    tempcheck2 = negdoc[item2]
                    if (word in tempcheck2):
                        num10 += 1
                    else:
                        num00 += 1

                val = mutualVal(num11,num01,num10,num00)
                diclist[word] = val
    return diclist

'''
if os.path.isdir(sys.argv[1]):
    textfile = sys.argv[1]
if os.path.isdir(sys.argv[2]):
    labelfile = sys.argv[2]
'''
file1 = open("train-text.txt","r")
file2 = open("train-labels.txt","r")

lineno = 0
#lineno = len(temp1)


id = []
content = []
for line in file1:
    line = line.strip()
    i = 0
    while (i != -1):
        if (line[i] == " "):
            id.append(line[0:i])
            number = i
            i = -1
        else:
            i += 1
    content.append(line[number+1:])
    lineno += 1
file1.close()
developno = lineno * 0.75
text = {}
i = 0
for i in range(len(id)):
    text[id[i]] = content[i]

id2 = []
content2 = []
for line in file2:
    line = line.strip()
    i = 0
    while ( i != -1):
        if ( line[i] == " "):
            id2.append(line[0:i])
            number = i
            i = -1
        else:
            i += 1
    content2.append(line[number+1:])
file2.close()
label = {}
i = 0
for i in range(len(id2)):
    label[id2[i]] = content2[i]


deceptive = 0
truthful = 0
positive = 0
negative = 0
dectotal = 0
trutotal = 0
postotal = 0
negtotal = 0
decepcount = {}
truthcount = {}
poscount = {}
negcount = {}
total = {}
decdoc = {}
trudoc = {}
posdoc = {}
negdoc = {}


i = 0
while (i < developno):

    i += 1
    current = id[i]
    templab = label[current].split(" ")
    label1 = templab[0]
    label2 = templab[1]
    tempcontent = text[id[i]].split(" ")
    extracted = []
    for k in range((len(tempcontent))):
        tempstring = tempcontent[k].lower()
        newstring = re.sub("[^a-z']+", "", tempstring)
        if newstring:
            extracted.append(newstring)
            if (newstring in total):
                total[newstring] += 1
            else:
                total[newstring] = 1
    if (label1 == "deceptive"):
        deceptive += 1
        for j in range(len(extracted)):
            if (extracted[j] in decepcount):
                decepcount[extracted[j]] += 1
            else:
                decepcount[extracted[j]] = 1
            dectotal +=1
        decdoc[current] = extracted
    else:
        truthful += 1
        for j in range(len(extracted)):
            if (extracted[j] in truthcount):
                truthcount[extracted[j]] += 1
            else:
                truthcount[extracted[j]] = 1
            trutotal += 1
        trudoc[current] = extracted
    if (label2 == "positive"):
        positive += 1
        for j in range(len(extracted)):
            if (extracted[j] in poscount):
                poscount[extracted[j]] += 1
            else:
                poscount[extracted[j]] = 1
            postotal += 1
        posdoc[current] = extracted
    else:
        negative += 1
        for j in range(len(extracted)):
            if (extracted[j] in negcount):
                negcount[extracted[j]] += 1
            else:
                negcount[extracted[j]] = 1
            negtotal += 1
        negdoc[current] = extracted

decFeat = {}
decFeat = getDecFeat(decdoc,trudoc)
decFeat_sorted = sorted(decFeat.items(),key=operator.itemgetter(1))
decFeat_sorted.reverse()
posFeat = {}
posFeat = getPosFeat(posdoc,negdoc)
posFeat_sorted = sorted(posFeat.items(),key=operator.itemgetter(1))
posFeat_sorted.reverse()

priorDec = deceptive/developno
priorTru = truthful/developno
priorPos = positive/developno
priorNeg = negative/developno
featNum = 30

decProb = {}
truProb = {}

deckinds = len(decepcount)
trukinds = len(truthcount)

for feat1 in decFeat_sorted:
    if (featNum == 0):
        break
    else:
        if (feat1[0] in decepcount):
            featno1 = decepcount[feat1[0]]
        else:
            featno1 = 0
        featProb1 = (featno1 + 1)/(dectotal + deckinds)
        decProb[feat1[0]] = featProb1
        if (feat1[0] in truthcount):
            featno2 = truthcount[feat1[0]]
        else:
            featno2 = 0
        featProb2 = (featno2 + 1)/(trutotal + trukinds)
        truProb[feat1[0]] = featProb2
        featNum -= 1

featNum2 = 30

posProb = {}
negProb = {}
poskinds = len(poscount)
negkinds = len(negcount)

for feat2 in posFeat_sorted:
    if (featNum2 == 0):
        break
    else:
        if (feat2[0] in poscount):
            featno3 = poscount[feat2[0]]
        else:
            featno3 = 0
        featProb3 = (featno3 + 1)/(postotal + poskinds)
        posProb[feat2[0]] = featProb3

        if (feat2[0] in negcount):
            featno4 = negcount[feat2[0]]
        else:
            featno4 = 0
        featProb4 = (featno4 + 1)/(negtotal + negkinds)
        negProb[feat2[0]] = featProb4
        featNum2 -= 1
'''
for test in posProb:
    if (posProb[test] > negProb[test]):
        print "Yes"
    else:
        print "No"
#print decProb["chicago"]
'''
input_file=open("nbmodel.txt", "w")
input_file.write(str(priorDec)+"\n")
input_file.write(str(priorTru)+"\n")
input_file.write(str(priorPos)+"\n")
input_file.write(str(priorNeg)+"\n")
input_file.write("30\n")
for writeitem in decProb:
    input_file.write(str(writeitem) + " " + str(decProb[writeitem]) + "\n")
for writeitem in truProb:
    input_file.write(str(writeitem) + " " + str(truProb[writeitem]) + "\n")
for writeitem in posProb:
    input_file.write(str(writeitem) + " " + str(posProb[writeitem]) + "\n")
for writeitem in negProb:
    input_file.write(str(writeitem) + " " + str(negProb[writeitem]) + "\n")
input_file.close()


def testDev():
    i = int(developno)
    dectp = 0
    decfn = 0
    decfp = 0
    trutp = 0
    trufn = 0
    trufp = 0
    postp = 0
    posfn = 0
    posfp = 0
    negtp = 0
    negfn = 0
    negfp = 0
    while (i < lineno):
        probdec = log(priorDec)
        probtru = log(priorTru)
        probpos = log(priorPos)
        probneg = log(priorNeg)
        testid = id[i]
        testcontent = text[testid].split(" ")
        for m in range(len(testcontent)):
            tempword = testcontent[m].lower()
            newtempword = re.sub("[^a-z']+", "", tempword)
            if (newtempword in decProb):
                probdec += log(decProb[newtempword])
                probtru += log(truProb[newtempword])
            if (newtempword in posProb):
                probpos += log(posProb[newtempword])
                probneg += log(negProb[newtempword])
        testlabel1 = label[testid].split(" ")[0]
        print probdec,probtru
        if (probdec > probtru):
            if (testlabel1 == "deceptive"):
                dectp += 1
            else:
                decfp += 1
                trufn += 1
        else:
            if (testlabel1 == "truthful"):
                trutp += 1
            else:
                trufp += 1
                decfn += 1
        testlabel2 = label[testid].split(" ")[1]
        if (probpos > probneg):
            if (testlabel2 == "positive"):
                postp += 1
            else:
                posfp += 1
                negfn += 1
        else:
            if (testlabel2 == "negative"):
                negtp += 1
            else:
                negfp += 1
                posfn += 1
        i += 1
    decpre = dectp/(dectp+decfp)
    decrecall = dectp/(dectp+decfn)
    f1dec = 2*decpre*decrecall/(decpre+decrecall)

    trupre = trutp/(trutp+trufp)
    trurecall = trutp/(trutp+trufn)
    f1tru = 2*trupre*trurecall/(trupre+trurecall)

    pospre = postp/(postp+posfp)
    posrecall = postp/(postp+posfn)
    f1pos = 2*pospre*posrecall/(pospre+posrecall)

    negpre = negtp/(negtp+negfp)
    negrecall = negtp/(negtp+negfn)
    f1neg = 2*negpre*negrecall/(negpre+negrecall)

    return (f1dec+f1tru+f1pos+f1neg)/4

testDev()