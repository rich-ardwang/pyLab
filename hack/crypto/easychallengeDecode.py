import base64

def decode1(ans):
	s = ''
	for i in ans:
		x  = ord(i) - 25
		x  = x ^ 36
		s += chr(x)
	return s

def decode2(ans):
	s = ''
	for i in ans:
		x  = i^36
		x  = x - 36
		s += chr(x)
	return s

def decode3(ans):
    return base64.b32decode(ans, casefold =False, map01= None)

number ="UC7KOWVXWVNKNIC2XCXKHKK2W5NLBKNOUOSK3LNNVWW3E==="
number = decode1(decode2(decode3(number)))
print(number)