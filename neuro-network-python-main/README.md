## Neural Network Training Algorithm (Backpropagation)

### Wikipedia link: Wikipedia link: [Backpropagation](https://en.wikipedia.org/wiki/Backpropagation)

#### Key Points:

Forward Pass
Input data passes sequentially through all layers of the network.
Each neuron computes a weighted sum of its inputs and applies an activation function (tanh, sigmoid, relu, etc.).
The output of the last layer is the network’s prediction.

### Backward Pass

The error at the output is calculated:
$\text{error} = \text{expected} - \text{predicted}$

The error is propagated backward through the layers to adjust the weights.
For each neuron, the delta is computed as:
$\delta = \text{error} \dot f'(out)$
where $\text{f′}$ is the derivative of the neuron’s activation function.

#### Weight Update

* Each weight is updated using:
  $w_{\text{new}} = w_{\text{old}} + \eta \cdot \delta \cdot \text{input}$

where $\eta$ is the learning rate and is the neuron’s input.

* Bias is updated similarly:
  $b_{\text{new}} = b_{\text{old}} + \eta \cdot \delta$

### Activation Functions
Common activation functions include:
- Sigmoid: $f(x) = \frac{1}{1 + e^{-x}}$
- Tanh: $f(x) = \tanh(x)$
- ReLU: $f(x) = \max(0, x)$
- linear: $f(x) = x$

### Derivative of Activation Functions
- Sigmoid: $f'(x) = f(x) \cdot (1 - f(x))$
- Tanh: $f'(x) = 1 - f(x)^2$
- ReLU: $f'(x) = 1$ if $x > 0$ else $0$
- linear: $f'(x) = 1$

Universality
The algorithm works for any number of layers.
Each neuron knows its activation function and derivative, making the training code fully general.