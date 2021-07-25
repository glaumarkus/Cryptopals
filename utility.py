import collections
import os

def sortDict(unorderedDict, filterValue=None, reverse=True):
	if filterValue:
		return collections.OrderedDict(
			sorted(
				{ key:unorderedDict[key] for key in unorderedDict.keys() if unorderedDict[key] > filterValue}.items(),
				key=lambda x: float(x[1]),
				reverse=reverse
				)
			)
	return collections.OrderedDict(
		sorted(
			unorderedDict.items(),
			key=lambda x: float(x[1]),
			reverse=reverse
			)
		)

def RNGint(start=0, end=254):
	i = int.from_bytes(os.urandom(1), byteorder='little') / 255
	r = end - start
	i *= r
	i += start
	return int(i)