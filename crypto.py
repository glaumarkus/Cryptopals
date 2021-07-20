from converters import str2bytes
import base64
from Crypto.Cipher import AES

def XOR(first, second):
	
	if type(first) == str or type(second) == str:
		raise Exception('Input is not in Bytes Format!')

	if len(first) == len(second):
		return bytes(a ^ b for (a, b) in zip(first, second))

	second = [second[i % len(second)] for i in range(len(first))]
	return bytearray(bytes(a ^ b for (a, b) in zip(first, second)))

def decrypt(data, key, mode=AES.MODE_ECB):
	enc = base64.b64decode(data)
	cipher = AES.new(key, mode)
	return cipher.decrypt(enc)