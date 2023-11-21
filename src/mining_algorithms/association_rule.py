from itertools import chain, combinations


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


def getSupport(testSet, itemSetList):
    count = 0
    for itemSet in itemSetList:
        if(set(testSet).issubset(itemSet)):
            count += 1
    return count


# def associationRule(freqItemSets, itemSetList, minConf):
#     rules = []

#     for k, itemSets in freqItemSets.items():
#         if k > 1:  # Hanya proses frequent itemsets dengan k > 1
#             for itemSet, support, tids in itemSets:
#                 subsets = powerset(itemSet)

#                 for s in subsets:
#                     if len(s) > 0:
#                         sSupport = getSupport(s, itemSetList)
#                         confidence = float(support) / sSupport

#                         if confidence > minConf:
#                             rules.append((s, itemSet.difference(s), confidence))

#     return rules


# def associationRule(freqItemSetDict, itemSetList, minConf):
#     rules = []

#     # Menghitung dukungan setiap itemset dalam freqItemSet
#     itemSetSupport = {}
#     for k, itemSetList in freqItemSetDict.items():
#         for itemSet, support, tids in itemSetList:
#             itemSetTuple = tuple(itemSet)  # Konversi set menjadi tuple
#             itemSetSupport[itemSetTuple] = support

#     for k, itemSetList in freqItemSetDict.items():
#         for itemSet, support, tids in itemSetList:
#             subsets = powerset(itemSet)
#             itemSetSup = itemSetSupport[tuple(itemSet)]  # Mengambil dukungan itemSet

#             for s in subsets:
#                 s_tuple = tuple(s)
#                 if s_tuple in itemSetSupport and itemSetSupport[s_tuple] > 0:
#                     confidence = float(itemSetSup / itemSetSupport[s_tuple])
#                     if confidence > minConf:
#                         rules.append([set(s), set(itemSet.difference(s)), support, confidence])

#     return rules


# def associationRule(freqItemSetDict, itemSetList, minConf):
#     rules = []
    
    
#     # Menghitung dukungan setiap itemset dalam freqItemSet
#     itemSetSupport = {}
#     for k, itemSets in freqItemSetDict.items():
#         for itemSet, support, tids in itemSets:
#             itemSetTuple = tuple(itemSet)  # Konversi set menjadi tuple
#             itemSetSupport[itemSetTuple] = support
            
    
#     for k, itemSets in freqItemSetDict.items():
#         for itemSet, support, tids in itemSets:
#             subsets = powerset(itemSet)
#             itemSetSup = itemSetSupport[tuple(itemSet)]  # Mengambil dukungan itemSet

#             for s in subsets:
#                 s_tuple = tuple(s)
#                 if s_tuple in itemSetSupport and itemSetSupport[s_tuple] > 0:
#                     confidence = float(itemSetSup / itemSetSupport[s_tuple])
#                     if confidence > minConf:

#                         # Hitung Lift Ratio
#                         lift_ratio = confidence / (itemSetSupport[tuple(itemSet.difference(s))] / len(itemSetList))

#                         rules.append([set(s), set(itemSet.difference(s)), support, confidence, lift_ratio])

#     return rules

# Code Sebelumnya 
# def associationRule(freqItemSetDict, itemSetList, minConf):
#     rules = {}
    
#     # Menghitung dukungan setiap itemset dalam freqItemSet
#     itemSetSupport = {}
#     for k, itemSets in freqItemSetDict.items():
#         for itemSet, support, tids in itemSets:
#             itemSetTuple = frozenset(itemSet)  # Konversi set menjadi frozenset
#             itemSetSupport[itemSetTuple] = support
            
#     for k, itemSets in freqItemSetDict.items():
#         for itemSet, support, tids in itemSets:
#             subsets = powerset(itemSet)
#             itemSetSup = itemSetSupport[frozenset(itemSet)]  # Mengambil dukungan itemSet

#             for s in subsets:
#                 s_tuple = frozenset(s)
#                 if s_tuple in itemSetSupport and itemSetSupport[s_tuple] > 0:
#                     confidence = float(itemSetSup / itemSetSupport[s_tuple])
#                     if confidence >= minConf:
#                         # Hitung Lift Ratio
#                         lift_ratio = confidence / (itemSetSupport[frozenset(itemSet.difference(s))] / len(itemSetList))
                        
#                         # Buat key untuk aturan asosiasi
#                         rule_key = (frozenset(s), frozenset(itemSet.difference(s)))
                        
#                         rules[rule_key] = [support, confidence, lift_ratio]

#     return rules


# def associationRule(freqItemSetDict, itemSetList, minConf):
#     rules = {}

#     # Menghitung dukungan setiap itemset dalam freqItemSet
#     itemSetSupport = {}
#     for k, itemSets in freqItemSetDict.items():
#         for itemSet, support, tids in itemSets:
#             itemSetTuple = tuple(itemSet)
#             itemSetSupport[itemSetTuple] = support

