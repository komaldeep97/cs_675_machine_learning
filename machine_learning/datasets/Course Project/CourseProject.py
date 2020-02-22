from sklearn.metrics import accuracy_score
from sklearn import svm
import random
import statistics
import sys

##import files

data_files = sys.argv[1]
f = open(data_files,'r')
test_data = []
x = f.readline()

while(x!=''):
    a = x.split()
    y = []
    for j in range(0, len(a), 1):
        y.append(float(a[j]))
    test_data.append(y)
    x = f.readline()
    
row_count = len(test_data)
column_count = len(test_data[0])


labelfile = sys.argv[2]
f = open(labelfile)
train_labels = {}
num = [0,0]
x = f.readline()
while(x != ''):
    a = x.split()
    train_labels[int(a[1])] = int(a[0])
    x = f.readline()
    num[int(a[0])] += 1

#Compute Mean for all features
mean_0 = []
mean_1 = []
mean = []
for j in range(0, column_count, 1):
    mean_0.append(0)
    mean_1.append(0)
    mean.append(0)

for i in range(0, row_count, 1):
    if(train_labels.get(i) != None and train_labels[i] == 0):
        for j in range(0, column_count, 1):
            mean_0[j] = mean_0[j] + test_data[i][j]
            
    if(train_labels.get(i) != None and train_labels[i] == 1):
        for j in range(0, column_count, 1):
            mean_1[j] = mean_1[j] + test_data[i][j]
            
for j in range(0, column_count, 1):
    mean_0[j] = mean_0[j]/num[0]
    mean_1[j] = mean_1[j]/num[1]

for i in range(column_count):
    mean[i] = (mean_0[i] + mean_1[i])/2
    
#Compute F-scores
f_scores = [0]*column_count
for i in range(column_count):
    a = (mean_1[i] - mean[i]) ** 2 + (mean_0[i] - mean[i]) ** 2
    
    b = 0
    c = 0
    for k in range(0, row_count, 1):
        if(train_labels.get(k) != None and train_labels[k] == 0):
            c = c + (test_data[k][i] - mean_0[i]) ** 2
        elif(train_labels.get(k) != None and train_labels[k] == 1):
            b = b + (test_data[k][i] - mean_1[i]) ** 2
            
    b = b / (num[1] - 1)
    c = c / (num[0] - 1)
    
    f_scores[i] = a /(b+c)

mean_fscores = statistics.mean(f_scores)
std_fscores = statistics.stdev(f_scores)

#Picking up threshold and dropping features

threshold = mean_fscores + 13 * std_fscores
print(threshold)
new_test_data = []


for i in range(0, row_count, 1):
    temp = []
    for j in range(0, column_count, 1):
        if(f_scores[j] > threshold):
            temp.append(test_data[i][j])
    new_test_data.append(temp)
            
new_column_count = len(new_test_data[0])

print(new_column_count)

rowIDS = []
for r in range(row_count):
    rowIDS.append(r)


random.shuffle(rowIDS)

#Converting train labels dict to list
dictList= list(train_labels.values())

train_data = []
valid_data = []

train_label = []
valid_label = []

for i in range(0, int(0.75 * row_count), 1):
    train_data.append(new_test_data[rowIDS[i]])
    train_label.append(dictList[rowIDS[i]])

for i in range(int(0.75 * row_count), row_count, 1):
    valid_data.append(new_test_data[rowIDS[i]])
    valid_label.append(dictList[rowIDS[i]])
        
clf = svm.SVC(gamma='scale')
clf.fit(train_data,train_label)
labels_check = list(clf.predict(valid_data))

# accuracy_score(valid_label,labels_check)

print("Accuracy:"accuracy_score(valid_label,labels_check))
        
        
    