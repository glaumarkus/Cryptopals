from KeysizeGuesser import *
from SingleByteCracker import *



class RepeatingXORCracker():

	def __init__(self):
		self.success = False
		self.KeysizeGuesser = KeysizeGuesser()
		self.key = None

	def crack(self, bytestring):

		if type(bytestring) != bytearray:
			raise Exception('Input is not in Bytearray Format!')

		# get keysize
		self.KeysizeGuesser.guess(bytestring)
		keysize = self.KeysizeGuesser.getKeysize()

		# make datablocks
		datablocks = makeBlocks(bytestring, keysize)

		self.key = ''

		for blockId in datablocks.keys():

			blockstring = datablocks[blockId]
			cracker = SingleCharXORCracker(mode=CrackerMode.CHARONLY)
			cracker.crack(bytearray(blockstring))

			if cracker.success:
				self.key += cracker.result.charStr

	def getKey(self):
		return self.key

