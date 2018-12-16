
from scipy.io import arff
import numpy as np
import pandas as pd
import math
import random

#Handle data
def converByte(line):
    converted = []
    for i in range(len(line) - 1):
        converted.append(int(line[i]))
    converted.append(line[-1].decode('utf-8'))
    return converted

def loadArff(filename):
    raw_data = arff.loadarff(filename)
    df_data = pd.DataFrame(raw_data[0])
    dataset = []
    for row in df_data.iterrows():
        index, data = row
        data = data.tolist()[1:]
        dataset.append(converByte(data))
    return dataset

#Summarize data
def splitDataset(dataset, splitRatio):
    train_size = int(len(dataset)) * splitRatio
    train_set = []
    copy = list(dataset)
    while len(train_set) < train_size:
        index = random.randrange(len(copy))
        train_set.append(copy.pop(index))

    return [train_set, copy]

def seperateByClass(dataset):
    seperated = {}
    for row in dataset:
        if row[-1] not in seperated:
            seperated[row[-1]] = []
        seperated[row[-1]].append(row)
    return seperated
        
# central middle of data        
def mean(numbers):
	return sum(numbers)/float(len(numbers))
 
# get standard deviation 
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)

def summarize(dataset):
    summaries = []
    data = [line[:-1] for line in dataset]
    for attribute in zip(*data):
        summaries.append((mean(attribute), stdev(attribute)))
    return summaries

def summarizeByClass(dataset):
    seperated = seperateByClass(dataset)
    summaries = {}
    for className, instances in seperated.items():
        summaries[className] = summarize(instances)

    return summaries

# Make prediction

if __name__ == "__main__":    
    data = loadArff('Zoo.arff')
    train, test = splitDataset(data, 0.7)    
    summariesEachClass = summarizeByClass(data)
    print(summariesEachClass)
    