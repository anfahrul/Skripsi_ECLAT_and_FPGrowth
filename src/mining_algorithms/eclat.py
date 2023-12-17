from memory_profiler import profile

class Itemset:
    def __init__(self, item):
        self.item = item
        self.support = 0
        self.tids = set()    

class Eclat:
    def __init__(self, minsup, verbose):
        self.minsup = minsup
        self.vertical_data = {}
        self.vertical_data_pruned = {}
        self.verbose = verbose


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
        
        print("Finish reading the data")
        return list_of_items_in_each_transaction

    
    def prune_items(self):
        self.vertical_data_pruned = {k: v for k, v in self.vertical_data.items() if v.support >= self.minsup}

        # sorted_items = sorted(self.vertical_data.items(), key=lambda item: item[1].support)
        # self.vertical_data = dict(sorted_items)
        print("Finish pruning the data")  
    
    
    def sorting_item_freq(self):
        return sorted(self.vertical_data_pruned, key=lambda item: self.vertical_data_pruned[item].support)
    

    def calculate_support(self, itemset):
        common_tids = None

        for item in itemset:
            item_data = self.vertical_data_pruned[item]
            if common_tids is None:
                common_tids = set(item_data.tids)
            else:
                common_tids = common_tids.intersection(item_data.tids)

        return len(common_tids), common_tids
    
    
    def eclat_mine(self, prefix, diff_items, minsup, k, frequent_itemsets):
        support, common_tids = self.calculate_support(prefix)

        if support >= minsup:
            frequent_itemsets[k] = frequent_itemsets.get(k, [])
            itemset_data = (tuple(prefix), support, common_tids)
            if itemset_data not in frequent_itemsets[k]:
                frequent_itemsets[k].append(itemset_data)

        if support < minsup or k < 1:
            return

        for i, prefix_item in enumerate(diff_items):
            new_prefix = list(prefix)
            new_prefix.append(prefix_item)

            new_diff_items = diff_items[i+1:]
            self.eclat_mine(tuple(new_prefix), new_diff_items, minsup, k + 1, frequent_itemsets)

            
    def eclat_mine_without_verbose(self, prefix, diff_items, minsup, frequent_itemsets):
        support, common_tids = self.calculate_support(prefix)

        if support >= minsup:
            itemset_data = (tuple(prefix), support, common_tids)
            frequent_itemsets.append(itemset_data)

        if support < minsup or not diff_items:
            return

        for i, prefix_item in enumerate(diff_items):
            new_prefix = list(prefix)
            new_prefix.append(prefix_item)

            new_diff_items = diff_items[i+1:]
            self.eclat_mine_without_verbose(tuple(new_prefix), new_diff_items, minsup, frequent_itemsets)

    
    @profile
    def run(self):
        print("Running ECLAT Algorithm")
        self.prune_items()
        
        sorted_items = self.sorting_item_freq()
        
        if self.verbose == True:
            frequent_itemsets = {}
            for i, prefix_item in enumerate(sorted_items):
                diff_items = sorted_items[i+1:]
                self.eclat_mine({prefix_item}, diff_items, self.minsup, 1, frequent_itemsets)
            
            print("ECLAT Algorithm mining successfully")
            return self.vertical_data, frequent_itemsets
        else:
            frequent_itemsets = []
            for i, prefix_item in enumerate(sorted_items):
                diff_items = sorted_items[i+1:]
                self.eclat_mine_without_verbose({prefix_item}, diff_items, self.minsup, frequent_itemsets)
                
            print("ECLAT Algorithm mining successfully")
            return frequent_itemsets
        