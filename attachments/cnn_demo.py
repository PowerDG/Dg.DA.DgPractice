import tensorflow as tf
import numpy as np
import cv2 as cv
import operator
import os

from tensorflow.examples.tutorials.mnist import input_data
print(tf.__version__)
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder(shape=[None, 784], dtype=tf.float32)
y = tf.placeholder(shape=[None, 10], dtype=tf.float32)
x_image = tf.reshape(x, [-1, 28, 28, 1])

# convolution layer 1
conv1_w = tf.Variable(tf.truncated_normal(shape=[5, 5, 1, 32], stddev=0.1, dtype=tf.float32))
conv1_bias = tf.Variable(tf.truncated_normal(shape=[32], stddev=0.1))
conv1_out = tf.nn.conv2d(input=x_image, filter=conv1_w, strides=[1, 1, 1, 1], padding='SAME')
conv1_relu = tf.nn.relu(tf.add(conv1_out, conv1_bias))

# max pooling 1
maxpooling_1 = tf.nn.max_pool(conv1_relu, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# convolution layer 2
conv2_w = tf.Variable(tf.truncated_normal(shape=[5, 5, 32, 64], stddev=0.1, dtype=tf.float32))
conv2_bias = tf.Variable(tf.truncated_normal(shape=[64], stddev=0.1))
conv2_out = tf.nn.conv2d(input=maxpooling_1, filter=conv2_w, strides=[1, 1, 1, 1], padding='SAME')
conv2_relu = tf.nn.relu(tf.add(conv2_out, conv2_bias))

# max pooling 2
maxpooling_2 = tf.nn.max_pool(conv2_relu, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# fc-1
w_fc1 = tf.Variable(tf.truncated_normal(shape=[7*7*64, 1024], stddev=0.1, dtype=tf.float32))
b_fc1 = tf.Variable(tf.constant(0.1, shape=[1024]))
h_pool2 = tf.reshape(maxpooling_2, [-1, 7*7*64])
output_fc1 = tf.nn.relu(tf.add(tf.matmul(h_pool2, w_fc1), b_fc1))

# dropout
keep_prob = tf.placeholder(dtype=tf.float32)
h2 = tf.nn.dropout(output_fc1, keep_prob=keep_prob)

# fc-2
w_fc2 = tf.Variable(tf.truncated_normal(shape=[1024, 10], stddev=0.1, dtype=tf.float32))
b_fc2 = tf.Variable(tf.constant(0.1, shape=[10]))
y_conv = tf.add(tf.matmul(output_fc1, w_fc2), b_fc2)

cross_loss = tf.nn.softmax_cross_entropy_with_logits(logits=y_conv, labels=y)
loss = tf.reduce_mean(cross_loss)
step = tf.train.GradientDescentOptimizer(0.05).minimize(loss)

# accuracy
acc_mat = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1))
acc = tf.reduce_sum(tf.cast(acc_mat, tf.float32))

saver = tf.train.Saver()
prediction = tf.argmax(y_conv, 1)


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(10000):
        batch_xs, batch_ys = mnist.train.next_batch(50)
        sess.run(step, feed_dict={x: batch_xs, y: batch_ys, keep_prob: 0.5})
        if (i + 1) % 100 == 0:
            curr_acc = sess.run(acc, feed_dict={x: mnist.test.images[:1000], y: mnist.test.labels[:1000], keep_prob: 1.0})
            print("current test Accuracy : %f" % (curr_acc))
    saver.save(sess, "./tf_mnist.model", global_step=10000)

"""
def write_digit_image():
    for i in range(100):
        im = mnist.test.images[i:(i+1)]
        label = mnist.test.labels[i:(i+1)]
        index = np.argmax(label, 1)[0]
        im = np.reshape(im, [28, 28])
        cv.normalize(im, im, 0, 255, cv.NORM_MINMAX)
        cv.imwrite("D:/gloomyfish/ocrtext/" + str(index) + "_" + str(i) + ".png", np.uint8(im))


with tf.Session() as sess:
    write_digit_image()
    saver.restore(sess, tf.train.latest_checkpoint('.'))
    path = "D:/gloomyfish/ocrtext/"
    files = os.listdir(path)
    count = 0
    for f in files:
        if os.path.isfile(os.path.join(path, f)):
            size = len(f)
            ext_name = f[size-3 : size]
            if operator.eq(ext_name, 'png'):
                input_data = cv.imread(os.path.join(path, f), cv.IMREAD_GRAYSCALE)
                input_x = np.reshape(input_data, [1, 784]) / 255.0
                digit = sess.run(prediction, feed_dict={x: input_x, keep_prob: 1.0})
                print("predict digit : %d., actual digit : %s"%(digit[0], f[0:1]))
                if str(digit[0]) == f[0:1]:
                    count = count + 1
    print("correct precent: %f"%(count/100.0))
"""