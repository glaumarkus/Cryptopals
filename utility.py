import collections

def sortDict(unorderedDict, filterValue=None, reverse=True):
    if filterValue:
        return collections.OrderedDict(
            sorted(
                { key:unorderedDict[key] for key in unorderedDict.keys() if unorderedDict[key] > filterValue}.items(),
                reverse=reverse
                )
            )
    return collections.OrderedDict(sorted(unorderedDict.items(), reverse=reverse))
