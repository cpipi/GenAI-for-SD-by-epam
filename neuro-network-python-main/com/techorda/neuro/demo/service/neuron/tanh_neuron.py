import math
from neuron.neuron import Neuron


class TanhNeuron(Neuron):
    def __init__(self, input_count: int) -> None:
        super().__init__(input_count)

    def activation_function(self, x: float) -> float:
        return math.tanh(x)

    def derivative(self, x: float) -> float:
        """
        Derivative of tanh activation function.
        d/dx tanh(x) = 1 - tanh(x)^2
        Since x is the output (already passed through tanh),
        we compute: 1 - x^2
        """
        return 1.0 - x * x
