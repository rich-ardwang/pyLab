#!/usr/bin/env Python
#coding:utf-8


# get filename
fname = raw_input('Enter filename: ')
print fname

dictName={}
#cha=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
cha=['二画','三画','四画','五画','六画','七画','八画','九画']
# attempt to open file for reading
try:
	fobj = open(fname, 'r')
except IOError, e:
	print "*** file open error:", e
else:
	# display contents to the screen
	idxName=''
	for eachLine in fobj:
		lstName=eachLine.split()
		if lstName[0] in cha:
			idxName=lstName[0]
			dictName[idxName]=[]
		else:
			dictName[idxName].extend(lstName)
	#print str(dictName['C']).decode('string_escape')
	fobj.close()

#Output
output_file_path=fname+'.txt'
with open(output_file_path,'w') as fw:
	keys=dictName.keys()
	keys.sort()
	for k in keys:
		fw.write(k)
		fw.write('\n')
		for i in range(len(dictName[k])):
			fw.write(dictName[k][i])
			fw.write('\n')

	fw.write('-------------------------------')
	fw.write('\n')
	fw.write('-------------------------------')
	fw.write('\n')
	totalCnt=0
	for k in keys:
		cnt=len(dictName[k])
		totalCnt=totalCnt+cnt
		fw.write('%s cnt: %d' % (k,cnt))
		fw.write('\n')
	fw.write('\n')
	fw.write('Total cnt: %d' % (totalCnt))
	fw.close()