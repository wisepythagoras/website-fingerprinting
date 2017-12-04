# http://cv-tricks.com/tensorflow-tutorial/training-convolutional-neural-network-for-image-classification/

from __future__ import print_function

import random
import json
import dpkt
import re
import os
import tensorflow as tf

# Parameters
learning_rate = 0.1
num_steps = 40
batch_size = 21
display_step = 100

# Network Parameters
n_hidden_1 = 40 # 1st layer number of neurons
n_hidden_2 = 40 # 2nd layer number of neurons
num_input = 30
num_classes = 7

# tf Graph input
X = tf.placeholder("float", [None, num_input])
Y = tf.placeholder("float", [None, num_classes])

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([num_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, num_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([num_classes]))
}


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
    sizes = [0] * num_input
    i = 0

    # Loop through all the packets and save the sizes.
    for ts, buf in pcap:
        if i >= num_input:
            break

        sizes[i] = len(buf)

        i += 1

    # Finally return the sizes.
    return sizes


def neural_net(x):
    """ Create the neural network model. """

    # Hidden fully connected layer with 256 neurons
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])

    # Hidden fully connected layer with 256 neurons
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])

    # Output fully connected layer with a neuron for each class
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']

    return out_layer


def next_batch(streams, labels, batch_size):
    """ Get the next batch of each part. """

    # Get the batches.
    batch_x, batch_y = streams[:batch_size], labels[:batch_size]

    # Trim the original data.
    streams, labels = streams[batch_size:], labels[batch_size:]

    # Return the batches.
    return batch_x, batch_y, streams, labels


def train(streams, labels):
    """ This function trains the classifier with the data. """

    # Shuffle the arrays.
    streams, labels = shuffle(streams, labels)

    stream_amount = len(streams)
    training_size = int(stream_amount * 0.9)

    # Get 70% of the streams for training purposes.
    training_x, training_y = streams[:training_size], labels[:training_size]

    # Get 30% of the streams for testing purposes
    testing_x, testing_y = streams[training_size:], labels[training_size:]

    streams, labels = training_x, training_y

    print("Training size: {}".format(training_size))
    print("Testing size:  {}".format(stream_amount - training_size))

    # Construct a new model.
    logits = neural_net(X)

    # Define loss and optimizer.
    loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        logits=logits, labels=Y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
    train_op = optimizer.minimize(loss_op)

    # Evaluate the newly created model.
    correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # Initialize the variables.
    init = tf.global_variables_initializer()

    # Start the training.
    with tf.Session() as sess:
        # Run the initializer.
        sess.run(init)

        for step in range(1, num_steps + 1):
            # Get the next batch.
            batch_x, batch_y, streams, labels = next_batch(streams, labels, batch_size)

            print(len(batch_x))
            print(len(batch_y))

            # Run optimization op (backprop)
            sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})

            if step % display_step == 0 or step == 1:
                # Calculate batch loss and accuracy
                loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x,
                                                                     Y: batch_y})
                print("Step " + str(step) + ", Minibatch Loss= " + \
                      "{:.4f}".format(loss) + ", Training Accuracy= " + \
                      "{:.3f}".format(acc))

        print("Optimization Finished!")

        # Calculate accuracy for MNIST test images
        print("Testing Accuracy:", \
              sess.run(accuracy, feed_dict={X: testing_x,
                                            Y: testing_y}))

        # tf.train.import_meta_graph('mnist.meta')
        saver = tf.train.Saver()
        saver.save(sess, './abcde.data')


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

        print("    {} pcap files".format(i))
        num_classes += 1

        # Increment the label
        current_label += 1

    # Finally train the classifier.
    train(streams, labels)
