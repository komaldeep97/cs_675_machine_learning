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

eta = 0.01
error = 1
theta = 0.000000001
if len(sys.argv) > 3:
	eta = float(sys.argv[3])
	theta = float(sys.argv[4])
print("Please Note that the value of eta is %s and the value of theta is %s. If you want to change that you can pass Eta as Argument3 and Theta as Argument4." % (eta, theta))
previous_error = float ('inf')
while (error > theta):
	condition = 1
	compute_error = 0
	d = []
	del_f = [0]*col

	for i  in range(row):
		condition = 0
		if(labels.get(i) != None):
			condition = dot_product(data[i],w)
			d.append(math.log(1 + math.exp(-labels[i] * condition)))
			for j in range(col):
				del_f[j] += (labels[i] - (1/(1 + math.exp(-condition)))) * data[i][j]
	
	for i in range(len(d)):
		compute_error += d[i]

	error = abs(previous_error - compute_error)
	# if(error <= theta):
	# 	break
	for i in range(len(w)):
		w[i] = w[i] + (eta * del_f[i])
	previous_error = compute_error
print("Final Weight", w)
# Finding distance
normw = 0
for j in range(col-1):
	normw += w[j]**2
normw = math.sqrt(normw)
print("||w|| =", normw)
distance = w[len(w)-1]/normw
print("Distance from the origin is", distance)

# prediction
for i in range(row):
	if(labels.get(i) == None):
		dp = dot_product(data[i],w)
		if(dp>0):
			print("1", i)
		else:
			print("0", i)
