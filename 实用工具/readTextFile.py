#!/usr/bin/env Python

'readTextFile.py -- read and display text file'

# get filename
fname = raw_input('Enter filename: ')
print fname

# attempt to open file for reading
try:
    fobj = open(fname, 'r')
except IOError, e:
    print "*** file open error:", e
else:
    # display contents to the screen
    for eachLine in fobj:
        print eachLine
    fobj.close()
    fname = raw_input('Enter:')
