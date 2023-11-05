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
            
    def getDatasetFromFile(self, filename):
        with open(filename, 'r') as file:
            csv_reader = reader(file)
            for line in csv_reader:
                line = list(filter(None, line))
                self.listOfItemset.append(line)
                self.frequencyOfTransaction.append(1)