from enum import Enum
from textoperations import *
import converters
from utility import *


class CrackerMode(Enum):
	CHARONLY = 1
	WORDONLY = 2
	BOTH = 3


class probabilityRatio:

	def __init__(self, mode=2):
		self.mode = mode
		self.charRatio = 0.0
		self.wordRatio = 0.0

	def __float__(self):
		if self.mode==CrackerMode.CHARONLY:
			return self.charRatio
		elif self.mode==CrackerMode.WORDONLY:
			return self.wordRatio
		return ( self.wordRatio + self.charRatio )

	def __str__(self):
		return str(self.__float__())

	def __gt__(self, other):
		if self.mode==CrackerMode.CHARONLY:
			return self.charRatio > other
		elif self.mode==CrackerMode.WORDONLY:
			return self.wordRatio > other
		return ( self.wordRatio + self.charRatio ) > other


class probabilityTracker:

	def __init__(self):
		self.ratios = {}
		self.ordered = None

class crackResult():

	def __init__(self):
		self.msgEncrypted = None
		self.msgDecrypted = None
		self.probability = None
		self.char = None
		self.charStr = None


class SingleCharXORCracker:

	def __init__(self, mode=2, thresholdChars=0.7, thresholdWords=0.6):
		self.mode = mode
		self.tracker = probabilityTracker()
		self.thresholdChars = thresholdChars
		self.thresholdWords = thresholdWords
		self.result = crackResult()
		self.success = False

	def crack(self, bytestring):

		if type(bytestring) != bytearray:
			raise Exception('Input is not in Bytes Format!')

		# iterate through charset and evaluate based on mode
		for char in range(256):
			tmpString = bytes2str(
			bytearray(
				[byte ^ char for byte in bytestring]
				)
			)
			ratio = probabilityRatio(self.mode)
			ratio.charRatio = numAsciiChars(tmpString)

			if (self.mode == 1):
				self.tracker.ratios[char] = ratio
				continue
			
			ratio.wordRatio = numEnglishWords(tmpString)
			self.tracker.ratios[char] = ratio

		# evaluate best matches
		filterValue = 0.0
		if (self.mode == 1):
			filterValue = self.thresholdChars
		elif (self.mode == 2):
			filterValue = self.thresholdWords
		elif self.mode == 3:
			filterValue = self.thresholdChars + self.thresholdWords
		
		self.tracker.ordered = sortDict(self.tracker.ratios, filterValue=filterValue)

		# if not found
		if len(self.tracker.ordered) == 0:
			return

		# fill record
		self.success = True
		self.result.char = next(iter(self.tracker.ordered))
		self.result.charStr = chr(self.result.char)
		self.result.probability = float(self.tracker.ordered[self.result.char])
		self.result.msgEncrypted = bytestring
		self.result.msgDecrypted = bytes2str(
			bytearray(
				[byte ^ self.result.char for byte in bytestring]
				)
			)[:-1]

	def successful(self):
		return self.success

	def getDecryptionChar(self):
		return self.result.char

	def getDecryptedMsg(self):
		return self.result.msgDecrypted

	def printResult(self):
		print('###########################')
		print('SingleCharXORCracker Result')
		print(f'Char: {self.result.char} // {self.result.charStr}')
		print(f'Msg: {self.result.msgDecrypted}')
		print('###########################')


