from converters import *
from utility import *
import base64
from Crypto.Cipher import AES
from math import ceil
import os



'''
XOR function
'''
def XOR(first, second):
	
	if type(first) == str or type(second) == str:
		raise Exception('Input is not in Bytes Format!')

	if len(first) == len(second):
		return bytes(a ^ b for (a, b) in zip(first, second))

	second = [second[i % len(second)] for i in range(len(first))]
	return bytearray(bytes(a ^ b for (a, b) in zip(first, second)))


'''
pkcs7 padding function
'''
def pkcs7padding(plaintext, blocksize=16):
	'''
	if type(plaintext) == bytes:
		plaintext = bytes2str(plaintext)
	'''
	size = len(plaintext)

	if size % blocksize == 0:
		return plaintext

	numBlocks = size // blocksize + 1
	numPads = blocksize - (size % blocksize)
	padding = numPads * (numPads).to_bytes(1, byteorder='little')

	if type(plaintext) == bytes:
		return plaintext + padding

	return plaintext + bytes2str(padding)


'''
remove pkcs7 padding function
'''
def removepkcs7padding(plaintext):
	if type(plaintext[-1]) == int:
		plaintext = plaintext[:-plaintext[-1]]
	return bytes2str(plaintext)


'''
Utility function to split data in blocks and the option to append pkcs7 padding
'''
def makeAESBlocks(data,blocksize=16, padding=True):
	if padding:
		data = pkcs7padding(data, blocksize)
	numBlocks = ceil(len(data) / blocksize)
	return [data[i * blocksize : i * blocksize + blocksize] for i in range(numBlocks)]


'''
Basic AES-ECB decryption function, replaced later with Cipher Class
'''
def decrypt(data, key, mode=AES.MODE_ECB):
	enc = base64.b64decode(data)
	cipher = AES.new(key, mode)
	return cipher.decrypt(enc)


'''
Base Cipher class with ECB encryption
'''
class Cipher:
	
	def __init__(self, key, blocksize=16):
		self.cipher = AES.new(key, AES.MODE_ECB)
		self.blocksize = blocksize
		
	def encryptBlockECB(self, plaintext):
		ciphertext = self.cipher.encrypt(plaintext)
		return ciphertext

	def decryptBlockECB(self, ciphertext):
		plaintext = self.cipher.decrypt(ciphertext)
		return plaintext

	def encryptECB(self, plaintext):
		# add padding
		blocks = makeAESBlocks(plaintext, self.blocksize)
		ciphertext = b''.join([self.encryptBlockECB(block) for block in blocks])
		return ciphertext
	
	def decryptECB(self, ciphertext):
		blocks = makeAESBlocks(ciphertext, self.blocksize, padding=False)
		plaintext = b''.join([self.decryptBlockECB(block) for block in blocks])
		return removepkcs7padding(plaintext)


'''
CBC Cipher Class
'''
class CBC(Cipher):
	
	def __init__(self, key, iv, blocksize=16):
		super(CBC,self).__init__(key, blocksize)
		self.iv = iv
	
	def encrypt(self, plaintext):
		blocks = makeAESBlocks(plaintext, self.blocksize, padding=True)
		newKey = self.iv
		ciphertext = b''
		
		for block in blocks:
			block = XOR(str2bytes(block), newKey)
			newKey = self.encryptBlockECB(bytes(block))
			ciphertext += newKey
			
		return ciphertext
	
	def decrypt(self, ciphertext): 
		blocks = makeAESBlocks(ciphertext, self.blocksize, padding=False)
		newKey = self.iv
		plaintext = b''
		
		for block in blocks:
			changedBlock = self.decryptBlockECB(block)
			changedBlock = XOR(changedBlock, newKey)
			plaintext += changedBlock
			newKey = block
		
		return removepkcs7padding(plaintext)


'''
Encryption Oracle Base
'''
class EncryptionOracle:
	
	def __init__(self, plaintext, key=None):
		
		self.key = os.urandom(16)
		self.padFront = bytes2str(b''.join([(RNGint(1,127)).to_bytes(1, byteorder='little') for i in range(RNGint(5,10))]))
		self.padBack = bytes2str(b''.join([(RNGint(1,127)).to_bytes(1, byteorder='little') for i in range(RNGint(5,10))]))
		self.encMode = int.from_bytes(os.urandom(1), byteorder="little") / 255
		self.paddedPlaintext = self.padFront + plaintext + self.padBack
		
		if self.encMode >= 0.5:
			self.encryptECB(self.paddedPlaintext)
		else:
			self.encryptCBC(self.paddedPlaintext)
			
	def encryptECB(self, plaintext):
		self.cipher = Cipher(self.key)
		self.ciphertext = self.cipher.encryptECB(plaintext)
		
	def encryptCBC(self, plaintext):
		self.cipher = CBC(self.key, os.urandom(16))
		self.ciphertext = self.cipher.encrypt(plaintext)
	
	def getEncrypted(self):
		return self.ciphertext
	
	def getMode(self):
		if self.encMode >= 0.5:
			return 'ECB'
		return 'CBC'
		
	def guessMode(self):
		
		numBlocks = len(self.ciphertext) // 16
		blocks = [self.ciphertext[i * 16 : i * 16 + 16] for i in range(numBlocks)]
		if len(set(blocks)) != numBlocks:
			return 'ECB'
		return 'CBC'


'''
ECB Cracker via Oracle
'''
class ECBCracker:
	
	def __init__(self):
		self.key = os.urandom(16)
		self.blocksize = None
		self.cipher = Cipher(self.key, 16)
				
	def encrypt(self, buffer, data):
		return self.cipher.encryptECB(buffer + data)
	
	def findBlocksize(self):
		initSize = len(self.encrypt(b'x',b''))
		for i in range(1,100):
			if len(self.encrypt(b'x' * i, b'')) != initSize:
				self.blocksize = i - 1
				return
		
	def makeCharDict(self):
		
		bufferSize = self.blocksize - 1
		charDict = {
			self.cipher.encryptECB(
				(b'x' * bufferSize) + (bytes([i]))
			) 
			: bytes([i])
			for i in range(256)
		}
		return charDict
	
	def crack(self, ciphertext):
	
		plaintext = []
		
		# this is how long i need to iterate
		msgSize = len(ciphertext)

		# buffer of known chars
		buffer = b'x' * (self.blocksize - 1)

		# make char dict
		charDict = self.makeCharDict()

		# iterations to find msgs
		for i in range(msgSize):

			byteToDecrypt = ciphertext[i]

			# make msg
			toEncrypt = buffer + bytes([byteToDecrypt])
			
			encrypted = self.cipher.encryptBlockECB(toEncrypt)

			plaintext.append(
				charDict[encrypted]
			)
			
		return bytes2str(b''.join(plaintext))


'''
random key
'''
def getRandomBytes(n):
	return os.urandom(n)
