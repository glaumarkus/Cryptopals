from itertools import combinations
from textoperations import *


class probabilityTracker:

	def __init__(self):
		self.ratios = {}
		self.ordered = None

class KeysizeGuesser():

	def __init__(self, start=2, end=40, numCompares=4):
		self.record = probabilityTracker()
		self.start = start
		self.end = end + 1
		self.numKeysizes = numCompares

	def guess(self, data):

		for keysize in range(self.start, self.end):
		    
		    blocks = []
		    for i in range(self.numKeysizes):
		        start = i * keysize
		        end = (i * keysize) + keysize
		        blocks.append(data[start : end])
		    
		    pairs = combinations(blocks, 2)
		    distance = 0.0
		    
		    for (first, second) in pairs:
		        dist += hammingDist(first, second)
		    
		    distance /= len(combinations)
		    distance /= keysize
		    
		    self.probabilityTracker.ratios[keysize] = distance
		    distances[dist] = keysize

			self.probabilityTracker.ordered = sortDict(self.probabilityTracker.ratios)

	def getKeysize(self):
		return next(iter(self.tracker.ordered))




