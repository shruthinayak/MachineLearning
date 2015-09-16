import operator
import utilities as util
import sys
execfile("utilities.py")
count = 0
attrList = []
class Node(object):
    name = ""
    childNode0 = None
    childNode1 = None
    attributes=[]
    
    def __init__(self, featureSet):
        self.featureSet = featureSet
        self.classSet = [item.get('Class') for item in featureSet]
    
    def getFeatureVectorsForAttr(self, attrName, sign=1):
        featuresForAttr = []
        for item in self.featureSet:
            if item.get(attrName) == sign:
                featuresForAttr.append(item)
        return featuresForAttr
    
    
    def printtree(self, count):
        if self.childNode0 != None:
            s = "| "*(count+1)
            print s,
            print (self.name), "=", "0", ":"
            self.childNode0.printtree(count+1)
        if self.childNode1 != None:
            s = "| "*(count+1)
            print s,
            print(self.name), "=", "1", ":"
            self.childNode1.printtree(count+1)
        if self.childNode0 == None or self.childNode1 == None:
            sys.stdout.write('\033[F')
            print self.name
            
        

def pickBestAttr(node): 
    node.entropy = round(util.classEntropy(node.classSet), 4)
    infGainAttr = {}
    for attrName in node.attributes:
        if not attrName == 'Class':
            attrValuesPos = node.getFeatureVectorsForAttr(attrName, 1)
            attrValuesNeg = node.getFeatureVectorsForAttr(attrName, 0)
            classEntGivenAttr = util.calculateClassEntropyGivenAttr(attrName, attrValuesPos, attrValuesNeg)
            if(node.entropy - classEntGivenAttr) > 0:
                infGainAttr[attrName] = round(node.entropy - round(util.calculateClassEntropyGivenAttr(attrName, attrValuesPos, attrValuesNeg), 4), 4)
    
    if len(infGainAttr):
        sorted_x = sorted(infGainAttr.items(), key=operator.itemgetter(1))
        return sorted_x[-1][0]
    return ""

def id3(I, O, T): #I: AttributeSet O: Discrimating attr T: Target Set
    src = Node(T)
    src.attributes = list(I)
    if len(T)==0:
        n = Node([])
        n.name = "Failure"
        return n

    if(len(set(src.classSet))==1):
        n = Node([])
        n.name = set(src.classSet).pop()
        return n
        
    if(len(I)==0):
        class0 = [item.get('Class') for item in T].count(0)
        class1 = [item.get('Class') for item in T].count(1)
        n = Node([])
        n.name = "0" if class0>class1 else "1"
        return n
    
    X = pickBestAttr(src)
    #print X
    if(len(X)>1):
        src.name = X
        src.attributes.remove(X)
        src.childNode0 = id3(src.attributes, X, src.getFeatureVectorsForAttr(X, 0))
        src.childNode1 = id3(src.attributes, X, src.getFeatureVectorsForAttr(X, 1))
    return src


featureSet = util.parseLines(sys.argv[1])
attrList = list(util.headers)
rootNode = id3(attrList, None, featureSet)
rootNode.printtree(0)