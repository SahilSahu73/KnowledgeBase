---
title: "Tensors"
date: "2025-08-26"
unique_id: "819423616caab7306f7d0fc329af9a90c6cc32131ef8aa0d15b3323afadddfc1"
author: "AutoMigrationScript"
tags: []
description: ""
---
# Tensors

### Initializing Tensors
1. Directly from data - data type is automatically inferred
`data = [[1, 2], [3, 4]]
x_data = torch.tensor(data)`

2. From Numpy array - `torch.from_numpy(np_array)`

3. From another tensor - new tensor retains properties (shape, datatype) of the argument tensor; unless explicitly overridden
`torch.ones_like(), torch.zeros_like() and torch.rand_like()`

4. Initialize with random or constant values
`torch.ones(shape)`, `torch.zeros(shape)`, and `torch.rand(shape)`

### Major attributes of a Tensor
shape, dtype and device

### Operations on Tensors
There are more than 1200 operations, including arithmetic, linear algebra, matrix manipulation (slicing, indexing, transposing etc.), 
sampling and many more described here - [https://docs.pytorch.org/docs/stable/torch.html]
These operations can be run on accelerators, using the `.to` method we have to explicitly move the tensors to those devices
Keep in mind that copying those tensors across devices can be expensive in terms of time and memory.

joining tensors - `torch.cat()` to concatenate a sequence of tensors along an existing dimension.
`torch.stack()` to concatenate a sequence of tensors along a new dimension.
For both operations, all tensors need to be of same size.

**Arithmetic Operations:**
y1 = tensor @ tensor.T 
@ - matmul
.T - Transpose

*Another way of doing matmul:*
y2 = tensor.matmul(tensor.T)
torch.matmul(tensor, tensot.T, out=y3)

*element-wise multiplication*
z1 = y1 * y2   
z2 = tensor.mul(tensor)
torch.mul(tensor, tensor, out=z3)


If we have a one-element tensor (maybe by aggregating all the values of a tensor into one), then using `.item()` can convert it into
a python numerical value.

*In-place operations:*
Stores the result into the operand, denoted by a _ suffix.
`tensor.add_(5)`
*IMP Note - In-place operations might save some memory, but can be problematic when computing derivatives because of an immediate loss
of history. Hence, their use is discouraged.*


### Bridge with NumPy
*Tensors on the CPU and NumPy arrays can share their underlying memory locations, and changing one will change other.*
Tensor to NumPy array
```python
t = torch.ones(5)
n = t.numpy()
# Any operation on one tensor will change both
t.add_(2) # change in the tensor reflects in the Numpy array
```
NumPy array to Tensor
```python
n = np.ones(5)
t = torch.from_numpy(n)

np.add(n, 1, out=n)
# changes can be seen in both
```

