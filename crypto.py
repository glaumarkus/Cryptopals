import converters

def XOR(first, second):
	
	if type(first) == str:
		first = str2bytes(first)
	if type(second) == str:
		second = str2bytes(second)

	if len(first) == len(second):
		return bytes(a ^ b for (a, b) in zip(first, second))

	second = [second[i % len(second)] for i in range(len(first))]
	return bytearray(bytes(a ^ b for (a, b) in zip(first, second)))