#     for itemSetTuple in itemSetSupport.keys():
#         print("itemSetTuple", itemSetTuple)
#         itemSet = set(itemSetTuple)
#         itemSetSup = itemSetSupport[itemSetTuple]
        
#         # print("itemset", itemSet)

#         subsets = powerset(itemSetTuple)
        

#         for s in subsets:
#             s_set = set(s)
#             s_set_tuple = tuple(s_set)
            
#             print("s:", s_set, "diff s:", itemSet.difference(s_set))
#             if s_set_tuple in itemSetSupport and itemSetSupport[s_set_tuple] > 0:
#                 confidence = float(itemSetSup / itemSetSupport[s_set_tuple])

#                 if confidence >= minConf:
#                     # Hitung Lift Ratio
#                     s_difference = itemSet.difference(s_set)
#                     s_difference_tuple = tuple(sorted(s_difference))
#                     lift_ratio = confidence / (itemSetSupport[s_difference_tuple] / len(itemSetList))

#                     # Buat key untuk aturan asosiasi
#                     rule_key = (tuple(s_set), s_difference_tuple)

#                     rules[rule_key] = [itemSetSupport[itemSetTuple], confidence, lift_ratio]

#     return rules


def associationRule(freqItemSetDict, itemSetList, minConf):
    rules = {}

    # Menghitung dukungan setiap itemset dalam freqItemSet
    itemSetSupport = {}
    for k, itemSets in freqItemSetDict.items():
        for itemSet, support, tids in itemSets:
            itemSetTuple = frozenset(itemSet)
            itemSetSupport[itemSetTuple] = support

    for itemSet in itemSetSupport.keys():
        subsets = powerset(itemSet)
        itemSetSup = itemSetSupport[frozenset(itemSet)]
        

        for s in subsets:
            s_tuple = frozenset(s)
            
            if s_tuple in itemSetSupport and itemSetSupport[s_tuple] > 0:
                confidence = float(itemSetSup / itemSetSupport[s_tuple])

                if confidence >= minConf:
                    support_B = (itemSetSupport[frozenset(itemSet.difference(s))] / len(itemSetList))
                    
                    lift_ratio = confidence / support_B
                    
                    s_difference = frozenset(itemSet.difference(s))

                    rule_key = (s_tuple, s_difference)
                    
                    support = itemSetSup
                    
                    rules[rule_key] = [
                        support, 
                        confidence, 
                        lift_ratio
                        ]

    return rules


def associationRuleEclatWithoutVerbose(freqItemSetList, itemSetList, minConf):
    rules = {}

    # Menghitung dukungan setiap itemset dalam freqItemSet
    itemSetSupport = {}
    for itemSet, support, tids in freqItemSetList:
        itemSetTuple = frozenset(itemSet)
        itemSetSupport[itemSetTuple] = support

    for itemSet, support, tids in freqItemSetList:
        subsets = powerset(itemSet)
        itemSetSup = itemSetSupport[frozenset(itemSet)]
        
        
        for s in subsets:
            s_tuple = frozenset(s)
            
            
            if s_tuple in itemSetSupport and itemSetSupport[s_tuple] > 0:
                # Menghitung dukungan itemset B
                itemSet_B = tuple(item for item in itemSet if item not in s)
                itemSet_B_support = itemSetSupport[frozenset(itemSet_B)]
                
                # print( "itemSetSup:", itemSetSup, "itemset A:", s_tuple, " supp A:", itemSetSupport[s_tuple])                
                confidence = float(itemSetSup / itemSetSupport[s_tuple])

                if confidence >= minConf:
                    support_B = itemSet_B_support  # Tidak perlu dibagi len(itemSetList)
                    # print("confidence", confidence, "B:", itemSet_B, "supp:", support_B)
                    
                    lift_ratio = confidence / (support_B / len(itemSetList))
                    
                    s_difference = frozenset(itemSet_B)

                    rule_key = (s_tuple, s_difference)
                    
                    support = itemSetSup
                    
                    rules[rule_key] = [
                        support, 
                        confidence, 
                        lift_ratio
                    ]

    return rules



def associationRuleFpGrowth(freqentItemset, listOfItemset, minConf):
    rules = {}

    for itemSet in freqentItemset:
        subsets = powerset(itemSet)
        itemSetSup = getSupport(itemSet, listOfItemset)
        
        for s in subsets:
            support = getSupport(s, listOfItemset)
            confidence = float(itemSetSup / support)
            if confidence >= minConf:
                lift_ratio = confidence / (getSupport(itemSet.difference(s), listOfItemset) / len(listOfItemset))
                
                rule_key = (frozenset(s), frozenset(itemSet.difference(s)))
                
                rules[rule_key] = [support, confidence, lift_ratio]
                
    return rules