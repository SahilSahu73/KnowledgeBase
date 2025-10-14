---
title: "__init__"
date: "2025-08-26"
unique_id: "08aa570a9191ac42aa512102dcc6ea3ffa1d478ec83618c8cc670a6c6c2782a7"
author: "AutoMigrationScript"
tags: []
description: ""
---
# Quickstart on Pytorch and getting to know about the basic functions

Pytorch has 2 primitives to work with data `torch.utils.data.Dataset` and `torch.utils.data.DataLoader`
Dataset stores the samples and their corresponding labels.
DataLoader wraps an iterable around the Dataset.
We pass the Dataset as an argument to the DataLoader. This wraps an iterable over the dataset and supports automatic batching,
sampling, shuffling and multiprocess data loading.

To create a Neural Network, we need to create a class that inherits from `nn.Module`
We define the layers of the network in __init__ function and specify how data will pass through the network in the `forward` function.
To accelerate operations -> use CUDA or any other accelerator available, by default CPU.

To train model we need loss function and an optimizer.

Saving models - common way to do that is to serialize the internal state dictionary (containing the model parameters).
`torch.save(model.state_dict(), "model.pth")`
Loading model - re-creating the model structure and loading the state dictionary into it.


Tensors -> specialized data structure similar to NumPy ndArrays + can run on GPUs or other hardware accelerators.
Tensors and NumPy arrays can often share the same underlying memory, eliminating the need to copy data.
