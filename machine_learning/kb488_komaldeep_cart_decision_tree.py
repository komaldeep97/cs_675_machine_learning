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

final={}
for i in range(col):
	for j in range(row):
		left_tree=[]
		right_tree=[]
		lp=0
		rp=0
		for k in range(row):
			if data[j][i] <= data[k][i]:
				left_tree.append(data[k])
				if(labels.get(k) == -1):
					lp+=1
			else:
				right_tree.append(data[k])
				if(labels.get(k) == -1):
					rp+=1
		lsize=len(left_tree)
		rsize=len(right_tree)
		if lsize == 0:
			gini = (rsize/row) * (rp/rsize) * (1-(rp/rsize))
		elif rsize == 0:
			gini = (lsize/row) * (lp/lsize) * (1-(lp/lsize))
		else:
			gini = ((lsize/row) * (lp/lsize) * (1-(lp/lsize))) + ((rsize/row) * (rp/rsize) * (1-(rp/rsize)))
					
		final[gini] = [i,data[j][i]]

print("{'columns k': %d, 'split s': %f}" % (final[min(final)][0], final[min(final)][1]))
