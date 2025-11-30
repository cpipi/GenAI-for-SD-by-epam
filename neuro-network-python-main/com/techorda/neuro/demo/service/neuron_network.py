from typing import List

class NeuronNetwork:

    def __init__(self):
        self.layers: List = []  # layers = new ArrayList<>();

        """
        Implement this constructor
        to create a neural network with a specified architecture.
        Your network should train during initialization
        """
        # Add layers here. For example:
        # self.layers.append(NeuronLayer(3, 16, NeuronType.TANH))
        # self.layers.append(NeuronLayer(16, 16, NeuronType.TANH))
        for layer in self.layers:
            self.initialize_weights(layer)

    # implement this method
    def initialize_weights(self, layer):
        pass

    def predict(self, inputs: List[float]) -> List[float]:
        output = inputs
        for layer in self.layers:
            output = layer.activate(output)
        return output

    def train(self):
        # add logic for training in constructor
        # AS EXAMPLE:
        # training_inputs = ..
        # training_outputs = ..
        # self.train(training_inputs, training_outputs, 20000, 0.01)
        pass

    """ implement this method
    to train the neural network using backpropagation
    for the given number of epochs and learning rate.
    Use Mean Squared Error (MSE) as the loss function.
    Log the total error every 1000 epochs.
    trainingInputs - input data for training
    trainingOutputs - expected output data for training
    epochs - number of training iterations
    learningRate - step size for weight updates
    Hint: You will need to implement forward propagation,
    error calculation, backpropagation, and weight updates.
    """
    def train(self, training_inputs, training_outputs, epochs, learning_rate):
        pass
