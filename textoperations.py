from converters import *
from crypto import *
from enum import Enum

def isTextChar(char):
	if (type(char) == str):
		char = ord(char)
	return (65 <= char <= 90) or (97 <= char <= 122)

def findKeysize(data):
	return None

def getWordList():
	with open('files/englishwords.txt', 'r') as f:
		wordList = [word for word in f.read().split('\n')]
	return wordList

def numAsciiChars(string):
	true = 0
	for char in string:
		if isTextChar(char):
			true += 1
	return (true / len(string))


charFrequency = {
	'a': 0.8167, 'b': 0.1492, 'c': 0.2782, 'd': 0.4253, 'e': 0.12702,
	'f': 0.2228, 'g': 0.2015, 'h': 0.6094, 'i': 0.6966, 'j': 0.0153,
	'k': 0.0772, 'l': 0.4025, 'm': 0.2406, 'n': 0.6749, 'o': 0.7507,
	'p': 0.1929, 'q': 0.0095, 'r': 0.5987, 's': 0.6327, 't': 0.9056,
	'u': 0.2758, 'v': 0.0978, 'w': 0.2360, 'x': 0.0150, 'y': 0.1974,
	'z': 0.0074, ' ': 0.128,
}

def numCharFrequency(char):
	try:
		if(ord(char) > 64 and ord(char) < 90):
			return charFrequency[char.lower()]
		return charFrequency[char]
	except KeyError:
		return 0.0

def numFrequencyEstimation(string):
	return sum([numCharFrequency(char) for char in string])

class WordListMode(Enum):
	SMALL = 1
	MEDIUM = 2
	LARGE = 3
	ALL = 4


def numEnglishWords(string, wordListMode=WordListMode.MEDIUM):
	words = [word.lower() for word in string.split(' ')]
	sumChars = sum([len(word) for word in words if len(word) > 1])
	
	if wordListMode == WordListMode.SMALL:
		wordList = englishWordListSmall
	elif wordListMode == WordListMode.MEDIUM:
		wordList = englishWordListMedium
	elif wordListMode == WordListMode.LARGE:
		wordList = englishWordListLarge
	else:
		wordList = englishWordListAll

	matchedChars = 0
	for word in words:
		if word in wordList and len(word) > 1:
			matchedChars += len(word)
	return matchedChars / sumChars


def hammingDist(first, second):

	if type(first) == str or type(second) == str:
		raise Exception('Input is not in Bytes Format!')

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


def decodeURLParams(string):
	return {
		pair.split('=')[0] : pair.split('=')[1]
		for pair in string.split('&')
	}

def parseUserData(userData):
	email = userData['email']
	uid = userData['uid']
	role = userData['role']
	return f'email={email}&uid={uid}&role={role}'

def profileFor(string):
	procString = string.split('&')[0]
	userData = {
		'email' : string,
		'uid' : 10,
		'role' : 'user'
	}
	return parseUserData(userData)

def encryptUserProfile(userData, key):
	cipher = Cipher(key)
	encoded = cipher.encryptECB(userData)
	return encoded

def decryptUserProfile(userData, key):
	cipher = Cipher(key)
	decoded = cipher.encryptECB(userData)
	return decoded



englishWordListAll = getWordList()
englishWordListSmall = englishWordListAll[:100]
englishWordListMedium = englishWordListAll[:500]
englishWordListLarge = englishWordListAll[:1000]
