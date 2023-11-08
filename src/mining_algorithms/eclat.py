from optparse import OptionParser
from src.models.product import Product
from src.models.transaction import TransactionProduct, Transaction


class Itemset:
    def __init__(self, item):
        self.item = item
        self.support = 0
        self.tids = set()
        

class Eclat:
    def __init__(self, minsup):
        self.minsup = minsup
        self.item_count = 0
        self.trans_count = 0
        self.data = None


    def read_data(self):
        transactionsProducts = TransactionProduct.query.all()
        
        self.item_count = 0
        self.data = {}
        itemsInEachTransactionDict = {}
        listOfItemInEachTransaction = []
        
        for item in transactionsProducts:
            if item.transaction_id not in itemsInEachTransactionDict:
                itemsInEachTransactionDict[item.transaction_id] = []
                
            itemsInEachTransactionDict[item.transaction_id].append(item.itemCode)
            
            if item.itemCode not in self.data:
                self.data[item.itemCode] = Itemset(item.itemCode)
                self.item_count += 1
            
            self.data[item.itemCode].tids.add(item.transaction_id)
        
        
        for _, value in self.data.items():
                value.support = len(value.tids)
            
        listOfItemInEachTransaction = [values for values in itemsInEachTransactionDict.values()]
        
        return listOfItemInEachTransaction

    
    def prune_and_sort_items(self):
        keys_to_delete = [key for key, itemset in self.data.items() if itemset.support < self.minsup]

        for key in keys_to_delete:
            del self.data[key]

        self.data = {k: v for k, v in sorted(self.data.items(), key=lambda item: item[1].support)}
        
        
    def calculate_support(self, itemset):
        common_tids = None

        for item in itemset:
            item_data = self.data[item]
            if common_tids is None:
                common_tids = set(item_data.tids)
            else:
                common_tids = common_tids.intersection(item_data.tids)

        return len(common_tids), common_tids
    
    
    def eclat_mine(self, prefix, items, minsup, k, frequent_itemsets):
        support, common_tids = self.calculate_support(prefix)

        if support >= minsup:
            frequent_itemsets[k] = frequent_itemsets.get(k, [])
            itemset_data = (frozenset(prefix), support, common_tids)
            if itemset_data not in frequent_itemsets[k]:
                frequent_itemsets[k].append(itemset_data)

        if support < minsup or k < 1:
            return

        for item in items:
            new_prefix = prefix | {item}
            new_items = items.difference({item})

            self.eclat_mine(new_prefix, new_items, minsup, k + 1, frequent_itemsets)
    
    
    def run(self):
        listOfItemInEachTransaction = self.read_data()
        self.prune_and_sort_items()
        minsup = self.minsup
        frequent_itemsets = {} 
        verticalData = self.data

        items = set(self.data.keys())

        for item in items:
            self.eclat_mine({item}, items.difference({item}), minsup, 1, frequent_itemsets)

        return listOfItemInEachTransaction, verticalData, frequent_itemsets