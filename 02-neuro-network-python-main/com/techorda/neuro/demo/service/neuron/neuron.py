# python
from abc import ABC, abstractmethod
from typing import List, Sequence
import random

class Neuron(ABC):
    def __init__(self, input_count: int) -> None:
        if input_count < 1:
            raise ValueError("input_count must be >= 1")
        self.weights: List[float] = [random.random() - 0.5 for _ in range(input_count)]
        self.bias: float = random.random() - 0.5

    def activate(self, inputs: Sequence[float]) -> float:
        if len(inputs) != len(self.weights):
            raise ValueError("Input length does not match weights length.")
        total = self.bias + sum(i * w for i, w in zip(inputs, self.weights))
        return self.activation_function(total)

    @abstractmethod
    def activation_function(self, x: float) -> float:
        raise NotImplementedError

    @abstractmethod
    def derivative(self, x: float) -> float:
        raise NotImplementedError
