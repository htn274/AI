
from scipy.io import arff
import numpy as np
import pandas as pd
import math
import random

alpha = 1

#Handle data
def converByte(line):
    # legs = line[12]
    converted = [] 
    legs = [0] * 9
    for i in range(len(line) - 1):
        if i == 12:
            legs[int(line[i])] += 1
            converted = converted + legs
        else:
            converted.append(int(line[i]))
    converted.append(line[-1].decode('utf-8'))
    return converted

def loadArff(filename):
    raw_data = (arff.loadarff(filename))
    dataset = []
    for line in raw_data[0]:
        line = line.tolist()
        dataset.append(converByte(line[1:]))
    dataset = np.array(dataset)
    return dataset

def splitDataset(dataset, splitRatio = 0.7):
    train_size = int(len(dataset)) * splitRatio
    train_set = []
    copy = list(dataset)
    while len(train_set) < train_size:
        index = random.randrange(len(copy))
        train_set.append(copy.pop(index))

    return np.array(train_set), np.array(copy)

def accuracy_score(testSet, pred):
    correct = 0
    for check in zip(testSet, pred):
        if check[0] == check[1]:
            correct +=1 
        # else:
        #     print(check)
    return correct/float(len(testSet)) * 100.0

class MultinominalNB(object):
    #alpha for Laplace smoothing
    def __init__(self, alpha = 1.0):
        self.alpha = alpha
    def fit(self, X, y):
        self.classes = np.unique(y)
        seperated = [[x for x, t in zip(X, y) if t == c] for c in self.classes]
        count_sample = X.shape[0]
        self.class_prior_ = [np.log(len(i) / count_sample) for i in seperated]
        # self.class_prior_ = (len(i) / count_sample) for i in seperated]
        count = np.array([np.array(i).sum(axis=0) for i in seperated]) + self.alpha
        self.feature_prob = np.log(count / (count.sum(axis = 1)[np.newaxis].T))
        # self.feature_prob = (count / (count.sum(axis = 1)[np.newaxis].T))
        return self

    def predict_prob(self, X):
        return [(self.feature_prob * x).sum(axis = 1) + self.class_prior_ for x in X]

    def predict(self, X):
        pred = np.argmax(self.predict_prob(X), axis = 1)
        prob = np.max(self.predict_prob(X), axis = 1)
        return [self.classes[p] for p in pred], prob

def test_from_file(filename):
    testset = loadArff(filename)
    X_test = testset[:, :-1].astype(np.int)
    pred, prob = nb.predict(X_test)
    # print(pred)
    for i in range(len(pred)):
        print(pred[i], ':', np.exp(prob[i]))

if __name__ == "__main__":    
    # Load data from file
    dataset = loadArff("Zoo.arff")
    # split trainset and testset
    train = test = dataset
    X_train = train[:, :-1].astype(np.int)
    y_train = train[:, -1]
    X_test = test[:, :-1].astype(np.int)
    y_test = train[:, -1]
    # Train model
    nb = MultinominalNB().fit(X_train, y_train)
    y_pred = nb.predict(X_test)
    print("Acuracy score: ", accuracy_score(y_test, y_pred))
    # Test from file
    test_from_file('./Data/test.arff')
    
    

    