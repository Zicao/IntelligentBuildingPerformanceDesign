'''
Created on Mar 24, 2011
Ch 11 code
@author: Peter
'''
from numpy import *

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return C1#map(frozenset, C1)#use frozen set so we
                            #can use it as a key in a dict    

def scanD(dataSet, Ck, minSupport):
    ssCnt = {}
    i=0
    D=map(set,dataSet)
    for tid in D:
        tid = frozenset(tid)
        for can in Ck:
            canSet=frozenset(can)
            if canSet.issubset(tid):
                if not canSet in ssCnt: ssCnt[canSet]=1
                else: ssCnt[canSet] += 1
        i+=1
    numItems = float(i)
    retList = []
    supportData = {}
    for key in ssCnt:
        try:
            support = ssCnt[key]/numItems
        except (ZeroDivisionError, e):
            print("Error:", e)
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    #print("ScanD retList",retList)
    return retList, supportData

def aprioriGen(Lk, k): #creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): 
            L1 = list(Lk[i])[:k-2]; 
            L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if k==2:
                retList.append(Lk[i] | Lk[j])
            elif L1==L2: #if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j]) #set union
    return retList

def apriori(dataSet, minSupport = 0.3):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(dataSet, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(dataSet, Ck, minSupport)#scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def generateRules(L, supportData, minConf=0.7):  #supportData is a dict coming from scanD
    bigRuleList = []
    for i in range(1, len(L)):#only get the sets with two or more items
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList         

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = [] #create new list to return
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence
        if conf >= minConf: 
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > (m + 1)): #try further merging
        Hmp1 = aprioriGen(H, m+1)#create Hm+1 new candidates
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):    #need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
            
def pntRules(ruleList, itemMeaning):
    for ruleTup in ruleList:
        for item in ruleTup[0]:
            print(itemMeaning[item])
        print("           -------->")
        for item in ruleTup[1]:
            print(itemMeaning[item])
        print("confidence: %f" % ruleTup[2])
        print("\n")     #print a blank line