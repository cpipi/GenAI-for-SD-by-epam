from neuron.neuron import Neuron

class LinearNeuron(Neuron):
    def __init__(self, input_count: int) -> None:
        super().__init__(input_count)

    def activation_function(self, x: float) -> float:
        return x

    def derivative(self, x: float) -> float:
        return 1.0
