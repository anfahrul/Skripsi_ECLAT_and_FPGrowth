from optparse import OptionParser
from src.models.product import Product
from src.models.transaction import TransactionProduct, Transaction
from memory_profiler import profile


class Itemset:
    def __init__(self, item):
        self.item = item
        self.support = 0
        self.tids = set()
        

class Eclat:
    def __init__(self, minsup):
        self.minsup = minsup
        self.vertical_data = {}

    def read_data(self, transactions):
        self.vertical_data = {}

        items_in_each_transaction = {}

        for item in transactions:
            items_in_each_transaction.setdefault(item.transaction_id, []).append(item.itemCode)

            if item.itemCode not in self.vertical_data:
                self.vertical_data[item.itemCode] = Itemset(item.itemCode)

            itemset = self.vertical_data[item.itemCode]
            itemset.tids.add(item.transaction_id)
            itemset.support += 1

        list_of_items_in_each_transaction = list(items_in_each_transaction.values())
        
        return list_of_items_in_each_transaction

    
    def prune_and_sort_items(self):
        # keys_to_delete = [key for key, itemset in self.vertical_data.items() if itemset.support < self.minsup]

        # for key in keys_to_delete:
        #     del self.vertical_data[key]

        # self.vertical_data = {k: v for k, v in sorted(self.vertical_data.items(), key=lambda item: item[1].support)}
        
        self.vertical_data = {k: v for k, v in self.vertical_data.items() if v.support >= self.minsup}

        sorted_items = sorted(self.vertical_data.items(), key=lambda item: item[1].support)
        self.vertical_data = dict(sorted_items)        
    
    # def calculate_support(self, itemset):
    #     common_tids = set()

    #     if itemset:
    #         common_tids = set(self.vertical_data[itemset[0]].tids)

    #         for item in itemset[1:]:
    #             common_tids.intersection_update(self.vertical_data[item].tids)

    #     return len(common_tids), common_tids



    def calculate_support(self, itemset):
        common_tids = None

        for item in itemset:
            item_data = self.vertical_data[item]
            if common_tids is None:
                common_tids = set(item_data.tids)
            else:
                common_tids = common_tids.intersection(item_data.tids)

        return len(common_tids), common_tids
    
    
    # def eclat_mine(self, prefix, diff_items, minsup, k, frequent_itemsets):
    #     support, common_tids = self.calculate_support(prefix)

    #     if support >= minsup:
    #         frequent_itemsets[k] = frequent_itemsets.get(k, [])
    #         itemset_data = (frozenset(prefix), support, common_tids)
    #         if itemset_data not in frequent_itemsets[k]:
    #             frequent_itemsets[k].append(itemset_data)

    #     if support < minsup or k < 1:
    #         return

    #     for item in diff_items:
    #         new_prefix = prefix | {item}
    #         new_items = diff_items.difference({item})

    #         self.eclat_mine(new_prefix, new_items, minsup, k + 1, frequent_itemsets)
    
    
    # def eclat_mine(self, prefix, diff_items, minsup, k, frequent_itemsets):
    #     support, common_tids = self.calculate_support(prefix)

    #     if support >= minsup:
    #         frequent_itemsets[k] = frequent_itemsets.get(k, [])
    #         itemset_data = (frozenset(prefix), support, common_tids)
    #         if itemset_data not in frequent_itemsets[k]:
    #             frequent_itemsets[k].append(itemset_data)

    #     if support < minsup or k < 1:
    #         return

    #     print("test k:", k, " prefix:", prefix, " diff:", diff_items)
    #     for i in range(len(diff_items)):
    #         # Lakukan deep-first search untuk setiap item di diff_items
    #         item = diff_items[i]
    #         new_prefix = prefix | {item}
    #         new_items = diff_items[i+1:]

    #         self.eclat_mine(new_prefix, new_items, minsup, k + 1, frequent_itemsets)

    
    # def eclat_mine(self, prefix, diff_items, minsup, k, frequent_itemsets):
    #     support, common_tids = self.calculate_support(prefix)

    #     if support >= minsup:
    #         frequent_itemsets[k] = frequent_itemsets.get(k, [])
    #         itemset_data = (frozenset(prefix), support, common_tids)
    #         if itemset_data not in frequent_itemsets[k]:
    #             frequent_itemsets[k].append(itemset_data)

    #     if support < minsup or k < 1:
    #         return

    #     print("test k:", k, " prefix:", prefix, " diff:", diff_items)
    #     # Urutkan diff_items berdasarkan support
    #     diff_items = sorted(diff_items, key=lambda item: self.vertical_data[item].support, reverse=True)

    #     for i in range(len(diff_items)):
    #         # Lakukan deep-first search untuk setiap item di diff_items
    #         item = diff_items[i]
    #         new_prefix = prefix | {item}
    #         new_items = diff_items[:i] + diff_items[i+1:]

    #         self.eclat_mine(new_prefix, new_items, minsup, k + 1, frequent_itemsets)


    # def eclat_mine(self, prefix, diff_items, minsup, k, frequent_itemsets):
    #     support, common_tids = self.calculate_support(prefix)

    #     if support >= minsup:
    #         frequent_itemsets[k] = frequent_itemsets.get(k, [])
    #         itemset_data = (frozenset(prefix), support, common_tids)
    #         if itemset_data not in frequent_itemsets[k]:
    #             frequent_itemsets[k].append(itemset_data)

    #     if support < minsup or k < 1:
    #         return

    #     print("test k:", k, " prefix:", prefix, " diff:", diff_items)
    #     # Urutkan diff_items berdasarkan support secara ascending
    #     diff_items = sorted(diff_items, key=lambda item: self.vertical_data[item].support)

    #     for i in range(len(diff_items)):
    #         # Lakukan deep-first search untuk setiap item di diff_items
    #         item = diff_items[i]
    #         new_prefix = prefix | {item}
    #         new_items = sorted(diff_items[i+1:], key=lambda x: self.vertical_data[x].support)

    #         self.eclat_mine(new_prefix, new_items, minsup, k + 1, frequent_itemsets)


    # Hampir benar
    # def eclat_mine(self, prefix, diff_items, minsup, k, frequent_itemsets):
    #     support, common_tids = self.calculate_support(prefix)

    #     if support >= minsup:
    #         frequent_itemsets[k] = frequent_itemsets.get(k, [])
    #         itemset_data = (frozenset(prefix), support, common_tids)
    #         if itemset_data not in frequent_itemsets[k]:
    #             frequent_itemsets[k].append(itemset_data)

    #     if support < minsup or k < 1:
    #         return


    #     sorted_diff_items = sorted(diff_items, key=lambda item: self.vertical_data[item].support)
    #     print("test k:", k, " prefix:", prefix, " diff:", sorted_diff_items)
        
    #     for i, prefix_item in enumerate(sorted_diff_items):
    #         # Lakukan deep-first search untuk setiap item di diff_items
    #         new_prefix = list(prefix)  # Konversi tuple ke list untuk mempertahankan urutan
    #         new_prefix.append(prefix_item)
    #         # print("new prefix", new_prefix)
            
    #         new_diff_items = sorted(set(sorted_diff_items[i+1:]), key=lambda item: sorted_diff_items.index(item))

    #         self.eclat_mine(tuple(new_prefix), new_diff_items, minsup, k + 1, frequent_itemsets)
    
    
    def eclat_mine(self, prefix, diff_items, minsup, k, frequent_itemsets):
        support, common_tids = self.calculate_support(prefix)

        if support >= minsup:
            frequent_itemsets[k] = frequent_itemsets.get(k, [])
            itemset_data = (tuple(prefix), support, common_tids)
            if itemset_data not in frequent_itemsets[k]:
                frequent_itemsets[k].append(itemset_data)
        
        
        if support < minsup or k < 1:
            return


        sorted_diff_items = sorted(diff_items, key=lambda item: self.vertical_data[item].support)
        # print("test k:", k, " prefix:", prefix, " diff:", sorted_diff_items)
        
        for i, prefix_item in enumerate(sorted_diff_items):
            # Lakukan deep-first search untuk setiap item di diff_items
            new_prefix = list(prefix)  # Konversi tuple ke list untuk mempertahankan urutan
            new_prefix.append(prefix_item)
            # print("new prefix", new_prefix)
            
            new_diff_items = sorted(set(sorted_diff_items[i+1:]), key=lambda item: sorted_diff_items.index(item))

            self.eclat_mine(tuple(new_prefix), new_diff_items, minsup, k + 1, frequent_itemsets)
 
    
    def run(self):
        self.prune_and_sort_items()
        frequent_itemsets = {} 
        
        sorted_items = sorted(self.vertical_data, key=lambda item: self.vertical_data[item].support)
        for i, prefix_item in enumerate(sorted_items):
            diff_items = sorted(set(sorted_items[i+1:]), key=lambda item: sorted_items.index(item))
            self.eclat_mine({prefix_item}, diff_items, self.minsup, 1, frequent_itemsets)
            # print({prefix_item}, diff_items)
        
        # print("frequent_itemsets", frequent_itemsets)
        
        # for k, v in self.vertical_data.items():
        #     self.eclat_mine({k}, items.difference({k}), self.minsup, 1, frequent_itemsets)
        
        # items = set(self.vertical_data.keys())

        # for item in items:
        #     self.eclat_mine({item}, items.difference({item}), self.minsup, 1, frequent_itemsets)

        return self.vertical_data, frequent_itemsets