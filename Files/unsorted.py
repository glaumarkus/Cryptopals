


def isTextChar(char):
	if (type(char) == str):
		char = ord(char)
	return (65 <= char <= 90) or (97 <= char <= 122)

def findKeysize(data):
	return None

def getWordList():
	with open('englishwords.txt', 'r') as f:
		wordList = {
			word:idx 
			for idx, word in enumerate(f.read().split('\n')) 
		}
	return wordList

def numAsciiChars(string):
	true = 0
	for char in string:
		if isTextChar(char):
			true += 1
	return (true / len(string))

def numEnglishWords(string):
	words = [word for word in string.split(' ')]
	sumChars = sum([len(word) for word in words if len(word) > 2])
	wordList = getWordList()
	matchedChars = 0
	for word in words:
		if word in wordList.keys() and len(word) > 2:
			matchedChars += len(word)
	return matchedChars / sumChars


import collections

def sortDict(unorderedDict, filterValue=None):
	if filterValue:
		return collections.OrderedDict(
			sorted(
				{ key:unorderedDict[key] for key in unorderedDict.keys() if unorderedDict[key] > filterValue}.items(),
				reverse=True
				)
			)
	return collections.OrderedDict(sorted(unorderedDict.items(), reverse=True))

import converters

class probabilityRatios:
	def __init__(self):
		self.charRatio = 0.0
		self.wordRatio = 0.0


def SingleByteCracker(bytestring):

	probabilities = {}
	for char in range(256):
		tmpString = bytes2str(
			bytearray(
				[byte ^ char for byte in bytestring]
				)
			)
		ratios = probabilityRatios()
		ratios.charRatio = numAsciiChars(tmpString)
		if ratios.charRatio >= 0.7:
			ratios.wordRatio = numEnglishWords(tmpString)

		probabilities[char] = ratios





