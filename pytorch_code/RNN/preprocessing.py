import unicodedata
import string
import torch

# we can use "_" to represent any character out-of-vocabulary, that is, any character our model will not handle.
allowed_characters = string.ascii_letters + " .,;'" + "_"
n_letters = len(allowed_characters)


# turning unicode string to plain ASCII
def unicodeToASCII(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in allowed_characters
    )


# Converting names to Tensors
# First finding the index of the letter
def letterToIndex(letter):
    if letter not in allowed_characters:
        return allowed_characters.find("_")
    else:
        return allowed_characters.find(letter)


# turn a line into a <line_length x 1 x n_letters> tensor
def lineToTensor(name):
    tensor = torch.zeros(len(name), 1, n_letters)
    for li, letter in enumerate(name):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor


if __name__ == '__main__':

    # Testing unicodeToASCII function
    print(f"converting 'Ślusàrski' to {unicodeToASCII('Ślusàrski')}")

    # testing the one hot encoded vectors
    print(f"The letter 'a' becomes {lineToTensor('a')}")
    print(f"The name 'Ahn' becomes {lineToTensor('Ahn')}")
