#!/usr/bin/env python3

from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

print("This is just a dummy classifier that simulates packet sizes in order")

streams = [
    # Stream
    [
        # Packets
        140, 160, 142, 157, 161, 139,
    ],
    [141, 159, 139, 156, 163, 142],
    [139, 162, 141, 153, 159, 138],

    [122, 192, 81, 263, 156, 138],
    [120, 188, 84, 266, 159, 142],
    [124, 189, 83, 259, 161, 134],
]

labels = [0, 0, 0, 1, 1, 1]

# We can either do a decision tree or a KNN classifier.
# clf = tree.DecisionTreeClassifier()
clf = KNeighborsClassifier()
clf = clf.fit(streams, labels)

x_test = [
    [123, 191, 83, 262, 154, 140],
    [139, 155, 139, 157, 162, 140],
]

print(clf.predict([x_test[0]]))
print(clf.predict([x_test[1]]))

predictions = clf.predict(x_test)

print(accuracy_score([1, 0], predictions))
