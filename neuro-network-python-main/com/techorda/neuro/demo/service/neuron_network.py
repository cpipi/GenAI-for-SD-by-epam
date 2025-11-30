from typing import List
import random
from neuron_layer import NeuronLayer
from neuron.tanh_neuron import TanhNeuron
from neuron.linear_neuron import LinearNeuron


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
        
        # Create network architecture for circle classification
        # Input layer: 2 neurons (x, y coordinates)
        # Hidden layer: 4 tanh neurons
        # Output layer: 1 linear neuron (0 or 1)
        self.layers.append(NeuronLayer([TanhNeuron(2) for _ in range(4)]))
        self.layers.append(NeuronLayer([LinearNeuron(4)]))
        
        for layer in self.layers:
            self.initialize_weights(layer)
        
        # Generate training data and train the network
        training_inputs, training_outputs = self._generate_training_data(1000)
        self._train_with_data(training_inputs, training_outputs, epochs=2000, learning_rate=0.15)

    # implement this method
    def initialize_weights(self, layer):
        # Weights are already initialized in Neuron.__init__
        # This method is a placeholder for any additional initialization
        pass

    def predict(self, inputs: List[float]) -> List[float]:
        output = inputs
        for layer in self.layers:
            output = layer.activate(output)
        return output

    def _generate_training_data(self, num_samples: int):
        """
        Generate training data for circle classification.
        A point (x, y) is inside the circle if x^2 + y^2 <= 25 (radius = 5)
        Returns: (training_inputs, training_outputs)
        """
        training_inputs = []
        training_outputs = []
        
        for _ in range(num_samples):
            # Generate random coordinates in range [-8, 8]
            x = random.uniform(-8, 8)
            y = random.uniform(-8, 8)
            
            # Check if point is inside circle (radius 5)
            distance_squared = x * x + y * y
            is_inside = 1.0 if distance_squared <= 25.0 else 0.0
            
            training_inputs.append([x, y])
            training_outputs.append([is_inside])
        
        return training_inputs, training_outputs

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
    def train(self, training_inputs=None, training_outputs=None, epochs=None, learning_rate=None):
        """
        Overloaded train method that can be called with or without parameters.
        - train(): Generates new training data and trains the network
        - train(training_inputs, training_outputs, epochs, learning_rate): Trains with provided data
        """
        if training_inputs is None:
            # Parameterless call - generate new training data with larger dataset
            training_inputs, training_outputs = self._generate_training_data(1000)
            epochs = 2000
            learning_rate = 0.15
        
        self._train_with_data(training_inputs, training_outputs, epochs, learning_rate)
    
    def _train_with_data(self, training_inputs, training_outputs, epochs, learning_rate):
        """
        Internal training method using backpropagation.
        Implements forward propagation, error calculation, backpropagation, and weight updates.
        Uses Mean Squared Error (MSE) as the loss function.
        Logs the total error every 1000 epochs.
        """
        for epoch in range(epochs):
            total_error = 0.0
            
            # Forward pass and backward pass for each training sample
            for inputs, expected_output in zip(training_inputs, training_outputs):
                # Forward propagation - compute outputs and store activations
                layer_outputs = [inputs]  # Store input as first layer output
                current_input = inputs
                
                for layer in self.layers:
                    current_output = layer.activate(current_input)
                    layer_outputs.append(current_output)
                    current_input = current_output
                
                # Get final prediction
                final_output = layer_outputs[-1]
                
                # Calculate error for this sample
                error = expected_output[0] - final_output[0]
                total_error += error * error
                
                # Backpropagation
                deltas = [[] for _ in self.layers]
                
                # Output layer delta
                output_neuron = self.layers[-1].neurons[0]
                output_activation = layer_outputs[-1][0]
                delta_output = error * output_neuron.derivative(output_activation)
                deltas[-1].append(delta_output)
                
                # Hidden layers deltas (backpropagation)
                for layer_idx in range(len(self.layers) - 2, -1, -1):
                    layer = self.layers[layer_idx]
                    next_layer = self.layers[layer_idx + 1]
                    
                    layer_deltas = []
                    for neuron_idx, neuron in enumerate(layer.neurons):
                        # Calculate weighted sum of deltas from next layer
                        weighted_delta_sum = 0.0
                        for next_neuron_idx, next_neuron in enumerate(next_layer.neurons):
                            weighted_delta_sum += deltas[layer_idx + 1][next_neuron_idx] * next_neuron.weights[neuron_idx]
                        
                        # Multiply by derivative of activation function
                        neuron_output = layer_outputs[layer_idx + 1][neuron_idx]
                        delta = weighted_delta_sum * neuron.derivative(neuron_output)
                        layer_deltas.append(delta)
                    
                    deltas[layer_idx] = layer_deltas
                
                # Update weights and biases
                for layer_idx, layer in enumerate(self.layers):
                    layer_input = layer_outputs[layer_idx]
                    
                    for neuron_idx, neuron in enumerate(layer.neurons):
                        delta = deltas[layer_idx][neuron_idx]
                        
                        # Update weights
                        for weight_idx in range(len(neuron.weights)):
                            neuron.weights[weight_idx] += learning_rate * delta * layer_input[weight_idx]
                        
                        # Update bias
                        neuron.bias += learning_rate * delta
            
            # Log error every 500 epochs
            if (epoch + 1) % 500 == 0:
                mse = total_error / len(training_inputs)
                print(f"Epoch {epoch + 1}/{epochs}, MSE: {mse:.6f}")
