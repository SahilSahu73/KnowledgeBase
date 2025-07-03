# DataLoaders and Datasets

Ideally want to decouple(separate) our dataset code from our model training code for better readability and modularity.
PyTorch has 2 data primitives: `torch.utils.data.DataLoader` and `torch.utils.data.Dataset` that allows us to use pre-loaded datasets
as well as your own data.
Dataset stores the samples and their corresponding labels, and DataLoader wraps an iterable around the Dataset to enable easy access
to the samples.

### Dataset:
PyTorch domain libraries provide a number of pre-loaded datasets (such as FashionMNIST) that subclass `torch.utils.data.Dataset` 
and implement functions specific to the particular data. They can be used to prototype and benchmark your model.

*Loading a Dataset*
Example - Fashion-MNIST dataset from torchvision
To load the dataset use datasets.FashionMNIST
```python
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor

training_data = datasets.FashionMNIST(
    root = 'data', # directory/path where the train/test data is stored
    train = True, # specifies training or test data
    download = True, # download the data from the internet if not available at root
    transform = ToTensor() # specify the feature transformations
)

testing_data = datasets.FashionMNIST(
    root = 'data', 
    train = False,
    download = True,
    transform = ToTensor()
)
```

*Iterating and visualizing the dataset*
Can index Datasets manually like a list: `training_data[index]` 
here in this case one index returns 2 values, image and it's corresponding label
`img, label = training_data[index]`


==**Creating a Custom Dataset for my Files**==
A custom Dataset class must implement 3 functions: __init__, __len__, __getitem__.
```python
import pandas as pd
from torchvision.io import decode_image
from torch.utils.data import Dataset

class CustomImageDataset(Dataset):
    
    def __init__(self, img_dir, annotations_file, transform=None, target_transform=None):
        self.img_dir = img_dir
        self.labels = pd.read_csv(annotations_file) # example case wherein the annotations are in a csv file
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.labels.iloc[idx, 0])
        image = decode_image(img_path)
        label = self.labels.iloc[idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label
```

Description of the code snippet above
__init__
The init function is run once when instantiating the Dataset object. We initialize the directory containing the images, the annotation files,
and both transforms.
The labels csv looks like:
tshirt1.jpeg, 0
tshirt2.jpeg, 0
.....
ankleboot99.jpeg, 9

__len__
The __len__ function(to be accurate method) returns the no. of samples in our dataset.

__getitem__
This function loads and returns a sample from the dataset at the given index `idx`. Based on the index it identifies the image's location
on disk, converts that to a tensor using `decode_image()`, retrieves the corresponding label from the csv data in `self.labels`, calls
the transform functions on them (if applicable), and returns the tensor image and corresponding label in a tuple.


**Preparing my data for training with DataLoaders**
Dataset retrieves our dataset's features and labels one sample at a time. We typically want to pass samples in "minibatches", reshuffle
the data at every epoch to reduce model overfitting, use Python's multiprocessing to speed up data retrieval.
DataLoader does all that....


**Iterate through the DataLoader**
Each iteration returns a batch of `train_features` and `train_labels` (based on what `batch_size` is passed)
Also, if Shuffle=True then after all batches are iterated then the entire data is reshuffled and then batched again.

