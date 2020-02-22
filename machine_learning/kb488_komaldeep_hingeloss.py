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

print(">>>>.data",data)
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
print(">>>>>>>>>>>>labelfile", labels)
print(">>>>>>>>>>w", w)
#dot product
def dot_product(a,b):
    return sum(a_i * b_i for a_i,b_i in zip(a,b))

eta = 0.001
error = 1
theta = 0.000000001
if len(sys.argv) > 3:
    eta = float(sys.argv[3])
    theta = float(sys.argv[4])
print("Please Note that the value of eta is %s and the value of theta is %s. If you want to change that you can pass Eta as Argument3 and Theta as Argument4." % (eta, theta))
previous_error = float ('inf')
# for k in range(10000):
while (error > theta):
    condition = 1
    compute_error = 0
    d = []
    del_f = [0]*col

    for i  in range(row):
        if(labels.get(i) != None):
            condition = labels[i] * dot_product(data[i],w)
            d.append(labels[i] - dot_product(data[i],w))
            for j in range(col):
                if(condition<1):
                    del_f[j] += -1 * (labels[i] * data[i][j])
                else:
                    del_f[j] += 0
    
    for i in range(len(d)):
        compute_error += d[i]**2

    error = abs(previous_error - compute_error)
    # if(error <= theta):
    #   break
    for i in range(len(w)):
        w[i] = w[i] - (eta * del_f[i])
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
