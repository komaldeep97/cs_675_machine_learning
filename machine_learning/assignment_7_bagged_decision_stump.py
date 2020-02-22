import sys
import random

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

testdata = []
traindata = []

test_predictions = [0] * row

for k in (0, 100):
    bootstrap = []
    column = 0
    threshold = 0
    list_data = [x for x in range(row) if(labels.get(x) != None)]
    for i in range(row):
        if(labels.get(i) != None):
            bootstrap.append(random.choice(list_data))
    final = {}
    for i in range(col):
        for j in range(len(bootstrap)):
            left_tree = []
            right_tree = []
            lp = 0
            rp = 0
            for k in range(len(bootstrap)):
                if data[j][i] <= data[k][i]:
                    left_tree.append(data[k])
                    if(labels.get(k) == -1):
                        lp += 1
                else:
                    right_tree.append(data[k])
                    if(labels.get(k) == -1):
                        rp += 1
            lsize = len(left_tree)
            rsize = len(right_tree)
            if lsize == 0:
                gini = (rsize/row) * (rp/rsize) * (1-(rp/rsize))
            elif rsize == 0:
                gini = (lsize/row) * (lp/lsize) * (1-(lp/lsize))
            else:
                gini = ((lsize/row) * (lp/lsize) * (1-(lp/lsize))) + \
                    ((rsize/row) * (rp/rsize) * (1-(rp/rsize)))

            final[gini] = [i, data[j][i]]
    column = final[min(final)][0]
    threshold = final[min(final)][1]
    count_pos = 0
    count_neg = 0
    for i in range(row):
        if(labels.get(i) != None):
            if (data[i][column] > threshold):
                if(labels.get(i) == -1):
                    count_neg += 1
                elif(labels.get(i) == 1):
                    count_pos += 1
    for i in range(row):
        if(labels.get(i) == None):
            if count_neg > count_pos:
                if (data[i][column] > threshold):
                    test_predictions[i] += -1
                else:
                    test_predictions[i] += 1
            elif count_neg < count_pos:
                if (data[i][column] < threshold):
                    test_predictions[i] += -1
                else:
                    test_predictions[i] += 1
for i in range(row):
    if(labels.get(i) == None):
        if(test_predictions[i] > 0):
            print("1", i)
        else:
            print("0", i)
        # print("{'columns k': %d, 'split s': %f}" % (final[min(final)][0], final[min(final)][1]))
