import sys
from math import sqrt


# Opening data file and converting it to list of list
datafile = open(sys.argv[1])
data = []
line = datafile.readline()

while(line != ''):
	array = line.split()
	array_list = []
	for i in range(len(array)):
		array_list.append(float(array[i]))
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
	
# Finding the mean for 0 and 1label data
m0 = []
m1 = []
for j in range(col):
	m0.append(0.01)
	m1.append(0.01)

# for col 0
for i in range(row):
	if(labels.get(i) != None and labels[i]==0):
		for j in range(col):
			m0[j] += data[i][j]

	# for column 1
	elif(labels.get(i) != None and labels[i]==1):
		for j in range(col):
			m1[j] += data[i][j]

for j in range(col):
	m0[j] = m0[j]/total_number[0]
	m1[j] = m1[j]/total_number[1]

# Finding the Std Devation for 0 and 1 label data
s0 = [];
s1 = [];

for j in range(col):
    s0.append(0);

for j in range(col):
    s1.append(0);

for i in range(row):
    if(labels.get(i) != None and labels[i] == 0):
       for j in range(col):
            s0[j] = s0[j] + (data[i][j] - m0[j])**2;
    if(labels.get(i) != None and labels[i] == 1):
        for j in range(col):
            s1[j] = s1[j] + (data[i][j] - m1[j])**2;

for j in range(col):
    if(s0[j] != 0):
        s0[j] = sqrt(s0[j]/total_number[0])
    else:
        s0[j] = 0.1
    if(s1[j] != 0):
        s1[j] = sqrt(s1[j]/total_number[1])
    else:
        s1[j] = 0.1

## Predict the labels for the data whose labels are missing

for i in range(row):
	if(labels.get(i) == None):
		d0 = 0
		d1 = 0
		for j in range(col):
			d0 += ((data[i][j] - m0[j])/s0[j])**2;
			d1 += ((data[i][j] - m1[j])/s1[j])**2;
		if(d0<d1):
			print("0", i)
		else:
			print("1", i)
