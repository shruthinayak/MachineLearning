import operator
import copy
import utilities as util
import random
import sys
execfile("utilities.py")
nonleaf = []
count = 0
found = False
class Node(object):
    name = ""
    childNode0 = None
    childNode1 = None
    attributes = []
    entropy = 2
    
    def __init__(self, featureSet):
        self.featureSet = featureSet
        self.classSet = [item.get('Class') for item in featureSet]
        if(len(self.classSet) > 1):
            self.classEntropy()
    
    def getFeatureVectorsForAttr(self, attrName, sign=1):
        featuresForAttr = []
        for item in self.featureSet:
            if item.get(attrName) == sign:
                featuresForAttr.append(item)
        return featuresForAttr
    
    def classEntropy(self):
        datasize = len(self.classSet) * 1.0
        pos = self.classSet.count(1)
        pa = pos / datasize
        pb = (datasize - pos) / datasize
        self.entropy = round(util.calculateEntropy(pa, pb), 4)
    
    def printtree(self, count):
        if self.childNode0 != None:
            s = "| "*(count + 1)
            print s,
            if(self.childNode0.childNode0!=None):
                print (self.name), "=", "0", ":"
            else:
                print (self.name), "=", "0", ":",
            self.childNode0.printtree(count + 1)
        else: 
            print self.name
        if self.childNode1 != None:
            s = "| "*(count + 1)
            print s,
            if(self.childNode1.childNode1!=None):
                print (self.name), "=", "1", ":"
            else:
                print (self.name), "=", "1", ":",
            self.childNode1.printtree(count + 1)     

            
    def pickBestAttr(self): 
        infGainAttr = {}
        
        for attrName in self.attributes:
            if not attrName == 'Class':
                attrValuesPos = self.getFeatureVectorsForAttr(attrName, 1)
                attrValuesNeg = self.getFeatureVectorsForAttr(attrName, 0)
                classEntGivenAttr = util.calculateClassEntropyGivenAttr(attrName, attrValuesPos, attrValuesNeg)
                if(self.entropy - classEntGivenAttr) > 0:
                    infGainAttr[attrName] = round(self.entropy - util.calculateClassEntropyGivenAttr(attrName, attrValuesPos, attrValuesNeg), 4)
        if len(infGainAttr):
            sorted_x = sorted(infGainAttr.items(), key=operator.itemgetter(1))
            return sorted_x[-1][0]
        return ""
    
    def postpruning(self, l, k):
        dbest = copyTree(self)
        for i in range(1, l):
            ddash = copyTree(self) 
            m = random.randint(1, k)
            print m
            for j in range(1,m):
                global nonleaf
                nonleaf = []
                getNonLeafNodes(ddash)
                n = len(nonleaf)
                p = random.randint(1, n)-1
                chosenNode = nonleaf[p]
                class0 = chosenNode.classSet.count(0)
                class1 = chosenNode.classSet.count(1)
                chosenNode.childNode0 = None
                chosenNode.childNode1 = None
                chosenNode.name = "0" if class0 > class1 else "1"
            
                        
def copyTree(rootNode):
    if(rootNode != None):
        node = Node(rootNode.featureSet)
        node.name = rootNode.name
        node.childNode0 = copyTree(rootNode.childNode0)
        node.childNode1 = copyTree(rootNode.childNode1)
        return node
    else: 
        return None
        
def getNonLeafNodes(rootNode):
    global nonleaf
    if(rootNode.childNode0 != None or rootNode.childNode1 != None):
        nonleaf.append(rootNode)
    if rootNode.childNode0 != None:
        getNonLeafNodes(rootNode.childNode0)
    if rootNode.childNode1 != None:
        getNonLeafNodes(rootNode.childNode1)
    return

def classify(rootNode, tupledict):
    global count
    if(rootNode.childNode0 == None and rootNode.childNode1 == None):
        if(tupledict.get('Class')==0 and rootNode.name == "No"):
            count = count + 1
        elif(tupledict.get('Class')==1 and rootNode.name == "Yes"):
            count = count + 1
        return rootNode.name
    if(tupledict[rootNode.name]==0):
        classify(rootNode.childNode0, tupledict)
    else:
        classify(rootNode.childNode1, tupledict)

def id3(I, O, T):  # I: AttributeSet O: Discriminating attribute T: Target Set
    src = Node(T)
    src.attributes = list(I)
    
    if len(T) == 0:
        n = Node([])
        n.name = "Failure"
        return n

    if(len(set(src.classSet)) == 1):
        n = Node([])
        n.name = "Yes" if set(src.classSet).pop()==1 else "No"
        return n
        
    X = src.pickBestAttr()
    
    if(len(I) == 0 or len(X) < 1):
        class0 = [item.get('Class') for item in T].count(0)
        class1 = [item.get('Class') for item in T].count(1)
        n = Node([])
        n.name = "Yes" if class1 > class0 else "No"
        return n

    if(len(X) > 1):
        src.name = X
        src.attributes.remove(X)
        print src.name
        print "0:", len(src.getFeatureVectorsForAttr(X,0))
        print "1:", len(src.getFeatureVectorsForAttr(X,1)) 
        src.childNode0 = id3(src.attributes, X, src.getFeatureVectorsForAttr(X, 0))
        src.childNode1 = id3(src.attributes, X, src.getFeatureVectorsForAttr(X, 1))
    return src

featureSet = util.parseLines(sys.argv[1])
attrList = list(util.headers)
rootNode = id3(attrList, None, featureSet)
rootNode.printtree(0)
featureSet = util.parseLines(sys.argv[2])
for d in featureSet:
    classify(rootNode, d)
print 
print "Accuracy of the test data set of 2000 samples: ", count*1.0/len(featureSet)

