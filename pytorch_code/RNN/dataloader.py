import torch
from io import open
import os
import glob
import time
from torch.utils.data import Dataset
from preprocessing import lineToTensor

DATA_DIR = "data/names"

# check if GPU available otherwise use CPU
device = torch.device('cpu')
if torch.cuda.is_available():
    device = torch.device('cuda')

torch.set_default_device(device)
print(f"using device: {torch.get_default_device()}")


class NamesDataset(Dataset):

    def __init__(self, data_dir="/home/sahil/Main/pytorch_code/RNN/data/names"):
        self.data_dir = data_dir
        self.load_time = time.localtime
        labels_set = set()

        self.data = []
        self.labels = []
        self.data_tensors = []
        self.labels_tensors = []

        # read all the '.txt' files in the specified directory
        text_files = glob.glob(os.path.join(data_dir, '*.txt'))
        for file_name in text_files:
            label = os.path.splitext(os.path.basename(file_name))[0]
            labels_set.add(label)
            lines = open(file_name, encoding='utf-8').read().strip().split('\n')
            for name in lines:
                self.data.append(name)
                self.data_tensors.append(lineToTensor(name))
                self.labels.append(label)

        # Cache the tensor representation of the labels
        self.labels_uniq = list(labels_set)
        for idx in range(len(self.labels)):
            temp_tensor = torch.tensor([self.labels_uniq.index(self.labels[idx])])
            self.labels_tensors.append(temp_tensor)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data_item = self.data[idx]
        data_label = self.labels[idx]
        data_tensor = self.data_tensors[idx]
        label_tensor = self.labels_tensors[idx]

        return label_tensor, data_tensor, data_label, data_item


if __name__ == '__main__':

    # checking the dataset
    all_Data = NamesDataset(DATA_DIR)
    print(f"loaded {len(all_Data)} items of data.")
    print(f"example: {all_Data[0]}")
    print(f"Labels list: {all_Data.labels_uniq}")

    train_set, test_set = torch.utils.data.random_split(all_Data, [.85, .15])
    print(f"train examples = {len(train_set)}, validation examples = {len(test_set)}")
