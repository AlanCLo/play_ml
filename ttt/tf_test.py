
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(
    x_train, axis=1).reshape(x_train.shape[0], -1)
x_test = tf.keras.utils.normalize(
    x_test, axis=1).reshape(x_test.shape[0], -1)


def createModel():
    plt.imshow(x_train[0], cmap=plt.cm.binary)
    plt.show()
    plt.imshow(x_train[1], cmap=plt.cm.binary)
    plt.show()
    plt.imshow(x_train[2], cmap=plt.cm.binary)
    plt.show()
    plt.imshow(x_test[0], cmap=plt.cm.binary)
    plt.show()

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(
        128, activation=tf.nn.relu, input_shape=x_train.shape[1:]))
    model.add(
        tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(
        tf.keras.layers.Dense(10, activation=tf.nn.softmax))
    # 10 because dataset is numbers from 0 - 9

    model.compile(optimizer='adam',  # Good default optimizer to start with
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])  # what to track

    model.fit(x_train, y_train, epochs=3)  # train the model

    val_loss, val_acc = model.evaluate(x_test, y_test)
    print(val_loss)  # model's loss (error)
    print(val_acc)  # model's accuracy

    model.save('epic_num_reader.model')


model = tf.keras.models.load_model('epic_num_reader.model')

predictions = model.predict(x_test)
print(predictions)
print(np.argmax(predictions[0]))
print(np.argmax(predictions[1]))
