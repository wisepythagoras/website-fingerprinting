#!/usr/bin/env python3

from sklearn import tree

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

clf = tree.DecisionTreeClassifier()
clf = clf.fit(streams, labels)

print(clf.predict([[123, 191, 83, 262, 154, 140]]))
print(clf.predict([[139, 155, 139, 157, 162, 140]]))
