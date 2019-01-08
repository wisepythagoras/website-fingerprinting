#!/usr/bin/env python

import os.path
import sys
import json
import utils
from sklearn.externals import joblib


if len(sys.argv) == 1:
    print("A pcap file is needed")
    sys.exit(1)

elif os.path.exists('config.json') == False:
    print("No configuration found")
    sys.exit(1)

elif os.path.exists('./classifier-nb.dmp') == False:
    print("No classifier dump found; train first")
    sys.exit(1)

elif os.path.exists(sys.argv[1]) == False:
    print("The input file was not found")
    sys.exit(1)

# Read the configuration and start training.
with open('config.json') as fp:
    print("* Parsing configuration")

    # Load the configuration from the file.
    config = json.load(fp)

    # This is where all the labels are going to live.
    base_labels = [None] * len(config['pcaps'])

    # The base label starts from 1 and increments after that.
    current_label = 1

    for domain in config['pcaps']:
        # Set the base label.
        base_labels[current_label - 1] = domain

        # Increment the label
        current_label += 1

print("Loading the classifier...")

# Try to read the classifier.
classifier = joblib.load("./classifier-nb.dmp")
i = 0
right = 0
wrong = 0

# Read the pcap file.
stream = utils.read_pcap_file(sys.argv[1])

# Run the prediction.
prediction = classifier.predict([stream])

print(classifier.predict_proba([stream]))

# Print the results.
print(f"[{prediction[0]}] Prediction: {base_labels[prediction[0] - 1]}")
