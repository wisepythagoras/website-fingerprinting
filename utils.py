import dpkt
import socket
import random
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib


def empty_csv():
    """ Empties the CSV file. """

    with open("./fingerprints.csv", 'w') as f:
        f.write("")


def append_to_csv(domain, data):
    """ Append the information to the log file. """

    with open("./fingerprints.csv", 'a') as f:
        f.write("{},{}\n".format(domain, ','.join(str(num) for num in data)))


def inet_to_str(inet):
    """ Convert inet object to a string """

    return socket.inet_ntop(socket.AF_INET, inet)


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
    sizes = [0] * 40
    i = 0

    # Hold the addresses of the outgoing agent.
    outgoing_addr = None

    outgoing_packets = 0
    incoming_packets = 0
    total_number_of_packets = 0

    # This will contain the total size of the incoming packets.
    incoming_size = 0

    # Loop through all the packets and save the sizes.
    for ts, buf in pcap:
        packet_size = len(buf)
        is_outgoing = True

        # Parse the Ethernet packet.
        eth = dpkt.ethernet.Ethernet(buf)

        # Parse the IP packet.
        ip = eth.data

        # Get the source addresses.
        src = inet_to_str(ip.src)

        if total_number_of_packets == 0:
            # Get the address of the outgoing agents. The target user is the
            # outgoing agent, and the incoming packets are the server/website.
            outgoing_addr = src
            outgoing_packets += 1

        elif src == outgoing_addr:
            # Increment the outgoing packets.
            outgoing_packets += 1

        else:
            # Increment the incoming packets.
            incoming_packets += 1

            # Increment the size of the incoming packets.
            incoming_size += packet_size

            # This is an incoming packet.
            is_outgoing = False

        if i < 40:
            # Add the size to the array.
            sizes[i] = packet_size if is_outgoing else -packet_size

            # Increment the index.
            i += 1

        # Increment the total amount of packets.
        total_number_of_packets += 1

    # Get the ratio.
    ratio = float(incoming_packets) / (outgoing_packets if outgoing_packets != 0 else 1)

    # Print some details.
    print "OUT: {}, IN: {}, TOTAL: {}, SIZE: {}, RATIO: {}".format(\
        outgoing_packets, incoming_packets, total_number_of_packets, incoming_size, ratio)

    # Reverse the array to append the other information.
    sizes.reverse()

    # Add the ratio of incoming to outgoing packets.
    sizes.append(ratio)

    # Add the number of incoming packets.
    sizes.append(incoming_packets)

    # Add the number of outgoing packets.
    sizes.append(outgoing_packets)

    # Add the number of total packets.
    sizes.append(total_number_of_packets)

    # Add the total size of the incoming packets.
    sizes.append(incoming_size)

    # Reverse the array again so that the sizes are in order.
    sizes.reverse()

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
    clf = KNeighborsClassifier()

    # Now lets train our KNN classifier.
    clf = clf.fit(training_x, training_y)

    # Save a snapshot of this classifier.
    joblib.dump(clf, "./classifier-nb.dmp", compress=9)

    # Get the prediction.
    predictions = clf.predict(testing_x)

    print("Accuracy: %s%%" % (accuracy_score(testing_y, predictions) * 100,))
