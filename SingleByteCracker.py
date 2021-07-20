from enum import Enum
from textoperations import *
import converters
from utility import *


class CrackerMode(Enum):
	CHARONLY = 1
	WORDONLY = 2
	BOTH = 3


class probabilityRatio:

	def __init__(self, mode=CrackerMode.CHARONLY):
		self.mode = mode
		self.charRatio = 0.0
		self.wordRatio = 0.0

	def __float__(self):
		if self.mode==CrackerMode.CHARONLY:
			return self.charRatio
		elif self.mode==CrackerMode.WORDONLY:
			return self.wordRatio
		return 0.0

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

	def __init__(self, mode=CrackerMode.BOTH, thresholdWords=0.4, wordListMode=WordListMode.MEDIUM):
		self.mode = mode
		self.thresholdWords = thresholdWords
		self.metrics = {}
		self.metricsOrdered = None
		self.result = crackResult()
		self.success = False
		self.wordListMode = wordListMode

	def crack(self, bytestring):

		if type(bytestring) != bytearray:
			raise Exception('Input is not in Bytes Format!')

		# iterate through charset and evaluate based on mode
		for char in range(256):

			# xor data
			tmpString = bytes2str(
			bytearray(
				[byte ^ char for byte in bytestring]
				)
			)

			# fill metrics
			if self.mode == CrackerMode.CHARONLY:
				self.metrics[char] = numFrequencyEstimation(tmpString)

			if self.mode == CrackerMode.WORDONLY:
				self.metrics[char] = numEnglishWords(tmpString, self.wordListMode)


		# order dictionary with valsu
		self.metricsOrdered = sortDict(self.metrics, reverse=True)

		# if not found
		if len(list(self.metricsOrdered.keys())) == 0:
			return

		# fill record
		self.success = True
		self.result.char = next(iter(self.metricsOrdered))
		self.result.charStr = chr(self.result.char)
		self.result.probability = float(self.metricsOrdered[self.result.char])
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
		print(f'Probability: {self.result.probability}')
		print(f'Msg: {self.result.msgDecrypted}')
		print('###########################')


