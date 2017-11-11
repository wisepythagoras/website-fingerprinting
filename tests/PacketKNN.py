from scipy.spatial import distance

class PacketKNN():
    def fit(self, X_train, y_train):
        """ Create the classifier with the x and y data. """
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X_test):
        """ Predict the y type of each X_test. """
        predictions = []

        for row in X_test:
            # Get the closest element.
            label = self.closest(row)
            predictions.append(label)

        return predictions

    def closest(self, row):
        """ Compute the closest neighbor. """
        best_distance = distance.euclidean(row, self.X_train[0])
        best_index = 0

        for i in range(1, len(self.X_train)):
            # Compute the new distance.
            dist = distance.euclidean(row, self.X_train[i])

            if dist < best_distance:
                best_distance = dist
                best_index = i

        return self.y_train[best_index]
