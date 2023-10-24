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


def associationRule(freqItemSetDict, itemSetList, minConf):
    rules = []

    # Menghitung dukungan setiap itemset dalam freqItemSet
    itemSetSupport = {}
    for k, itemSetList in freqItemSetDict.items():
        for itemSet, support, tids in itemSetList:
            itemSetTuple = tuple(itemSet)  # Konversi set menjadi tuple
            itemSetSupport[itemSetTuple] = support

    for k, itemSetList in freqItemSetDict.items():
        for itemSet, support, tids in itemSetList:
            subsets = powerset(itemSet)
            itemSetSup = itemSetSupport[tuple(itemSet)]  # Mengambil dukungan itemSet

            for s in subsets:
                s_tuple = tuple(s)
                if s_tuple in itemSetSupport and itemSetSupport[s_tuple] > 0:
                    confidence = float(itemSetSup / itemSetSupport[s_tuple])
                    if confidence > minConf:
                        rules.append([set(s), set(itemSet.difference(s)), support, confidence])

    return rules