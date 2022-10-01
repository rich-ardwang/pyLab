a = 'harambe'
b = ':\"AL_RT^L*.?+6/46'
#print(b)
flag = ''
for i in range(len(b)):
    c = ord(a[i % 7]) ^ ord(b[i])
    flag += chr(c)
print(flag)