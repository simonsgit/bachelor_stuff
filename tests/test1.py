# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:12:29 2015

@author: stamylew
"""


import factorial
print "__name__ is:", __name__

import numpy as np
from factorial import factorial
import matplotlib as mpl
from matplotlib import pyplot as plt

#for i in range (1,101):
#    if i % 3 == 0 and i % 5 == 0:
#        print "fizzbuzz"
#    elif i % 3 == 0:
#        print "fizz"
#    elif i % 5 == 0:
#        print "buzz"
#    else:
#        print i
#s = "hello"
#print s[1:]   
#print s[2:4]
#print s[0:-1:1]
#print s[::2]

#import math
#from math import pi as circle_number
#print "cos(pi)=%f" % (math.cos(circle_number),)

#a = np.zeros((4,6), dtype=np.uint8)
#print a.ndim
#print a.shape[1]
#b = np.random.random(a.shape)
#c = a + b
#d = a * b
#e = a / (b +1)
#f = np.sqrt(b)
#print b

#a[:] = 1
#a[1,2] = 2
#s = np.sum(b)
#assert s == 7
#print s
#a[:,0] = 42
#a[0,...] = 42
#b = a[:,0:2]


#b = np.zeros((150,200), dtype=np.uint8)
#b[:,100] = 1
#b[75,:] = 1

#print b
#def f(x):
#    return np.sin(x)
#x = np.arange(-1.0, 1.0, 0.01)
#plt.xlabel('x')
#plt.ylabel('y')
#plt.title('Graph of sin(x) from -1 to 1')
#plt.plot(x, f(x))
#plt.axis([-1,1,-1,1])
#plt.savefig('graph')

#print factorial(5)
#
#a = np.asarray([[2,5,4,3,1,],[1,2,1,5,7]])
#print a
#print np.where(a == 4)
#print a[np.where(a == 1)]

a = [[4, 0, -1], 
     [2, 5, 4],
     [0, 0, 5]]
print a
print "eigenvectors: ", np.linalg.eig(a)
a =  np.array(a)

evs = np.array([[  0.00000000e+00,   4.47213595e-01,  -5.55111512e-16],
       [  1.00000000e+00,  -8.94427191e-01,  -1.00000000e+00],
       [  0.00000000e+00,   0.00000000e+00,   5.55111512e-16]])

invevs = np.linalg.inv(evs)
#print invevs
l = [[5, 0, 0],
     [0, 4, 0],
    [0, 0 ,5]]
#print l
b = np.dot(l, invevs)
#print b
c = np.dot(evs, b)
#print c
print np.dot(a, evs)
#import vigra
#
#vigra.impex.writeHDF5(evs, "data_delme.hdf5", "blubb", compression="lzf")
#
#l = vigra.readHDF5("data_delme.hdf5", "blubb")



#a = 5
#b = a == 3
#print b
#print np.shape(evs) == (3, 2)
#assert(np.shape(evs) == (3, 2)), "the shape schould be (3, 3)"
#print "atest", a[:-1, :]
#
##t = np.array([1,34,5])
#print np.dot(a, evs[0])
#print evs[0] * 5
