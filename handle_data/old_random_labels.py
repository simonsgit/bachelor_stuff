__author__ = 'stamylew'
import numpy as np

####old function:

nol = np.amax(data) #number of labels
print nol

tol = np.unique(data) #number of labels
print tol

check = len(tol) - 1

assert(check == nol)

label = [] #list of labels
rol = []

for i in range(1, len(tol)): #creates list of label data
   label.append(data == i)
   random = np.random.random(data.shape) #create array with random values between 0 and 1
   rol.append(random * label[i])


rol1 = label[0] * random #randomization_of_label1

s = sum(label[0]) #number of pixels labeled by label1

total = data.shape[0] * data.shape[1] * data.shape[2] #total number of pixels of data


p = 0.3 #wanted percentage of labeled pixels

q = (total - p*s) / total * 100 #percentile
print q

subset = np.percentile(rol1, q) #qth percentile

sol1 = rol1 > subset #selection of label1 dtype=bool
print subset
print sol1[35:37, 66:68, 66:68]
print sum(sol1)


r = np.random.random(100)

p = np.percentile(r, 90)

print r
print p

print r>p
print r<p

print np.sum(r>p)
print np.sum(r<p)

quit()





print "datatype of data:"
print data.dtype

label1 = data == 1 #filter label 1
label2 = data == 2 #filter label 2
all_labels = data >= 1 #all labels

random = np.random.random(data.shape) #create array with random values between 0 and 1

randomization_label1 = np.multiply(random, label1) #multiply label1 array with random array elementwise



b = randomization_label1 > 0.5

b = b.astype(np.int32)
b = b.astype(np.bool)
b = b.astype(np.float)

print randomization_label1[b]



random_label1 = threshold(randomization_label1, 0.5)
print "shape"
print random_label1.shape
random_label1[random_label1 > 0]= int(1) #reset label array

print "datatype of random_label1:"
print random_label1.dtype
print random_label1[35:37, 66:68, 66:68]
