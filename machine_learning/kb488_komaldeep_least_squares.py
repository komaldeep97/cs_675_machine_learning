import sys
import random
import math

# Opening data file and converting it to list of list
datafile = open(sys.argv[1])
data = []
line = datafile.readline()

while(line != ''):
    array = line.split()
    array_list = []
    for i in range(len(array)):
        array_list.append(float(array[i]))
    array_list.append(1)
    data.append(array_list)
    line = datafile.readline()

row = len(data)
col = len(data[0])
datafile.close()

# Opening labelfile and converting it into dictonary
labelfile = open(sys.argv[2])
labels = {}
total_number = [0, 0]
line = labelfile.readline()

while(line != ''):
    array = line.split()
    labels[int(array[1])] = int(array[0])
    if int(array[0]) == 0:
        labels[int(array[1])] = -1
    total_number[int(array[0])] += 1
    line = labelfile.readline()
labelfile.close()

# Initializing weight vector
w = []
del_e = []
for i in range(col):
    w.append(random.uniform(-0.01, 0.01))
    del_e.append(0)

#dot product
def dot_product(a,b):
    return sum(a_i * b_i for a_i,b_i in zip(a,b))

eta = 0.001
theta = 0.001
previous_error = float ('inf')
for k in range(10000):
    compute_error = 0
    d = []
    for j in range(col):
        del_e[j] = 0
    for i  in range(row):
        if(labels.get(i) != None):
            d.append(labels[i] - dot_product(data[i],w))
            for j in range(col):
                del_e[j] += (labels[i] - dot_product(data[i],w)) * data[i][j]
    
    for i in range(len(d)):
        compute_error += (d[i]**2)/2

    error = previous_error - compute_error
    if(error <= theta):
        break

    for i in range(len(w)):
        w[i] = w[i] + (eta * del_e[i])
    previous_error = compute_error
print("Final Weight", w)
# Finding distance
normw = 0
for j in range(col-1):
    normw += w[j]**2
normw = math.sqrt(normw)
distance = abs(w[len(w)-1]/normw)
print("Distance from the origin is", distance)

# prediction
for i in range(row):
    if(labels.get(i) == None):
        dp = dot_product(data[i],w)
        if(dp>0):
            print("1", i)
        else:
            print("0", i)

