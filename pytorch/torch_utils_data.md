---
title: "torch_utils_data"
date: "2025-08-26"
unique_id: "43f479c8e550768fa192ec60fa04d42d3cfe83a21b6a73ba5c01cfcd8dd07843"
author: "AutoMigrationScript"
tags: []
description: ""
---
# torch.utils.data 
In this module I will be studying more about torch.utils.data features and a little bit about how it works.

Heart of the PyTorch data loading utility - `torch.utils.data.DataLoader` class.
It represents a Python iterable over a dataset with support for:
1. map-style and iterable-stye datasets
2. customizing data loading order
3. automatic batching
4. single- and multi-process data loading
5. automatic memory pinning

These options are configured by the constructor arguments of the `Dataloader`:
```python
DataLoader(dataset, batch_size=1, shuffle=False, sampler=None,
           batch_sampler=None, num_workers=0, collate_fn=None,
           pin_memory=False, drop_last=False, timeout=0,
           worker_init_fn=None, *, prefetch_factor=2,
           persistent_workers=False)
```


### Dataset Types
1. Map-style dataset implements the __getitem__() and __len__() protocols, and represents a map from (possibly non-integral) indices/keys
to data samples.
Example: such a dataset, when accessed with `dataset[idx]`, could read the idx-th image and its corresponding label from a folder
on the disk.

`CLASS torch.utils.data.Dataset` 
All datasets that represent a map from keys to data samples should subclass this.
All subclasses should overwrite `__getitem__()`, supporting fetching a data sample for a given key.
Could also optionally overwrite `__len__()`, which is expected to return the size of the dataset by many Sampler implementations and 
the default options of DataLoader.
Can also optionally implement `__getitems__()` for speedup batched sample loading. This method accepts list of indices of samples of batch
and returns a list of samples.


2. Iterable-style dataset - instance of a subclass of `IterableDataset` that implements the `__iter__()` protocol, and 
represents an iterable over data samples.
This type of dataset is particularly suitable for cases where random reads are expensive or even improbable, and where the batch size
depends on the fetched data.
Example, such a dataset, when called `iter(dataset)`, could return a stream of data reading from a database. a remote server, or even
logs generated in real time.

When using Iterable-style dataset with multi-process data loading, the same dataset object is replicated on each worker process, and
thus the replicas must be configured differently to avoid data duplication. [https://docs.pytorch.org/docs/stable/data.html#torch.utils.data.IterableDataset]


### Data Loading Order and Sampler
Iterable-style datasets -> data loading order is entirely controlled by the user-defined iterable. Allows easier implementations
of chunk-reading and dynamic batch size (e.g. by yielding a batched sample at each time).

For map-style datasets -> `torch.utils.data.Sampler` classes are used to specify the sequence of indices/keys used in data loading.
They represent iterable objects over the indices to datasets.
E.g. Common case with Stochastic Gradient Descent (SGD), a sampler could randomly permute a list of indices and yield each one at a time,
or yield a small number of them for mini-batch SGD.

A sequential or shuffled sampler constructed automatically - based on shuffle argument passed to DataLoader.
Can also pass custom sampler object that at each time yields the next index/key to fetch.
Custom sampler that yields a list of batch indices at a time - passed as `batch_sampler` argument.
Automatic batching enabled via - `batch_size` and `drop_last` arguments.
Note - Neither `Sampler` nor `batch_sampler` is compatible with Iterable-style datasets, since such datasets have no notion of keys or indices.


### Loading Batched and Non-Batched Data
DataLoader supports automatically collating individual data samples into batches via arguments `batch_size`, `drop_last`, `batch_sampler`
and `collate_fn`(this has a default function).

1. Automatic Batching (default)
Corresponds to fetching a minibatch of data and collating them into batched samples, i.e., containing Tensors with one dimension being
the batch dimension (usually the first).

if batch_size is not None (default 1) -> data loader yields batched samples instead of individual samples.
`batch_size` and `drop_last` arguments used to specify how the data loader obtaines batches of dataset keys.

2. Disable Automatic Batching
When `batch_size` and `batch_sampler`(default None) both are None, automatic batching is disabled. Each sample obtained from the dataset
is processed with the function passed as the `collate_fn` argument.
Useful in cases when users want to handle batching manually in dataset code, or simply load individual samples.
E.g. It could be cheaper to directly load batched data(e.g. bulk reads from a database or reading continuos chunks of memory), or the batch
size is data dependent, or the program is designed to work on individual samples.

When automatic batching disabled - default collate_fn simply converts NumPy arrays into Pytorch Tensors, and keeps everything else untouched.


### Working with Collate function

*When automatic batching disabled*
`collate_fn` is called with each individual data sample, and the output is yielded from the data loader iterator.
In this case default `collate_fn` converts NumPy arrays into Pytorch Tensors.

*When automatic batching enabled*
`collate_fn` is called with a list of samples at each time. It is expected to collate the input samples into a batch for yielding from the 
data loader iterator.

Behaviour of Default collate function:
For instance each element of the dataset returns a tuple (image, class_index), the default `collate_fn` collates a list of such tuples into a
single tuple of a batched image tensor and a batched class label tensor.

Default `collate_fn` has the following properties:
- It always prepends a new dimension as the batch dimension.
- Automatically converts Numpy arrays and python numerical values into Pytorch tensors.
- Preserves the data structure. E.g. if each sample is dictionary, then it outputs a dictionary with the same set of keys but batched tensors
as values.

users may customize `collate_fn` to achieve custom batching, e.g., collating along a dimension other than the first, padding sequences of
various length, or adding support for custom data types.


### IMPORTANT NOTE:
DataLoader uses `torch.stack()` by default to collate a batch from the list of samples provided. This requires **all tensors in a batch to be of
the same shape.** If each sample is of varying lengths then `torch.stack()` will fail with:
`RuntimeError: stack expects each tensor to be equal size …`

There are 2 ways to solve this problem:
1. **pad sequence to the same length per batch**, using:
    - `collate_fn` that pads (e.g., with zeros or a PAD token) to match the longest subsequence in the batch.
    - use `torch.nn.utils.rnn.pad_sequence()` and `pack_padded_sequence()` in model

2. **use custom batching**:
    - create batches where all examples share the same length. (would not recommend to do this.)


### Single and Multi-process Data Loading

DataLoader uses single-process dataloading by default.
Within a Python process, the Global Interpreter Lock (GIL) prevents true fully parallelizing python code across threads. To avoid blocking
computation code with data loading, pytorch provides an easy switch to perform multi-process data loading by simply setting the argument
`num_workers` to a positive integer.

*Single-process data loading (default)*
In this mode, data fetching done in the same process a Dataloader is initialized. Therefore, data loading may block computing.
However, may be preferred when resource used for sharing data among processes is limited (e.g. shared memory, file descriptors),
or when the entire dataset is small and can be loaded entirely in memory.

*Multi-process data loading*
setting `num_workers` as a positive integer turns on multi-process data loading with the specified number of loader worker processes.

