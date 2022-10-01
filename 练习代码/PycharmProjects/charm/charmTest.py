import numpy as np

C = np.array(
    [
        [1, 2, 0, -1],
        [2, 0, -1, 1],
        [0, -1, 1, 2],
        [-1, 1, 2, 2]
    ]
)
C.T
print 'A:'
print C
print '10*A^-1:'
print 10*np.linalg.inv(C)
