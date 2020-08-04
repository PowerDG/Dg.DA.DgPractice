import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
print(tf.__version__)
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


def mlp_drop_out_demo():
    hidden_nodes = 50
    x = tf.placeholder(shape=[None, 784], dtype=tf.float32)
    y = tf.placeholder(shape=[None, 10], dtype=tf.float32)
    keep_prob = tf.placeholder(dtype=tf.float32)

    W1 = tf.Variable(tf.truncated_normal(shape=[784, hidden_nodes]), dtype=tf.float32)
    b1 = tf.Variable(tf.truncated_normal(shape=[1, hidden_nodes]), dtype=tf.float32)

    W2 = tf.Variable(tf.truncated_normal(shape=[hidden_nodes, hidden_nodes]), dtype=tf.float32)
    b2 = tf.Variable(tf.truncated_normal(shape=[1, hidden_nodes]), dtype=tf.float32)

    W3 = tf.Variable(tf.truncated_normal(shape=[hidden_nodes, 10]), dtype=tf.float32)
    b3 = tf.Variable(tf.truncated_normal(shape=[1, 10]), dtype=tf.float32)

    # layer first hidden
    nn_1 = tf.add(tf.matmul(x, W1), b1)
    h1 = tf.nn.dropout(tf.nn.sigmoid(nn_1), keep_prob=keep_prob)

    # layer second hidden
    nn_2 = tf.add(tf.matmul(h1, W2), b2)
    h2 = tf.nn.dropout(tf.nn.sigmoid(nn_2), keep_prob=keep_prob)

    # output layer
    nn_3 = tf.add(tf.matmul(h2, W3), b3)
    out = tf.nn.sigmoid(nn_3)

    # loss function
    error = tf.square(tf.subtract(out, y))
    loss = tf.reduce_sum(error)

    # BP
    step = tf.train.GradientDescentOptimizer(0.05).minimize(loss)
    init = tf.global_variables_initializer()

    # accuracy
    acc_mat = tf.equal(tf.argmax(out, 1), tf.argmax(y, 1))
    acc = tf.reduce_sum(tf.cast(acc_mat, tf.float32))

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(20000):
            batch_xs, batch_ys = mnist.train.next_batch(128)
            sess.run(step, feed_dict={x: batch_xs, y: batch_ys, keep_prob: 0.75})
            if (i+1) % 1000 == 0:
                curr_acc = sess.run(acc, feed_dict={x: mnist.test.images[:1000],
                                                    y: mnist.test.labels[:1000], keep_prob: 1.0})
                print("current test Accuracy : %f" % (curr_acc))


if __name__ == "__main__":
    mlp_drop_out_demo()

