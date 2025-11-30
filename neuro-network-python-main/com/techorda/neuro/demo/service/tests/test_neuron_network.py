# python
import math
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from neuron_network import NeuronNetwork

def test_predict_returns_finite_output():
    network = NeuronNetwork()
    input_vec = [0.5, -0.2, 0.1]
    output = network.predict(input_vec)
    assert len(output) == 1
    assert math.isfinite(output[0])

def test_train_improves_prediction():
    network = NeuronNetwork()
    inputs = [
        [0.0, 0.0, 0.0],
        [1.0, 1.0, 1.0]
    ]
    outputs = [
        [0.0],
        [1.0]
    ]

    before = network.predict(inputs[1])
    network.train()
    after = network.predict(inputs[1])
    assert abs(after[0] - 1.0) < abs(before[0] - 1.0)
