import math
import pdb
headers = []
def parseLines(filename):
    f = open(filename)
    global headers
    headers = f.readline().strip().split(",")
    lines = f.readlines()
    f.close()
    
    featureSet = []
    classSet = []
    for line in lines:
        values = map(int, line.strip().split(","))
        feature = dict(zip(headers, values))
        featureSet.append(feature)
    return featureSet

def classEntropy(listValues):
    datasize = len(listValues) * 1.0
    pos = len([i for i in listValues if i == 1])
    pa = pos / datasize
    pb = (datasize - pos) / datasize
    return calculateEntropy(pa, pb)

def calculateEntropy(pa, pb):
    if pa != 0.0 and pb != 0.0:
        return -pa * math.log(pa, 2) - pb * math.log(pb, 2)
    return 1

def calculateClassEntropyGivenAttr(headerName, attrValuesPos, attrValuesNeg):
    sizePos = len(attrValuesPos) * 1.0
    sizeNeg = len(attrValuesNeg) * 1.0
    if sizePos - 0.0 > 0.01 and sizeNeg - 0.0 > 0.01:
        posInstance1 = 0
        posInstance0 = 0
        negInstance1 = 0
        negInstance0 = 0
        for item in attrValuesPos:
            if item.get(headerName) == 1 and item.get('Class') == 1:
                posInstance1 = posInstance1 + 1
            else:
                negInstance1 = negInstance1 + 1
            
        for item in attrValuesNeg:
            if item.get(headerName) == 0 and item.get('Class') == 1:
                posInstance0 = posInstance0 + 1
            else:
                negInstance0 = negInstance0 + 1

        totalDataSize = sizePos + sizeNeg         
        
        posEntropy = sizePos / totalDataSize * calculateEntropy(posInstance1 / sizePos, negInstance1 / sizePos)
        negEntropy = sizeNeg / totalDataSize * calculateEntropy(posInstance0 / sizeNeg, negInstance0 / sizeNeg)
        
        return (posEntropy + negEntropy)
    return 1
