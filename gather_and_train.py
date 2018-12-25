#!/usr/bin/env python

import os
import re
import sys
import json
import utils
from sklearn.externals import joblib


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
        # Set the base label.
        base_labels[current_label - 1] = domain

        # Increment the label
        current_label += 1

    utils.empty_csv()
    current_label = 1

    for domain in config['pcaps']:
        print(" - {}".format(domain))
        i = 0

        # Traverse the directory for all the pcaps.
        for file in os.listdir('./pcaps/{}'.format(domain)):
            if file.endswith(".pcap") and (pat.match(file) is None):
                # if i > 20:
                #     break

                # This is the pcap file we'll be reading at this point.
                file = os.path.join("./pcaps/{}".format(domain), file)

                # Read the pcap file.
                data = utils.read_pcap_file(file)

                # Append the data to the streams array.
                streams.append(data)

                # Append everything to the log.
                utils.append_to_csv(domain, data)

                # Add a label for the new file.
                labels.append(current_label)
                labels_str.append(domain)

                i += 1

        print("    {} pcap files".format(i))

        # Increment the label
        current_label += 1

    # Finally train the classifier.
    utils.train(streams, labels)
