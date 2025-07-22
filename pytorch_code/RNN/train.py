import random
import numpy as np
from torch import nn
import torch
import time
from model1 import charRNN
import torch.utils.data
from preprocessing import n_letters
from dataloader import NamesDataset

DATA_DIR = "data/names"


def train(rnn, training_data, num_epochs=30, n_batch_size=128, report_every=3, lr=0.2, criterion=nn.NLLLoss()):
    """
    Training loop initiated here on the specified batch_size and epochs
    """
    # keeping track of the loss
    current_loss = 0
    all_losses = []
    rnn.train()
    optimizer = torch.optim.SGD(rnn.parameters(), lr=lr)

    print(f"training on dataset with n = {len(training_data)}")

    for iter in range(1, num_epochs+1):
        rnn.zero_grad()  # clearing the gradients very important step

        # create minibatches
        # cannot use dataloader for mini batches here because each of our names are of different lengths
        batches = list(range(len(training_data)))
        random.shuffle(batches)
        batches = np.array_split(batches, len(batches)//n_batch_size)

        for idx, batch in enumerate(batches):
            batch_loss = 0
            for i in batch:  # each example in the batch
                (label_tensor, text_tensor, label, text) = training_data[i]
                output = rnn.forward(text_tensor)
                loss = criterion(output, label_tensor)
                batch_loss += loss

            # optimize the parameters
            batch_loss.backward()
            nn.utils.clip_grad_norm_(rnn.parameters(), 3)
            optimizer.step()
            optimizer.zero_grad()

            current_loss += batch_loss.item() / len(batch)  # normalizing the batch loss and adding to the overall loss

        all_losses.append(current_loss / len(batches))
        if iter % report_every == 0:
            print(f"{iter} ({iter/num_epochs:.0%}): \t average batch loss = {all_losses[-1]}")
        current_loss = 0

    return all_losses


if __name__ == "__main__":

    # checking the dataset
    all_Data = NamesDataset(DATA_DIR)
    #   print(f"loaded {len(all_Data)} items of data.")
    #   print(f"example: {all_Data[0]}")
    #   print(f"Labels list: {all_Data.labels_uniq}")

    train_set, test_set = torch.utils.data.random_split(all_Data, [.85, .15])
    print(f"train examples = {len(train_set)}, validation examples = {len(test_set)}")

    # creating an RNN network with 58 input nodes, 128 hidden nodes and 18 output nodes
    n_hidden = 128
    rnn = charRNN(n_letters, n_hidden, len(all_Data.labels_uniq))
    print(rnn)

    # Testing the output labels
    #   input = lineToTensor("Albert")
    #   output = rnn(input)
    #   print(output)
    #   print(label_from_output(output, all_Data.labels_uniq))
    start_time = time.time()
    all_losses = train(rnn, all_Data)
    end_time = time.time()
    print(f"training took {end_time - start_time}")
