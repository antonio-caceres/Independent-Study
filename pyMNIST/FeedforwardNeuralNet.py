import numpy as np


class NeuralNet:
    weight_matrices = []
    bias_matrices = []
    learning_rate = 0

    def __init__(self, neuron_layers, learning_rate = .1):
        """
        Generate a neural network with a specified number of layers and neurons.
        :param neuron_layers: list of integers representing the number of neurons in each layer.
        :param learning_rate: learning rate of the neural network
        """
        self.weight_matrices = []
        self.bias_matrices = []
        learning_rate = -np.abs(learning_rate)
        for i in range(len(neuron_layers) - 1):
            weight_matrix = []
            for r in range(neuron_layers[i + 1]):
                weight_matrix.append(np.random.uniform(-1, 1, neuron_layers[i]))
            self.weight_matrices.append(np.array(weight_matrix))
            bias_matrix = []
            for r in range(neuron_layers[i + 1]):
                bias_matrix.append(np.random.uniform(-1, 1, 1))
            self.bias_matrices.append(np.array(bias_matrix))
        self.learning_rate = learning_rate

    def process_input(self, input_list):
        """
        Process one input using the current weights of the neural network.
        :param input_list: numpy column np array of inputs to be fed to the input layer
        :return: np array of the output layer with given input
        """
        output = input_list
        output_values = [input_list]
        for i in range(len(self.weight_matrices)):
            output = NeuralNet.sigmoid(np.matmul(self.weight_matrices[i], output) + self.bias_matrices[i])
            output_values.append(output)
        return output_values

    def stochastic_training_input(self, input_outputs, num_epochs, mini_batch_size):
        """
        Run several iterations of the training process, backpropagating at the end
        :param input_outputs: a list of tuples of input arrays and their expected output arrays
        :param num_epochs: the number of times to train batches
        :param mini_batch_size: the size of batches to use.
        :return: None
        """
        if mini_batch_size > len(input_outputs):
            mini_batch_size = len(input_outputs)
        for num in range(num_epochs):
            np.random.shuffle(input_outputs)
            io_batch = [input_outputs[i] for i in range(mini_batch_size)]
            weight_deltas = []
            for x in self.weight_matrices:
                weight_deltas.append(np.zeros(x.shape))
            bias_deltas = []
            for x in self.bias_matrices:
                bias_deltas.append(np.zeros(x.shape))
            for i, o in io_batch:
                layer_outputs = self.process_input(i)  # an array of matrices, same size as weight_matrices
                layer_error = np.multiply((layer_outputs[-1] - o), self.der_sigmoid(layer_outputs[-1]))  # Hadamard
                weight_deltas[-1] += np.matmul(layer_error, np.transpose(layer_outputs[-2]))  # from column -> row
                bias_deltas[-1] += layer_error
                for n in range(len(self.weight_matrices)-1):  # BACKPROPAGATION
                    # Each layer_output corresponds to a layer from the input to the output.
                    # Each weight_matrix corresponds to a layer from (input + 1) to the output.
                    # Each weight_ and bias_delta should corresponds to a layer from (input+1) to the output.
                    # We've already taken care of the output layer above.
                    a = np.dot(np.transpose(self.weight_matrices[-n-1]), layer_error)  # temporary value
                    b = self.der_sigmoid(layer_outputs[-n-2])  # temporary value
                    layer_error = np.multiply(a, b)
                    weight_deltas[-n - 2] += np.matmul(layer_error, np.transpose(layer_outputs[-n - 3]))
                    bias_deltas[-n - 2] += layer_error
            for i in range(len(self.weight_matrices)):
                weight_deltas[i] *= self.learning_rate / mini_batch_size
                self.weight_matrices[i] += weight_deltas[i]
                bias_deltas[i] *= self.learning_rate / mini_batch_size
                self.bias_matrices[i] += bias_deltas[i]

    @staticmethod
    def quad_cost_func(actual, expected):
        """
        Computation of the quadratic cost function for one input/output of the neural net.
        :param actual: np array of actual output values
        :param expected: np array of expected output values
        :return: a scalar value for the difference between the actual and expected values.
        """
        delta_matrix = np.abs(expected - actual)
        vec_length = np.dot(delta_matrix, delta_matrix)
        return 0.5 * vec_length  # I don't know why it's divided by 2; I'm copying the cost function from the book.

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def der_sigmoid(sig_x):  # derivative of output with respect to sum of weights/inputs/biases
        """
        Compute the derivative of sigmoid(x) at x with the value of sigmoid(x).
        :param sig_x: takes the result of NeuralNet.sigmoid(x) to compute the derivative of sigmoid(x) at x.
        :return: the derivative of the sigmoid function at the x-value of x given the value of sigmoid(x).
        """
        return sig_x * (1 - sig_x)