from optparse import OptionParser
from src.models.product import Product
from src.models.transaction import TransactionProduct, Transaction
import numpy
from csv import reader
from collections import defaultdict
from itertools import chain, combinations


class FPNode:
    def __init__(self, itemName, frequency, parentNode):
        self.itemName = itemName
        self.count = frequency
        self.parent = parentNode
        self.children = {}
        self.next = None

    def increment(self, frequency):
        self.count += frequency

    def display(self, ind=1):
        print('  ' * ind, self.itemName, ' ', self.count)
        for child in list(self.children.values()):
            child.display(ind + 1)
            
            
class FPGrowth:
    def __init__(self, minimumSupportRatio, minimumConfidence):
        self.minimumSupportRatio = minimumSupportRatio
        self.minimumConfidence = minimumConfidence
        self.listOfItemset = []
        self.frequencyOfTransaction = []


    def read_data(self):
        transactionsProducts = TransactionProduct.query.all()
        
        dictOfItemset = {}
        
        for item in transactionsProducts:
            if item.transaction_id not in dictOfItemset:
                dictOfItemset[item.transaction_id] = []
                
            dictOfItemset[item.transaction_id].append(item.itemCode)
            
        
        for _, itemset in dictOfItemset.items():
            self.listOfItemset.append(itemset)
            self.frequencyOfTransaction.append(1)
    
    
    def updateHeaderTable(self, item, targetNode, headerTable):
        if headerTable[item][1] is None:
            headerTable[item][1] = targetNode
        else:
            currentNode = headerTable[item][1]
            while currentNode.next is not None:
                currentNode = currentNode.next
            currentNode.next = targetNode

    def updateTree(self, item, parentNode, headerTable):
        if item in parentNode.children:
            parentNode.children[item].increment(1)
        else:
            newItemNode = FPNode(item, 1, parentNode)
            parentNode.children[item] = newItemNode
            self.updateHeaderTable(item, newItemNode, headerTable)
        return parentNode.children[item]

    # Construct FP Tree
    def constructFPTree(self):
        headerTable = defaultdict(int)
        for i, itemset in enumerate(self.listOfItemset):
            for item in itemset:
                headerTable[item] += self.frequencyOfTransaction[i]

        headerTable = dict((item, supportValue) for item, supportValue in headerTable.items() if supportValue >= self.minimumSupportRatio)

        if len(headerTable) == 0:
            return None, None

        for item in headerTable:
            headerTable[item] = [headerTable[item], None]

        initialNode = FPNode('Null', 1, None)

        for _, itemset in enumerate(self.listOfItemset):
            itemset = [item for item in itemset if item in headerTable]
            itemset.sort(key=lambda item: (-headerTable[item][0], item))

            currentNode = initialNode
            for item in itemset:
                currentNode = self.updateTree(item, currentNode, headerTable)

        return initialNode, headerTable
    
    
    def findPrefixPath(self, node, prefixPath):
        if node.parent is not None:
            prefixPath.append(node.itemName)
            self.findPrefixPath(node.parent, prefixPath)

    def createConditionalPatternBase(self, item, headerTable):
        nodeOfTree = headerTable[item][1]
        conditionalPaths = []
        frequencyOfEachPath = []

        while nodeOfTree is not None:
            prefixPath = []
            self.findPrefixPath(nodeOfTree, prefixPath)
            prefixPath = prefixPath[::-1]

            if len(prefixPath) > 1:
                conditionalPaths.append(prefixPath[:len(prefixPath) - 1])
                frequencyOfEachPath.append(nodeOfTree.count)

            nodeOfTree = nodeOfTree.next

        return conditionalPaths, frequencyOfEachPath

    def constructConditionalTree(self, conditionalPatternBase, frequency, minimumSupport):
        conditionalHeaderTable = defaultdict(int)

        for i, itemSet in enumerate(conditionalPatternBase):
            for item in itemSet:
                conditionalHeaderTable[item] += frequency[i]

        conditionalHeaderTable = dict((item, supportValue) for item, supportValue in conditionalHeaderTable.items() if supportValue >= minimumSupport)

        if len(conditionalHeaderTable) == 0:
            return None, None

        for item in conditionalHeaderTable:
            conditionalHeaderTable[item] = [conditionalHeaderTable[item], None]

        conditionalInitialNode = FPNode('Null', 1, None)
        conditionalPatternBaseExtracted = []

        for itemset, freq in zip(conditionalPatternBase, frequency):
            conditionalPatternBaseExtracted.extend([itemset.copy() for _ in range(freq)])

        for _, itemset in enumerate(conditionalPatternBaseExtracted):
            itemset = [item for item in itemset if item in conditionalHeaderTable]
            currentNode = conditionalInitialNode

            for item in itemset:
                currentNode = self.updateTree(item, currentNode, conditionalHeaderTable)

        return conditionalInitialNode, conditionalHeaderTable

    def miningTrees(self, headerTable, prefix, freqItemsetList):
        itemlistSorted = [item[0] for item in sorted(headerTable.items(), key=lambda item: (-item[1][0], item[0]))]

        for item in itemlistSorted:
            newFreqItemset = prefix.copy()
            newFreqItemset.add(item)
            freqItemsetList.append(newFreqItemset)
            conditionalPatternBase, frequency = self.createConditionalPatternBase(item, headerTable)
            conditionalTree, newHeaderTable = self.constructConditionalTree(conditionalPatternBase, frequency, self.minimumSupportRatio)

            if newHeaderTable is not None:
                self.miningTrees(newHeaderTable, newFreqItemset, freqItemsetList)
    
    
    def run(self):
        self.read_data()
        
        self.minimumSupport = len(self.listOfItemset) * self.minimumSupportRatio
        fpTree, headerTable = self.constructFPTree()

        if fpTree.children is None:
            print('No frequent item set')
        else:
            freqentItemset = []
            self.miningTrees(headerTable, set(), freqentItemset)
            
            return freqentItemset, self.listOfItemset, self.minimumConfidence