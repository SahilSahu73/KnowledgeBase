# torch.nn
All the contents of torch.nn that I should know about properly and links to other stuff.

The basic building blocks for graphs includes these containers and all the other modules and classes:
**The containers in torch.nn :**

1. *Module* -> the base class for all neural network modules
2. *Sequential* -> A Sequential container
3. *ModuleList* or *ModuleDict* -> Holds submodules in a list or dict
4. *ParametersList* or *ParametersDict* -> Holds Parameters in a List or Dictionary

----------------------------------------
Summary of the basic functionality that each module should provide when coding the network module:
i. Ingest input data as arguments to its forward propagation method.
ii. Generate an output by having the forward propagation method return a value. Output may have a different shape from the input.
iii. Calculate the gradients of its output w.r.t. its input, done through the backpropagation method automatically.
iv. Store and provide access to those parameters necessary for executing the forward propagation computation.
v. initialize model parameters as needed.


**There are many classes for different purposes in DL :**
Note: The below mentioned categories are not actual submodules present in the torch.nn module, these classes are just grouped for ease of
understanding and finding all the available classes at one place in documentation.

1. [*Convolution Layers*](https://docs.pytorch.org/docs/stable/nn.html#convolution-layers) -> This section contains all the classes for creating
convolutional layers, like nn.Conv1d, nn.Conv2d, nn.Conv3d, nn.ConvTranspose(x)d and so on.....
2. [*Pooling Layers*](https://docs.pytorch.org/docs/stable/nn.html#pooling-layers) -> Classes for creating pooling layers that performs max pooling
over an input signal composed of several input planes, like nn.MaxPool1d, nn.MaxPool2d, nn.Unpool1d, nn.Avgpool1d etc.
3. Padding Layers

4. [*Non-Linear Activations*](https://docs.pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity) -> List of Classes
of all non-linear activations.
    a. *nn.ELU* -> Exponential Linear Unit, applied element-wise
    ELU(x) = x,            if x>0
             α∗(exp(x)−1), if x<=0
    parameters: alpha(float) - default 1.0
    reason for using ELU - In contrast to ReLUs, ELUs have negative values which pushes the mean of the activations closer to zero. Mean 
    activations that are closer to zero enable faster learning as they bring the gradient closer to the natural gradient.

    b. *nn.ReLU*, *nn.PReLU*, *nn.LeakyReLU*, *nn.RReLU*, *nn.ReLU6* -> All of them are some version of ReLU (Rectified Linear Unit)
    *ReLU(x)* = max(0,x)
    *LeakyReLU(x)* = max(0,x) + negative_slope * min(0,x) -> parameters: negative_slope(float) - default=0.01 or 1e-2
    *ParametricReLU(x)* = max(0,x) + a * min(0,x) -> Parameters: num_parameters(int) - number of 'a' to learn. Although it takes an int as input there are only 2 values which are legitimate: 1, or the number of channels at input. Default: 1
    Here a is a learnable parameter. When called without arguments, nn.PReLU() uses a single parameter 'a' across all input channels. If called
    with nn.PReLU(nChannels), a seperate 'a' is used for each input channel.
    Also Weight decay should not be used when learning 'a' for good performance.
    *ReLU6(x)* = min(max(0,x),6) 
    In this we are basically restricting the value of positive side to 6, i.e. we don't want activations to exceed the value of 6. Not exactly sure why 6 but by restricting it to 6 lets the values to take a max of 3 bits (upto 8bits) which is an important aspect to look at while quantizing.
    *RReLU(x)* = x if x>=0    Parameters: lower bound-default 0.125, upper bound-default 0.3333333 
                 ax if x<0    here 'a' is randomly sampled from uniform distribution during training, while during evaluation 'a' is fixed with a = (lower bound + upper bound)/2 

    c. *nn.tanh*, *nn.HardTanh*, *nn.TanhShrink* -> tanh and it's variations.
    *tanh(x)* = exp(x) - exp(-x) / exp(x) + exp(-x)
    *HardTanh(x)* = -1, if x<-1          pytorch parameters min_value:default=-1, max_value:default=1
                     x, if -1 <= x <= 1
                     1, if x>1           It is a cheaper alternative and more computationally efficient version of tanh activation.
    *TanhShrink(x)* = x - tanh(x)

    d. *nn.HardSigmoid*, *nn.Sigmoid*, *nn.LogSigmoid*, *nn.SiLU*
    *Sigmoid(x)* = 1/(1+exp(-x))
    *HardSigmoid(x)* = max(0, min(1, (x+1)/2))  for training NN with weights and activations constrained to +1 or -1
    *LogSigmoid(x)* = log(1/(1+exp(-x)))  adding the log to this sigmoid function provides numerical stability when the numerical values are too low after the sigmoid(i.e. an attmept to solve the vanishing gradient problem)
    *SiLU(x)* = x * sigmoid(x)  Sigmoid Linear Unit, derived or first came from swish AF and this term was coined in GELU (Gaussian Error Linear Unit)
    It solves the problem of dying ReLU and it is not monotonically increasing, meaning its output is doesn't strictly increases or decreases as the input changes. SiLU has a "soft floor" effect - derivative is 0 around -1.28 which acts kinda like a regulizer, preventing weights from growing too large.
    Works well with batch normalization. better performance, especially in deep residual networks
    One downside is high computational complexity. 

    e. *nn.SELU*, *nn.CELU*, *nn.GELU*, *nn.swish (or SiLU same thing IG)* , *nn.HardSwish*
    *SELU(x)* = scale * (max(0,x) + min(0, alpha*(exp(x) - 1))) with alpha = 1.67326324... and scale = 1.0507009873..... 
    comes from Self normalizing neural nets in which selu are used. The idea of this network is that it is self normalizing, we don't need batch normalizing layers to normalize it.
    warning: if using kaiming_normal for initializing weights, then nonlinearity = 'linear' should be used instead of nonlinearity = 'selu' in order to get Self-Normalizing NN.
    *CELU(x)* = max(0,x) + min(0, alpha*(exp(x/alpha) - 1)) parameters: alpha-default=1.0
    If alpha set to default (1.0) then will be equivalent to ELU.
    *GELU(x)* = 0.5 * x * (1 + Tanh((2/pi)** 1/2 * (x + 0.044715 * x** 3)))
    Gaussian Error Linear Units
    
    f. Other non-linear activation functions:
    *nn.softmax*, *nn.softmin*, *nn.LogSoftmax*, *nn.AdaptiveLogSoftmaxWithLoss*
    [*nn.AdaptiveLogSoftmaxWithLoss*](https://docs.pytorch.org/docs/stable/generated/torch.nn.AdaptiveLogSoftmaxWithLoss.html#adaptivelogsoftmaxwithloss) - Used for training NN based Language models with very large vocabularies (i.e. large output spaces). Most effective when label distribution highly 
    imbalanced - partitions the labels into several clusters, according to there frequencies.
    Clusters may contain different number of targets each. Clusters containing less frequent labels assign lower dimensional embeddings to those labels, which speeds up the computation. For each minibatch, only clusters for which at least one target is present are evaluated.
    The idea is that the clusters which are accessed frequently (like the 1st one, containing most frequent labels), should also be cheap to compute - i.e. contain a small number of assigned labels.
    parameters: cutoffs - ordered sequence of integers sorted in increasing order. controls no.of clusters and partioning of targets into clusters. e.g. cutoffs = [10, 100, 1000] 1st 10 targets assigned to be 'head' of adaptive softmax, targets 11, 12, ... 100 assigned to 1st cluster, 101,...1000 assigned to 2nd cluster
    while remaining targets 1001,... n_classes-1 will be assigned to last, 3rd cluster.
    [Explained in detail here](https://arxiv.org/abs/1609.04309) 

5. [*Normalization Layers*](https://docs.pytorch.org/docs/stable/nn.html#normalization-layers):
Normalization technique used to make training of ANN faster and more stable by adjusting the inputs to each layer -- re-centering them around
zero and re-scaling them to a standard size (mean=0, std dev=1).
Experts still debating on why it actually works so well. Initially it was thought to tackle internal covariate shift (like the purpose of creating this was to tackle ICS)
Newer research suggests it doesn't fix this shift but instead smooths the objective function-a mathematical guide the network follows to improve (basically the gradient descent curve)- enhancing performance
In very deep NN, batch normalization can initially cause a severe gradient explosion-can be managed by shortcuts called skip connections in Residual Networks.

Internal Covariate Shift 
The input each layer of the NN receives follow a specific distribution, which shifts during training due to 2 main factors:
i. the random starting values of the network's settings (parameter initialization)
ii. The natural variation in the input data.
During training, as the parameters of preceeding layers adjust, the distribution of inputs to the current layer changes accordingly. such
that the current layer needs to constantly readjust to new distribtions. 
This issue is particularly severe in Deep NN, because small changes in shallower hidden layers will be amplified as they propagate within the
network, resulting in significant shift in the distribution of the deeper layers inputs.
Provides additional advantages as well:
i. can use higher learning rates - without causing problems like vanishing or exploding gradients - hence faster learning
ii. appears to have a regularizing effect, improving networks ability to generalize new data, reducing the need for dropout.

The internal working can be studied from wikipedia, it basically subtracts the mean and divides by standard deviation, which normalizes the
inputs to the activations (which have mean 0 and std dev 1), which belongs to a normal distribution. After this we have an option to change
the distribution by this formula: z~ = gamma * z^Norm^ + beta,  where gamma and beta are learnable parameters, this allows us to change the 
distribution of the inputs to the next layer because we don't always want them to be from one distribution, at some places yes, but not
everywhere, therefore we have this equation that learns those parameters to change them accordingly for each layer. 
[wiki link to Batch Norm](https://en.wikipedia.org/wiki/Batch_normalization)

**Important Note**: There is still a debate going whether to perform batch normalization on the activations which is being passed to the next
layer or to perform it on the 'Z' value i.e. before passing it to an activation function.
According to andrew ng, he mentioned that in practice mostly people perform BN on z values and then pass the normalized values to the activation
function, which then goes to the next layer as input.

Pytorch: 
*nn.BatchNorm1d(num_features, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True, device=None, dtype=None)*
Same for 2d and 3d

BatchNorm1d takes the input shape of 2Dimensions or 3Dimensions
2D -> (N, C) where N is batch size and C is no. of features -> e.g. commonly used after nn.Linear which outputs 2D tensors of (N, C)
3D -> (N, C, L) where N is batch size, C no. of channels and L is sequence length
Normalizes each layer independently for each feature/channel across the batch dimension.

BatchNorm2d
Input shape: designed for 4D inputs: (N, C, H, W) where N-Batch size, C-no. of channels, H-height, W-width
e.g. primarily used after 2D convolutional layers(nn.Conv2d)
Performs Spatial Batch Normalization, meaning it normalizes for each channel across the batch, height, and width dimensions.
This means a single mean and variance are calculated per channel for all spatial locations within that channel across the batch.

BatchNorm3d
Input shape: designed for 5D inputs: (N, C, D, H, W) where all same as above and D-Depth
e.g. used after 3D convolutional layers

By default, during training this layer keeps running estimates of its computed mean and variance, which are then used for normalization
during evaluation. The running estimates are kept with a default `momentum` of 0.1
Running estiamtes here are the moving averages used to calculate mean and variance with the specified momentum, if tracj_running_stats is set
to false then moving averages won't be used instead batch statistics mean and variance will be used during evaluation as well.

affine = True indicates learnable parameters, if set to false then the gamma and beta parameters wont change/learn.

*nn.LazyBatchNorm1d* or 2d or 3d
It is used to initialize the layers with uninitialized weights, that way the framework will automatically infer the parameters shape when first
called. This allows flexibility, making it easy to modify architectures and eliminating one common source of errors.

*nn.InstanceNorm1d* or 2d or 3d
used for improving real time image processing

**nn.LayerNorm**
Batch Normalization is dependent on the mini-batch size and it is not obvious how to apply it to recurrent neural networks (RNN).
Layer Normalization can be applied by computing the mean and variance used for normalization from all of the summed inputs to the neurons
in a layer on a single training case. Like BatchNorm, here each neuron is given its own adaptive bias and gain which are applied after the 
normalization but before the non-linearity. It also performs exactly the same computation at training and test times.
Also straight forward to apply to RNNs by computing the normalization statistics separately at each time step. -> effective at stabilizing the 
hidden state dynamics in RNN. 

So instead of computing mean and variance for each minibatch, we compute the mean and variance for each layer:
mean^l^ = 1/H summation from i=1 to H (a^l^) [image of formula](./LayerNorm_mean_var_formula.png)

All the hidden units in a layer share the same normalization terms, but different training cases have different normalization terms.
It also does not impose any constraint on the size of a mini-batch, we can have batch size 1.

Pytorch:
*nn.LayerNorm(normalized_shape, eps=1e-05, elementwise_affine=True, bias=True, device=None, dtype=None)*
Applies Layer normalization over a mini-batch of inputs.
The mean and std dev are calculated over the last D dimensions, where D is the dimension of normalized_shape. 
e.g. If normalized_shape is (3, 5) (a 2-dimensional shape), the mean and std dev are computed over the last 2 dimensions of the input (i.e. `input.mean((-2, -1))` )
here gamma and beta are the learnable affine transform parameters of normalized_shape if elementwise_affine is True.

*nn.RMSNorm* - LayerNorm adds a computational overhead, which makes these improvements expensive and significantly slows the underlying network.


6. [Recurrent Layers](https://docs.pytorch.org/docs/stable/nn.html#recurrent-layers):

*`nn.RNNBase(mode, input_size, hidden_size, num_layers=1, bias=True, ....)`*
Base class for RNN modules (RNN, LSTM, GRU)
Implements aspects of RNNs shared by the RNN, LSTM, and GRU classes, such as module initialization and utility methods for parameter storage
management.

Note: The forward method is not implemented by the RNNBase class.
Also LSTM and GRU classes override some methods implemented by RNNBase.

`nn.RNN(input_size, hidden_size, num_layers=1, nonlinearity='tanh', bias=True, batch_first=False, dropout=0.0, bidirectional=False, device=None, dtype=None)`
[source code of nn.RNN](https://github.com/pytorch/pytorch/blob/v2.7.0/torch/nn/modules/rnn.py#L469)
inherits from RNNBase
For each element in the input sequence, each layer computes the following function:
```math 
    h_t = \tanh(x_t W_{ih}^T + b_{ih} + h_{t-1}W_{hh}^T + b_{hh})
```
where `h_t` is the hidden state at time `t`, `x_t` is the input at time `t`, and `h_{(t-1)}` is the hidden state of the previous layer at time
`t-1` or the initial hidden state at time 0.

implementation equivalent to the following with bidirectional=False
```python

def forward(x, hx=None):
    if batch_first:
        x = x.transpose(0, 1)

    seq_len, batch_size, _ = x.size()
    if hx is None:
        hx = torch.zeros(num_layers, batch_size, hidden_size)
    h_t_minus_1 = hx
    h_t = hx
    output = []
    for t in range(seq_len):
        for layer in range(num_layers):
            h_t[layer] = torch.tanh(x[t] @ weight_ih[layer].T + bias_ih[layer] + h_t_minus_1[layer] @ weight_hh[layer].T + bias_hh[layer])
        output.append(h_t[-1])
        h_t_minus_1 = h_t

    output = torch.stack(output)
    if batch_first:
        output = output.transpose(0, 1)
    return output, h_t

```

args:
`input_size`: no. of expected features in the input `x`
`hidden_size`: no. of features or nodes in the hidden state `h`
`num_layers`: no. of recurrent layers. E.g., setting `num_layers=2` would mean stacking 2 RNNs together to form a Stacked RNN, with the 
              second RNN taking in ouputs of the 1st RNN and computing the final results. Default: 1
`nonlinearity`: either `tanh` or `relu`. Default: `tanh`
`bias`: for the bias term. Default: True
`batch_first`: If True then input and output tensors are provided as (batch, seq, features) instead of (seq, batch, features)
Note: this does not apply to the hidden or cell states 
`dropout`: if non-zero, introduces dropout layer on the outputs of each RNN layer except the last layer.
`bidirectional`: default: False


