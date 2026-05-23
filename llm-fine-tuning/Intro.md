## Why we need Fine-Tuning?
1. Pre-trained models are generalists. Fine-tuning allows them to become specialists in a particular domain (e.g., legal, medical, financial, customer service) by adapting to it's specific terminology, style, and knowledge.
2. Pre-Trained good at general text generation, fine-tuning can make it excel at a very specific task like sentiment analysis, NER, summarization of legal docs, or generating code.
3. fine-tuned model almost always outperforms a general pre-trained model because it has learned to focus on the relevant patterns and information within that specific context.
4. Training a LLM from scratch requires astronomical amounts of data and computational resources. Fine-tuning requires significantly less data and compute.
5. building from scratch expensive. Fine-tuning offers a cost effective way to leverage existing powerful models and tailor them to specific needs.

## How Fine-tuning is different from Pre-training
The differences are in scale, objective, data, and computational cost.

a. Pre-training aims to impart broad language understanding, encompassing grammar, factual knowledge, and reasoning skills, by exposing model to extensive and varied text data.
This process involves unsupervised or self-supervised learning, where the model learns to predict subsequent words or complete missing ones.
b. training data for pre-training consists of billions of words - generally unlabelled or self-labelled.
c. pre-training starts from randomly initialised weights (starting from scratch).
d. training from ground up, requires substantial computational resources and extended periods.
e. expense - very high
f. yields versatile, general purpose language model capable of addressing a broad spectrum of tasks. 

fine-tuning
a. aims to tailor a pre-trained model's existing knowledge to excel in a specific task or domain.
b. smaller training data, task or domain relevant datasets - contains labelled examples.
c. model state begins with the pre-trained model's established weights.
d. shorter period and fewer computational resources for training.
strategies may involve training only the upper layers or applying a reduced learning rate across all layers.
e. relatively inexpensive
f. yields a specialized model highly optimised for a defined task or domain

## Post-Training
It is an umbrella term encompassing all the training and refinement steps applied to LLM after its pre-training.
