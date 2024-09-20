import numpy as np


def sigmoid(x):
    """
    Calculate the sigmoid function of x
    :param x: a vector
    :return: sigmoid value of x
    """
    return 1 / (1 + np.exp(-x))


def relu(x):
    """
    Calculate the ReLU function of x
    :param x: a vector
    :return: ReLU value of x
    """
    return x * (x > 0)


class Brain:
    def __init__(self):
        # Initialize the weights and biases for layer 1
        self.W1 = np.random.normal(loc=0, scale=0.1, size=(5, 2))
        self.b1 = np.random.normal(loc=0, scale=0.1, size=(2,))

        # Initialize the weights and biases for layer 2
        self.W2 = np.random.normal(loc=0, scale=0.1, size=(2, 1))
        self.b2 = np.random.normal(loc=0, scale=0.1, size=(1,))

    def perform_action(self, vision):
        """
        Perform action based on the vision of the bird
        :param vision: numpy array of bird vision
        :return: True if the bird should flap, false otherwise
        """
        # Perform backpropagation
        output = sigmoid(np.dot(vision, self.W1) + self.b1)
        output = sigmoid(np.dot(output, self.W2) + self.b2)
        return output[0] >= 0.5

    def receive_genes(self, W1, b1, W2, b2):
        """
        Receive the gene from parents
        :param W1: gene W1
        :param b1: gene b1
        :param W2: gene W2
        :param b2: gene b2
        :return: None
        """
        self.W1 = W1
        self.b1 = b1
        self.W2 = W2
        self.b2 = b2
