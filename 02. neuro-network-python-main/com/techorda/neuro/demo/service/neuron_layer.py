# python
from typing import Sequence, List
from neuron.neuron import Neuron

class NeuronLayer:
    def __init__(self, neurons: Sequence[Neuron]) -> None:
        if not neurons:
            raise ValueError("neurons must be a non-empty sequence")
        self.neurons: List[Neuron] = list(neurons)

    def activate(self, inputs: Sequence[float]) -> List[float]:
        """
        Activate all neurons in the layer with the given inputs and
        return their outputs as a list of floats.
        """
        return [neuron.activate(inputs) for neuron in self.neurons]

    def size(self) -> int:
        return len(self.neurons)
