
"""traindata = "/content/drive/My Drive/traindata"
trainlabels = "/content/drive/My Drive/trainlabels"
testdata = "/content/drive/My Drive/testdata"
"""
import sys

traindata = sys.argv[1]
trainlabels = sys.argv[2]
testdata = sys.argv[3]

filedata = open(traindata).readlines()

lst = []
for line in filedata:
    lst.append([ float(x) for x in line.split()])

cols = len(lst[1])
rows = len(lst)
#print(rows, cols)

trainlabels = open(trainlabels).readlines()

trainlst = []
for line in trainlabels:
    trainlst.append([ float(x) for x in line.split()])

train_newlabels = []
for i in range(0, rows,1) :
  l1 = trainlst[i]
  train_newlabels.append(l1[0])
#print (train_newlabels)

print ("Train Data & Train Labels read")

import numpy as np
def train_test_split(listX, listY, train_size = 0.9):
        indexes = list(range(len(listX)))        
        np.random.shuffle(indexes)        
        train_len = int(train_size*len(indexes))        
        trainX, trainY = [], []        
        for idx in indexes[:train_len]:
            trainX.append(listX[idx])
            trainY.append(listY[idx])
  
        testX, testY = [], []
        for idx in indexes[train_len:]:
            testX.append(listX[idx])
            testY.append(listY[idx])
  
        return trainX, testX, trainY, testY

X_train, X_test, y_train, y_test = train_test_split(lst,train_newlabels ,0.9)

print ("Train & Validation Split Created")
"""Correlation Coefficient"""

def pearson (xi,xm,yi,ym):
  #print (xm,ym)
  num = 0
  sx = 0
  sy = 0
  dnum = 0
  for i,j in zip(xi,yi):
    #print (i,j)
    num = num + ((i - xm)*(j-ym))
    sx = sx + (i-xm)**2
    sy = sy + (j-ym)**2 
  dnum = dnum + ((math.sqrt(sx))*(math.sqrt(sy)))
  #print(dnum)
  if((num == 0) or (dnum == 0)):
    r = 0
  else:
    r = num / dnum
  return r

import statistics
import math

cor = []
cols = len(X_train[0])
rows = len(X_train)
for j in range(0, cols, 1):
  d = []
  y = []
  for i in range(0, rows, 1):
    d.append(X_train[i][j])
    y.append(y_train[i])
  dataX = d
  meanX = statistics.mean(dataX)
  dataY = y
  meanY = statistics.mean(dataY)
  cor.append(pearson(dataX,meanX,dataY,meanY))
#print(cor)

print ("Pearson Correlation Coefficient Calculated")

import numpy as np
cor = np.array(cor)
sort_index = np.argsort(-cor)
feature = []
for i in range(0,20):
  feature.append(sort_index[i])
print ("Total features Selected:",len(feature))
print (feature)

X_newtrain = []
X_newvalid = []
for j in feature:
  l1 = []
  l2 = []
  for i in range(0, len(X_train),1):
    l1.append(X_train[i][j])
  X_newtrain.append(l1)
  for i in range(0, len(X_test),1):
    l2.append(X_test[i][j])
  X_newvalid.append(l2)
X_newtrain = np.transpose(X_newtrain)
X_newvalid = np.transpose(X_newvalid)

print ("Data with features extracted")
print ("Performing SVM")

from sklearn import svm

#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(X_newtrain, y_train)

#Predict the response for test dataset
y_validpred = clf.predict(X_newvalid)

from sklearn import metrics

# Model Accuracy: how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_validpred))

tdata = open(testdata).readlines()
lsttst = []
for line in tdata:
    lsttst.append([ float(x) for x in line.split()])
cols = len(lst[1])
rows = len(lst)
#print(rows, cols)

X_testdata = []
for j in feature:
  l2 = []
  for i in range(0, len(tdata),1):
    l2.append(lsttst[i][j])
  X_testdata.append(l2)
X_testdata = np.transpose(X_testdata)

print ("Test Data read and feature extracted")

from sklearn import svm

#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(X_newtrain, y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_testdata)

print ("predicted labels")
for i in range(0, len(y_pred),1):
  print (y_pred[i])