from converters import str2bytes

def XOR(first, second):
	
	if type(first) == str or type(second) == str:
		raise Exception('Input is not in Bytes Format!')

	if len(first) == len(second):
		return bytes(a ^ b for (a, b) in zip(first, second))

	second = [second[i % len(second)] for i in range(len(first))]
	return bytearray(bytes(a ^ b for (a, b) in zip(first, second)))

