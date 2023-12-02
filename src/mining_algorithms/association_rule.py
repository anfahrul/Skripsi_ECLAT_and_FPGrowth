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


def associationRuleEclatWithoutVerbose(frequentItemset, listOfItemset, minimumConfidence):
    rules = {}

    dictOfItemsetsSupport = {frozenset(itemset): support for itemset, support, tids in frequentItemset}
    dictOfantecedentsSupport = {}

    for itemset, _, _ in frequentItemset:
        subsets = powerset(itemset)
        itemsetsSupport = dictOfItemsetsSupport[frozenset(itemset)]
        
        
        for antecedent in subsets:
            itemset = set(itemset)
            
            antecedent = frozenset(antecedent)
            
            antecedent = frozenset(antecedent)
            if antecedent not in dictOfantecedentsSupport:
                dictOfantecedentsSupport[antecedent] = getSupport(antecedent, listOfItemset)
            antecedentSupport = dictOfantecedentsSupport[antecedent]
            
            consequent = itemset.difference(antecedent)
            if frozenset(consequent) not in dictOfItemsetsSupport:
                dictOfItemsetsSupport[frozenset(consequent)] = getSupport(consequent, listOfItemset)
            consequentSupport = dictOfItemsetsSupport[frozenset(consequent)]

            confidence = float(itemsetsSupport / antecedentSupport)
            if confidence >= minimumConfidence:
                liftRatio = confidence / (consequentSupport / len(listOfItemset))

                ruleKey = (antecedent, frozenset(consequent))
                rules[ruleKey] = [itemsetsSupport, confidence, liftRatio]            

    return rules


def associationRuleFpGrowth(frequentItemset, listOfItemset, minimumConfidence):
    rules = defaultdict(list)

    dictOfItemsetsSupport = {frozenset(itemset): getSupport(itemset, listOfItemset) for itemset in frequentItemset}
    dictOfantecedentsSupport = {}
    
    for itemset in frequentItemset:
        subsets = powerset(itemset)
        itemsetsSupport = dictOfItemsetsSupport[frozenset(itemset)]

        for antecedent in subsets:
            itemset = set(itemset)
            
            antecedent = frozenset(antecedent)
            if antecedent not in dictOfantecedentsSupport:
                dictOfantecedentsSupport[antecedent] = getSupport(antecedent, listOfItemset)
            antecedentSupport = dictOfantecedentsSupport[antecedent]
            
            consequent = itemset.difference(antecedent)
            if frozenset(consequent) not in dictOfItemsetsSupport:
                dictOfItemsetsSupport[frozenset(consequent)] = getSupport(consequent, listOfItemset)
            consequentSupport = dictOfItemsetsSupport[frozenset(consequent)]

            confidence = float(itemsetsSupport / antecedentSupport)
            if confidence >= minimumConfidence:
                liftRatio = confidence / (consequentSupport / len(listOfItemset))

                ruleKey = (antecedent, frozenset(consequent))
                rules[ruleKey] = [itemsetsSupport, confidence, liftRatio]

    return dict(rules)

