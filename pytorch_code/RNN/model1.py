import torch.nn as nn


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


def label_from_output(output, output_label):
    top_n, top_i = output.topk(1)
    print(output.topk(1))
    label_i = top_i[0].item()
    return output_label[label_i], label_i
