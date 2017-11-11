# http://scikit-learn.org/stable/modules/neural_networks_supervised.html
from sklearn.neural_network import MLPClassifier, MLPRegressor

# Our X data.
X = [
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

# Our labels, or otherwise y data.
y = [0, 0, 0, 1, 1, 1]

# Our test data.
x_test = [
    [123, 191, 83, 262, 154, 140],  # Should be 1
    [139, 155, 139, 157, 162, 140], # Should be 0
]

# Class MLPClassifier implements a multi-layer perceptron (MLP)
# algorithm that trains using Backpropagation.
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(4, 6, 2), random_state=1)

clf.fit(X, y)
                   
print(list(clf.predict(x_test)))