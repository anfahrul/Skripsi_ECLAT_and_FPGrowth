from itertools import chain, combinations


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


def getSupport(testSet, itemSetList):
    count = 0
    for itemSet in itemSetList:
        if(set(testSet).issubset(itemSet)):
            count += 1
    return count


def associationRule(freqItemSet, itemSetList, minConf):
    rules = []

    # Menghitung dukungan setiap itemset dalam freqItemSet
    itemSetSupport = {}
    for itemSet in freqItemSet:
        itemSetTuple = tuple(itemSet)  # Konversi set menjadi tuple
        itemSetSupport[itemSetTuple] = getSupport(itemSet, itemSetList)

    for itemSet in freqItemSet:
        subsets = powerset(itemSet)
        itemSetSup = itemSetSupport[tuple(itemSet)]  # Mengambil dukungan itemSet
        
        for s in subsets:
            s_tuple = tuple(s)
            if s_tuple in itemSetSupport and itemSetSupport[s_tuple] > 0:   
                confidence = float(itemSetSup / itemSetSupport[s_tuple])
                if confidence > minConf:
                    rules.append([set(s), set(itemSet.difference(s)), itemSetSupport[tuple(itemSet)], confidence])
    
    return rules