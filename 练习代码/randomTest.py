def ranSort():
	ls=[]
	for i in range(100):
		tmp=random.randrange(1,101,1)
		ls.append(tmp)
		print i+1, tmp
	ls.sort()

	print '----------------------------------------------------------------------'
	print ls

	cnt=1
	index=0
	dic={}
	for j in range(99):
		if ls[j+1] == ls[j]:
			cnt=cnt+1
		else:
			dic[str(ls[index])]=cnt
			cnt=1
			index=j+1
			dic[str(ls[index])]=cnt
	if ls[99]==ls[98]:
		dic[str(ls[index])]=cnt
	
	print '----------------------------------------------------------------------'
	print dic

	lsp=[]
	for k in dic.keys():
		lsp.append(int(k))
	lsp.sort()
	print '----------------------------------------------------------------------'
	print lsp

	print '----------------------------------------------------------------------'
	total=0
	for x in lsp:
		a=dic[str(x)]
		total=total+a
		print x,a
	print '----------------------------------------------------------------------'
	print total
