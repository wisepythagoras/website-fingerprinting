#!/usr/bin/env python

import os
import re
import sys
import json
import dpkt
import random
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib


def shuffle(x, y):
    """ Shuffle the datasets. """

    for n in range(len(x) - 1):
        rnd = random.randint(0, (len(x) - 1))
        x1 = x[rnd]
        x2 = x[rnd - 1]

        y1 = y[rnd]
        y2 = y[rnd - 1]

        x[rnd - 1] = x1
        x[rnd] = x2

        y[rnd - 1] = y1
        y[rnd] = y2

    return x, y


def read_pcap_file(file):
    """ Read the pcap file and return the sizes of the packets. """

    # Read the file.
    fp = open(file)

    # Create the pcap object
    pcap = dpkt.pcap.Reader(fp)

    # This is the array that will contain all the packet sizes.
    sizes = [0] * 30
    i = 0

    # Loop through all the packets and save the sizes.
    for ts, buf in pcap:
        if i >= 30:
            break

        sizes[i] = len(buf)

        i += 1

    # Finally return the sizes.
    return sizes


def train(streams, labels):
    """ This function trains the classifier with the data. """

    # Shuffle the arrays.
    streams, labels = shuffle(streams, labels)

    stream_amount = len(streams)
    training_size = int(stream_amount * 0.9)

    # Get 70% of the streams for training purposes.
    training_x = streams[:training_size]
    training_y = labels[:training_size]

    # Get 30% of the streams for testing purposes
    testing_x = streams[training_size:]
    testing_y = labels[training_size:]

    print("Training size: {}".format(training_size))
    print("Testing size:  {}".format(stream_amount - training_size))

    # Initialize the classifier.
    clf = MultinomialNB()

    # Now lets train our KNN classifier.
    clf = clf.fit(training_x, training_y)

    # Save a snapshot of this classifier.
    joblib.dump(clf, "./classifier-nb.dmp", compress=9)

    # Get the prediction.
    predictions = clf.predict(testing_x)

    print("Accuracy: %s%%" % (accuracy_score(testing_y, predictions) * 100,))


# Read the configuration and start training.
with open('config.json') as fp:
    print("* Parsing configuration")

    # Load the configuration from the file.
    config = json.load(fp)

    # This is where all the streams are going to live.
    streams = []

    # This is where all the labels are going to live.
    labels = []
    labels_str = []
    base_labels = [None] * len(config['pcaps'])

    # The base label starts from 1 and increments after that.
    current_label = 1
    pat = re.compile(".*-curl\.pcap$")

    for domain in config['pcaps']:
        print(" - {}".format(domain))
        base_labels[current_label - 1] = domain
        i = 0

        # Traverse the directory for all the pcaps.
        for file in os.listdir('./pcaps/{}'.format(domain)):
            if file.endswith(".pcap") and (pat.match(file) is None):
                if i > 20:
                    break

                # This is the pcap file we'll be reading at this point.
                file = os.path.join("./pcaps/{}".format(domain), file)

                # Read the pcap file and append it to the streams array.
                streams.append(read_pcap_file(file))

                # Add a label for the new file.
                labels.append(current_label)
                labels_str.append(domain)

                i += 1

        print "    {} pcap files".format(i)

        # Increment the label
        current_label += 1

    try:
        print("Loading the classifier...")

        # Try to read the classifier.
        classifier = joblib.load("./classifier-nb.dmp")
        i = 0

        for stream in streams:
            # Run the prediction.
            prediction = classifier.predict([stream])

            # Print the results.
            print("[{}] Prediction: {} - Real: {}".format(i, base_labels[prediction[0] - 1], labels_str[i]))

            i += 1

    except:
        # Finally train the classifier.
        train(streams, labels)
