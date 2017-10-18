from sklearn import metrics
import tensorflow as tf
import numpy as np
from tensorflow.contrib import learn

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
feature_columns = [tf.contrib.layers.real_valued_column("", dimension=1)]

# Create the deep neural network classifier with 10, 20 and 30 units on
# each of the three layers, respectively.
classifier = learn.DNNClassifier(hidden_units=[10, 20, 30], n_classes=3, feature_columns=feature_columns)

# Train the neural network.
classifier.fit(np.array(streams), np.array(labels), steps=200)

x_test = [
    [123, 191, 83, 262, 154, 140],
    [139, 155, 139, 157, 162, 140],
]

one_predict = classifier.predict(np.array([x_test[0]]))
zero_predict = classifier.predict(np.array([x_test[1]]))
print(list(one_predict))
print(list(zero_predict))
