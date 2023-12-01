from itertools import chain, combinations
from collections import defaultdict


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


def getSupport(testSet, itemSetList):
    count = 0
    for itemSet in itemSetList:
        if(set(testSet).issubset(itemSet)):
            count += 1
    return count


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


def associationRuleFpGrowth(freqItemSet, itemSetList, minConf):
    rules = defaultdict(list)

    support_dict = {frozenset(itemSet): getSupport(itemSet, itemSetList) for itemSet in freqItemSet}

    for itemSet in freqItemSet:
        subsets = powerset(itemSet)
        itemSetSup = support_dict[frozenset(itemSet)]
        support = support_dict[frozenset(itemSet)]

        for s in subsets:
            s_set = frozenset(s)
            itemSet_set = set(itemSet)
            s_difference = itemSet_set.difference(s_set)

            confidence = float(itemSetSup / support_dict[s_set])
            if confidence >= minConf:
                support_B = support_dict[frozenset(s_difference)]
                lift_ratio = confidence / (support_B / len(itemSetList))

                rule_key = (s_set, frozenset(s_difference))
                rules[rule_key] = [support, confidence, lift_ratio]

    return dict(rules)

