from optparse import OptionParser
from src.models.product import Product
from src.models.transaction import TransactionProduct, Transaction
import numpy
from csv import reader
from collections import defaultdict, Counter, OrderedDict
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
    def __init__(self, minimumSupportCount, minimumConfidence):
        self.minimumSupportCount = minimumSupportCount
        self.listOfItemset = []
        self.dictOfFilteredItems = {}
        self.frequencyOfTransaction = []
        self.itemFrequencyFiltered = {}


    def read_data(self, transactions):
        dictOfItems = defaultdict(list)

        for item in transactions:
            dictOfItems[item.transaction_id].append(item.itemCode)

        self.listOfItemset = list(dictOfItems.values())
        self.frequencyOfTransaction = [1] * len(self.listOfItemset)
        self.dictOfFilteredItems = dictOfItems
     
     
    def getFrequentOfItems(self):
        itemFrequencyCounter = Counter(item for itemset in self.listOfItemset for item in itemset)

        self.itemFrequencyFiltered = {item: frequency for item, frequency in sorted(itemFrequencyCounter.items(), key=lambda x: x[1], reverse=True) if frequency >= self.minimumSupportCount}

    
    def filteredTransactionItems(self):
        order_keys = set(self.itemFrequencyFiltered.keys())
        sorted_order = [item for item in self.itemFrequencyFiltered]

        keys_to_remove = []
        
        for key, value in self.dictOfFilteredItems.items():
            filtered_list = [elem for elem in value if elem in order_keys]
            if not filtered_list:
                keys_to_remove.append(key)
            else:
                self.dictOfFilteredItems[key] = sorted(filtered_list, key=lambda x: sorted_order.index(x))

        for key_to_remove in keys_to_remove:
            del self.dictOfFilteredItems[key_to_remove]
    
    
    # CREATE THE TREE
    
    
    def updateHeaderTable(self, item, targetNode, headerTable):
        if headerTable[item][1] is None:
            headerTable[item][1] = targetNode
        else:
            currentNode = headerTable[item][1]
            while currentNode.next is not None:
                currentNode = currentNode.next
            currentNode.next = targetNode
    

    def updateTree(self, item, parentNode, headerTable, supportCount):
        if item in parentNode.children:
            parentNode.children[item].increment(supportCount)
        else:
            newItemNode = FPNode(item, supportCount, parentNode)
            parentNode.children[item] = newItemNode
            self.updateHeaderTable(item, newItemNode, headerTable)
        return parentNode.children[item]


    def constructFPTree(self):
        headerTable = self.itemFrequencyFiltered
        
        if len(headerTable) == 0:
            return None, None

        headerTable = {item: [freq, None] for item, freq in headerTable.items()}

        initialNode = FPNode('Null', 1, None)
        
        for _, itemset in self.dictOfFilteredItems.items():
            currentNode = initialNode
            for item in itemset:
                currentNode = self.updateTree(item, currentNode, headerTable, supportCount=1)

        return initialNode, headerTable
    
    
    # MINING THE TREE
    
    
    def findPrefixPath(self, node, prefixPath):
        if node.parent is not None:
            prefixPath.insert(0, node.itemName)
            self.findPrefixPath(node.parent, prefixPath)


    def createConditionalPatternBase(self, item, headerTable):
        node_of_tree = headerTable[item][1]
        dict_of_conditional_pattern_base = {}

        if node_of_tree.parent.itemName != 'Null':
            while node_of_tree is not None:
                prefix_path = []
                
                if node_of_tree.parent.itemName != 'Null':
                    self.findPrefixPath(node_of_tree.parent, prefix_path)

                    prefix_path = tuple(prefix_path)

                    if prefix_path in dict_of_conditional_pattern_base:
                        dict_of_conditional_pattern_base[prefix_path] += node_of_tree.count
                    else:
                        dict_of_conditional_pattern_base[prefix_path] = node_of_tree.count

                node_of_tree = node_of_tree.next

        return dict_of_conditional_pattern_base


    def constructConditionalTree(self, conditionalPatternBase):
        conditionalHeaderTable = defaultdict(int)

        for itemSet, freq in conditionalPatternBase.items():
            for item in itemSet:
                conditionalHeaderTable[item] += freq
        
        conditionalHeaderTable = {item: supportValue for item, supportValue in conditionalHeaderTable.items() if supportValue >= self.minimumSupportCount}
        
        if not conditionalHeaderTable:
            return None, None

        conditionalHeaderTable = {item: [freq, None] for item, freq in conditionalHeaderTable.items()}

        conditionalInitialNode = FPNode('Null', 1, None)
        
        for itemset, support in conditionalPatternBase.items():
            itemset = [item for item in itemset if item in conditionalHeaderTable]
            currentNode = conditionalInitialNode

            for item in itemset:
                currentNode = self.updateTree(item, currentNode, conditionalHeaderTable, supportCount=support)

        # print("conditionalInitialNode", conditionalInitialNode.display())
        return conditionalInitialNode, conditionalHeaderTable


    def miningTrees(self, headerTable, prefix, freqItemsetList):
        itemlistSorted = [item[0] for item in headerTable.items()][::-1]
        
        for item in itemlistSorted:
            newFreqItemset = list(prefix.copy())
            newFreqItemset.insert(0, item)
            freqItemsetList.append(newFreqItemset)
            conditionalPatternBase = self.createConditionalPatternBase(item, headerTable)
            # print("CPB: ", prefix, item, conditionalPatternBase)
            
            conditionalTree, newHeaderTable = self.constructConditionalTree(conditionalPatternBase)

            if newHeaderTable is not None:
                self.miningTrees(newHeaderTable, newFreqItemset, freqItemsetList)
    
    
    # TRIGGER
    
    
    def run(self):
        self.getFrequentOfItems()
        
        self.filteredTransactionItems()
        
        fpTree, headerTable = self.constructFPTree()
        
        if fpTree.children is None:
            print('No frequent item set')
        else:
            freqentItemset = []
            self.miningTrees(headerTable, set(), freqentItemset)
            
            # print(freqentItemset)
            return self.itemFrequencyFiltered, self.dictOfFilteredItems, freqentItemset, self.listOfItemset