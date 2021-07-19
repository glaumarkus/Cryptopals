import converters

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