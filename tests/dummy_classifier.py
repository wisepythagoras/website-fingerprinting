#!/usr/bin/env python3

from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from scipy.spatial import distance

print("This is just a dummy classifier that simulates packet sizes in order")

streams = [
    # Stream
    [140, 160, 142, 157, 161, 139],
    [141, 159, 139, 156, 163, 142],
    [139, 162, 141, 153, 159, 138],

    [122, 192, 81,  263, 156, 138],
    [120, 188, 84,  266, 159, 142],
    [124, 189, 83,  259, 161, 134],

    [62,  132, 181, 163, 176, 158],
    [60,  138, 184, 166, 179, 152],
    [64,  139, 183, 159, 171, 154],
]

labels = [0, 0, 0, 1, 1, 1, 2, 2, 2]

# We can either do a decision tree or a KNN classifier.
# We don't use a Decision Tree because of the information here:
# http://scikit-learn.org/stable/modules/tree.html
#clf = tree.DecisionTreeClassifier()

# http://scikit-learn.org/stable/modules/neighbors.html
clf = KNeighborsClassifier()
#clf = KNeighborsRegressor()

# http://scikit-learn.org/stable/modules/naive_bayes.html
#clf = GaussianNB()
#clf = MultinomialNB()

clf = clf.fit(streams, labels)

x_test = [
    [123, 191, 83,  262, 154, 140],
    [139, 155, 139, 157, 162, 140],
    [65,  130, 185, 158, 175, 150],
]

# Save a snapshot of this classifier.
joblib.dump(clf, "./classifier.dmp", compress=9)

print(clf.predict([x_test[0]]))
print(clf.predict([x_test[1]]))
print(clf.predict([x_test[2]]))

predictions = clf.predict(x_test)

print("Accuracy: %s%%" % (accuracy_score([1, 0, 2], predictions) * 100,))

