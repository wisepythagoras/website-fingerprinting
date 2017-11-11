#!/usr/bin/env python3

from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from scipy.spatial import distance
from sys import exit

try:
    classifier = joblib.load("./classifier.dmp")
except FileNotFoundError:
    print("The model is not there")
    exit(1)

x_test = [
    [123, 191, 83, 262, 154, 140],
    [139, 155, 139, 157, 162, 140],
]

print(classifier.predict([x_test[0]]))
print(classifier.predict([x_test[1]]))
