from typing import List
import random
import math
from neuron_layer import NeuronLayer
from neuron.tanh_neuron import TanhNeuron
from neuron.linear_neuron import LinearNeuron


class NeuronNetwork:
    """
    Neural network that learns to find the maximum of three input values.
    
    Architecture:
    - Input layer: 3 neurons (x1, x2, x3)
    - Hidden layer: 6 tanh neurons for feature learning
    - Output layer: 1 linear neuron (outputs the predicted maximum)
    
    The network is trained during initialization to learn the max function.
    """

    def __init__(self, hidden_neurons=6, epochs=2000, learning_rate=0.3, 
                 training_samples=2000, validation_split=0.2):
        """
        Initialize the neural network for finding maximum of three numbers.
        
        Args:
            hidden_neurons: Number of neurons in hidden layer (default 6)
            epochs: Number of training epochs (default 2000)
            learning_rate: Learning rate for gradient descent (default 0.3)
            training_samples: Number of training samples to generate (default 2000)
            validation_split: Fraction of data to use for validation (default 0.2)
        """
        self.layers: List = []
        self.hidden_neurons = hidden_neurons
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.training_samples = training_samples
        self.validation_split = validation_split
        
        # Momentum for each weight to smooth training
        self.momentum_weights = []
        self.momentum_biases = []

        # Create network architecture
        # Input: 3 numbers  
        # Hidden: configurable tanh neurons for feature learning
        # Output: 1 linear neuron for the maximum value
        self.layers.append(NeuronLayer([TanhNeuron(3) for _ in range(hidden_neurons)]))
        self.layers.append(NeuronLayer([LinearNeuron(hidden_neurons)]))

        for layer_idx, layer in enumerate(self.layers):
            self.initialize_weights(layer, layer_idx)
            # Initialize momentum buffers
            layer_momentum_w = []
            layer_momentum_b = []
            for neuron in layer.neurons:
                layer_momentum_w.append([0.0 for _ in neuron.weights])
                layer_momentum_b.append(0.0)
            self.momentum_weights.append(layer_momentum_w)
            self.momentum_biases.append(layer_momentum_b)

        # Generate training data and train the network
        training_inputs, training_outputs = self._generate_training_data(training_samples)
        self._train_with_data(training_inputs, training_outputs, epochs, learning_rate)

    def initialize_weights(self, layer, layer_idx):
        """
        Initialize weights using He initialization for better convergence.
        He initialization: w ~ N(0, 2/n_in) for tanh activations
        
        Args:
            layer: The layer to initialize
            layer_idx: Index of the layer in the network
        """
        # Determine number of inputs to this layer
        if layer_idx == 0:
            fan_in = 3  # Input layer has 3 inputs
        else:
            fan_in = self.hidden_neurons
        
        # He initialization for tanh: scale factor is 2/fan_in under sqrt
        scale_factor = math.sqrt(2.0 / fan_in) if fan_in > 0 else 1.0
        
        for neuron in layer.neurons:
            # Reinitialize weights with He initialization
            for i in range(len(neuron.weights)):
                neuron.weights[i] = random.gauss(0, scale_factor)
            # Initialize bias to 0
            neuron.bias = 0.0

    def predict(self, inputs: List[float]) -> List[float]:
        """
        Predict the maximum of three input values.
        
        Args:
            inputs: List of three floats [x1, x2, x3] in range [-1, 1]
        
        Returns:
            List with one element [predicted_maximum]
        """
        output = inputs
        for layer in self.layers:
            output = layer.activate(output)
        return output

    def _generate_training_data(self, num_samples: int):
        """
        Generate training data for the max function.
        
        Args:
            num_samples: Number of training examples
            
        Returns:
            (training_inputs, training_outputs): Lists of inputs and expected outputs
        """
        training_inputs = []
        training_outputs = []

        for _ in range(num_samples):
            # Generate three random numbers in [-0.9, 0.9] (slightly narrower range)
            # to avoid extreme values that might saturate tanh
            x1 = random.uniform(-0.9, 0.9)
            x2 = random.uniform(-0.9, 0.9)
            x3 = random.uniform(-0.9, 0.9)

            # Compute the maximum
            max_value = max(x1, x2, x3)

            training_inputs.append([x1, x2, x3])
            training_outputs.append([max_value])

        return training_inputs, training_outputs

    def train(self, training_inputs=None, training_outputs=None, epochs=None, learning_rate=None):
        """
        Overloaded train method that can be called with or without parameters.
        - train(): Generates new training data and fine-tunes the network with very low learning rate
        - train(training_inputs, training_outputs, epochs, learning_rate): Trains with provided data
        """
        if training_inputs is None:
            # Parameterless call - generate new training data
            training_inputs, training_outputs = self._generate_training_data(self.training_samples)
            epochs = self.epochs
            # Use extremely low learning rate for fine-tuning (10x lower than initial)
            learning_rate = self.learning_rate * 0.1

        self._train_with_data(training_inputs, training_outputs, epochs, learning_rate)

    def _train_with_data(self, training_inputs, training_outputs, epochs, learning_rate):
        """
        Internal training method using backpropagation with validation set.
        Splits data into training and validation sets.
        
        Args:
            training_inputs: List of input vectors
            training_outputs: List of output vectors
            epochs: Number of epochs to train
            learning_rate: Learning rate for gradient descent
        """
        # Split data into training and validation sets
        num_train = int(len(training_inputs) * (1 - self.validation_split))
        train_inputs = training_inputs[:num_train]
        train_outputs = training_outputs[:num_train]
        val_inputs = training_inputs[num_train:]
        val_outputs = training_outputs[num_train:]
        
        for epoch in range(epochs):
            total_error = 0.0

            # Forward pass and backward pass for each training sample
            for inputs, expected_output in zip(train_inputs, train_outputs):
                # Forward propagation - compute outputs and store activations
                layer_outputs = [inputs]
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

                # Update weights and biases with momentum and gradient clipping
                momentum_factor = 0.9  # Momentum coefficient
                
                for layer_idx, layer in enumerate(self.layers):
                    layer_input = layer_outputs[layer_idx]

                    for neuron_idx, neuron in enumerate(layer.neurons):
                        delta = deltas[layer_idx][neuron_idx]
                        
                        # Clip delta to prevent exploding gradients
                        clipped_delta = max(-1.0, min(1.0, delta))

                        # Update weights with momentum
                        for weight_idx in range(len(neuron.weights)):
                            weight_update = learning_rate * clipped_delta * layer_input[weight_idx]
                            # Clip weight update to prevent large jumps
                            weight_update = max(-0.5, min(0.5, weight_update))
                            
                            # Apply momentum
                            self.momentum_weights[layer_idx][neuron_idx][weight_idx] = (
                                momentum_factor * self.momentum_weights[layer_idx][neuron_idx][weight_idx] + 
                                weight_update
                            )
                            neuron.weights[weight_idx] += self.momentum_weights[layer_idx][neuron_idx][weight_idx]

                        # Update bias with momentum
                        bias_update = learning_rate * clipped_delta
                        bias_update = max(-0.5, min(0.5, bias_update))
                        
                        # Apply momentum to bias
                        self.momentum_biases[layer_idx][neuron_idx] = (
                            momentum_factor * self.momentum_biases[layer_idx][neuron_idx] + 
                            bias_update
                        )
                        neuron.bias += self.momentum_biases[layer_idx][neuron_idx]

            # Calculate training MSE and log every 500 epochs
            if (epoch + 1) % 500 == 0:
                train_mse = total_error / len(train_inputs)
                
                # Calculate validation error if we have validation data
                val_error = 0.0
                if len(val_inputs) > 0:
                    for val_input, val_expected in zip(val_inputs, val_outputs):
                        val_output = val_input
                        for layer in self.layers:
                            val_output = layer.activate(val_output)
                        error = val_expected[0] - val_output[0]
                        val_error += error * error
                    val_mse = val_error / len(val_inputs)
                    print(f"Epoch {epoch + 1}/{epochs}, Train MSE: {train_mse:.6f}, Val MSE: {val_mse:.6f}")
                else:
                    print(f"Epoch {epoch + 1}/{epochs}, MSE: {train_mse:.6f}")
