import torch.nn as nn
import torch.utils.data
from preprocessing import n_letters
from dataloader import NamesDataset

DATA_DIR = "data/names"


class charRNN(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super(charRNN, self).__init__()

        self.rnn = nn.RNN(input_size, hidden_size)
        self.h2o = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, line_tensor):
        rnn_out, hidden = self.rnn(line_tensor)
        output = self.h2o(hidden[0])
        output = self.softmax(output)

        return output


if __name__ == '__main__':

    # checking the dataset
    all_Data = NamesDataset(DATA_DIR)
    print(f"loaded {len(all_Data)} items of data.")
    print(f"example: {all_Data[0]}")
    print(f"Labels list: {all_Data.labels_uniq}")

    train_set, test_set = torch.utils.data.random_split(all_Data, [.85, .15])
    print(f"train examples = {len(train_set)}, validation examples = {len(test_set)}")

    # creating an RNN network with 58 input nodes, 128 hidden nodes and 18 output nodes
    n_hidden = 128
    rnn = charRNN(n_letters, n_hidden, len(all_Data.labels_uniq))
    print(rnn)
