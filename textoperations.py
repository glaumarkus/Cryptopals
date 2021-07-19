from converters import *

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

def hammingDist(first, second):
	if type(first) == str:
		first = str2bytes(first)
	if type(second) == str:
		second = str2bytes(second)

    distance = 0
    for i in range(len(first)):
        x = first[i] ^ second[i]
        bits = 0
        while (x > 0):
            bits += x & 1
            x >>= 1
        distance += bits
    return distance


def makeBlocks(data, keysize):
	keysizeBlocks = {i:[] for i in range(keysize)}
	for idx, byte in enumerate(data):
	    keysizeBlocks[idx % keysize].append(byte)
	return keysizeBlocks