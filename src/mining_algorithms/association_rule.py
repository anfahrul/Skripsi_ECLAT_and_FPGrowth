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


def associationRule(dictOfFrequentItemset, listOfItemset, minimumConfidence):
    rules = {}

    dictOfItemsetsSupport = {}
    
    for k, itemsets in dictOfFrequentItemset.items():
        for itemset, support, tids in itemsets:
            itemset = frozenset(itemset)
            dictOfItemsetsSupport[itemset] = support

    for itemset in dictOfItemsetsSupport.keys():
        subsets = powerset(itemset)
        itemsetsSupport = dictOfItemsetsSupport[frozenset(itemset)]
        
        for antecedent in subsets:
            itemset = set(itemset)
            
            antecedent = frozenset(antecedent)
            antecedentSupport = dictOfItemsetsSupport[antecedent]
            
            consequent = itemset.difference(antecedent)
            consequentSupport = dictOfItemsetsSupport[frozenset(consequent)]

            confidence = float(itemsetsSupport / antecedentSupport)
            if confidence >= minimumConfidence:
                liftRatio = confidence / (consequentSupport / len(listOfItemset))

                ruleKey = (antecedent, frozenset(consequent))
                rules[ruleKey] = [itemsetsSupport, confidence, liftRatio]  

    return rules


def associationRuleEclatWithoutVerbose(frequentItemset, listOfItemset, minimumConfidence):
    rules = {}

    dictOfItemsetsSupport = {frozenset(itemset): support for itemset, support, tids in frequentItemset}

    for itemset, _, _ in frequentItemset:
        subsets = powerset(itemset)
        itemsetsSupport = dictOfItemsetsSupport[frozenset(itemset)]
        
        
        for antecedent in subsets:
            itemset = set(itemset)
            
            antecedent = frozenset(antecedent)
            antecedentSupport = dictOfItemsetsSupport[antecedent]
            
            consequent = itemset.difference(antecedent)
            consequentSupport = dictOfItemsetsSupport[frozenset(consequent)]

            confidence = float(itemsetsSupport / antecedentSupport)
            if confidence >= minimumConfidence:
                liftRatio = confidence / (consequentSupport / len(listOfItemset))

                ruleKey = (antecedent, frozenset(consequent))
                rules[ruleKey] = [itemsetsSupport, confidence, liftRatio]            

    return rules


def associationRuleFpGrowth(frequentItemset, listOfItemset, minimumConfidence):
    rules = defaultdict(list)

    for itemset in frequentItemset:
        subsets = powerset(itemset)
        itemsetsSupport = frequentItemset[frozenset(itemset)]

        for antecedent in subsets:
            itemset = set(itemset)
            
            antecedent = frozenset(antecedent)
            antecedentSupport = frequentItemset[antecedent]
            
            consequent = itemset.difference(antecedent)
            consequentSupport = frequentItemset[frozenset(consequent)]

            confidence = float(itemsetsSupport / antecedentSupport)
            if confidence >= minimumConfidence:
                liftRatio = confidence / (consequentSupport / len(listOfItemset))

                ruleKey = (antecedent, frozenset(consequent))
                rules[ruleKey] = [itemsetsSupport, confidence, liftRatio]

    return dict(rules)

