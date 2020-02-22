from sklearn.svm import LinearSVC
from sklearn import svm
import sys
import random
import warnings
warnings.filterwarnings('ignore')

# Opening data file and converting it to list of list
datafile = open(sys.argv[1])
data = []
line = datafile.readline()

while(line != ''):
    array = line.split()
    array_list = [1.0]
    for i in range(len(array)):
        array_list.append(float(array[i]))
    #array_list.append(1)
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

k = int(sys.argv[3])

while(line != ''):
    array = line.split()
    labels[int(array[1])] = int(array[0])
    if int(array[0]) == 0:
        labels[int(array[1])] = -1
    total_number[int(array[0])] += 1
    line = labelfile.readline()
labelfile.close()

train_X = []
train_Y = []
test_X = []
row_num = []
for i in range(row):
    if(labels.get(i) != None):
        train_X.append(data[i])
        train_Y.append(labels.get(i))
    else:
        test_X.append(data[i])
        row_num.append(i)


# dot product
def dot_product(a, b):
    return sum(a_i * b_i for a_i, b_i in zip(a, b))


def getbestC(train, labels):

    random.seed()
    allCs = [.001, .01, .1, 1, 10, 100]
    error = {}
    for j in range(0, len(allCs), 1):
        error[allCs[j]] = 0
    rowIDs = []
    for i in range(0, len(train), 1):
        rowIDs.append(i)
    nsplits = 10
    for x in range(0, nsplits, 1):
        # Making a random train/validation split of ratio 90:10
        newtrain = []
        newlabels = []
        validation = []
        validationlabels = []

        random.shuffle(rowIDs)  # randomly reorder the row numbers
        # print(rowIDs)

        for i in range(0, int(.9*len(rowIDs)), 1):
            newtrain.append(train[i])
            newlabels.append(labels[i])
        for i in range(int(.9*len(rowIDs)), len(rowIDs), 1):
            validation.append(train[i])
            validationlabels.append(labels[i])

        #### Predict with SVM linear kernel for values of C={.001, .01, .1, 1, 10, 100} ###
        for j in range(0, len(allCs), 1):
            C = allCs[j]
            clf = svm.LinearSVC(C=C)
            clf.fit(newtrain, newlabels)
            prediction = clf.predict(validation)

            err = 0
            for i in range(0, len(prediction), 1):
                if(prediction[i] != validationlabels[i]):
                    err = err + 1

            err = err/len(validationlabels)
            error[C] += err
            # print("err=",err,"C=",C,"split=",x)

    bestC = 0
    minerror = 100
    keys = list(error.keys())
    for i in range(0, len(keys), 1):
        key = keys[i]
        error[key] = error[key]/nsplits
        if(error[key] < minerror):
            minerror = error[key]
            bestC = key

    # print(bestC,minerror)
    return [bestC, minerror]


#z_test = [[0] * len(test_X)] * k
z_test = []
z_train = []
for i in range(0, len(test_X), 1):
    p = []
    for j in range(k):
        p.append(0)
    z_test.append(p)

for i in range(0, len(train_X), 1):
    q = []
    for j in range(k):
        q.append(0)
    z_train.append(q)
    

#z_test = [[0] * k ] * len(test_X)
#z_train = [[0] * len(train_X)] * k
#_train = [[0] * k ] * len(train_X)

for i in range(k):
    z = []
    z1 = []
    # Initializing weight vector
    w = []
    for q in range(0, col, 1):
        w.append(random.uniform(-1, 1))

    for j in range(len(train_X)):
        z.append(dot_product(train_X[j], w))
    #new_w = []
    #for _ in range(col):
        #new_w.append(random.uniform(min(z), max(z)))
    w[0] = random.uniform(min(z), max(z))
    z = []
    for j in range(len(train_X)):
        z.append(dot_product(train_X[j], w))
    for j in range(len(train_X)):
        if (z[j] > 0.0):
            z_train[j][i] = 1
        else:
            z_train[j][i] = 0
    for j in range(len(test_X)):
        z1.append(dot_product(test_X[j], w))
    for j in range(len(test_X)):
        #z_test[i][j] = z1[j]
        if (z1[j] > 0.0):
            z_test[j][i] = 1
        else:
            z_test[j][i] = 0


bestC, minerror = getbestC(z_train, train_Y)
print("BestC:", bestC)
print("Min Error:", minerror)

clf = LinearSVC(C=bestC, max_iter=10000)
clf.fit(z_train, train_Y)
predictions1 = clf.predict(z_test)

for i, label in enumerate(predictions1):
    if label == -1:
        predictions1[i] = 0
for i in range(0, len(row_num), 1):
    print(predictions1[i],row_num[i])

