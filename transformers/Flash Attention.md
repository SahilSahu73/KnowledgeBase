- Transformer models are slow and memory hungry on long sequences - time and memory complexity are quadratic.
- Flash attention gives 3x speed on GPT-2

Basic terminology
What is compute -> Time spent on your GPU computing actual floating point operations (FLOPS)
What is memory -> Time spent transferring tensors within a GPU

Ideally -> want gCPU to be performing matrix multi. all the time and not restricted by memory.
Reality -> compute made more progress than memory, cause of which gCPU sits idle waiting for data to be loaded. => Memory Bound operation

So self-attention architecture is memory-bound.
Operations like softmax, mask, dropout are taking majority of the time as compared to matmul.
This happens because of the scale at which these operations takes place, which is our main bottleneck.
N -> number of tokens (context length)
d -> embedding dimensions
when Query and Key^T are multiplied, the attention matrix explodes to N * N which takes a lot of memory. For reference (d ~ 128; N ~128k tokens) in case of gemini: ~ 1 million tokens
O = Dropout(Softmax(Mask(QK^T)))V

## How is Self Attention implemented?
### \[Algorithm]:

Require: Matrices **Q, K, V** \[N X d] in HBM (high-bandwidth memory)
1. Load Q, K by blocks from HBM, compute S = QK^T, write S to HBM.
2. Read S from HBM, compute P = softmax(S), write P to HBM.
3. Load P and V by blocks from HBM, compute O = PV, write O to HBM.
4. Return O.

As we can see from the above algorithm there is alot of information transferring happening from HBM to gCPU and from gCPU to the HBM, making it memory-bound operation.

### \[MatMul]:

![flash-attention-image](transformers/self-attention-image.webp)

Simplified version
Step 1: each token is added with positional encoding to generate embedding to feed into a linear layer to generate <key, query, value>. For illustration, used 3 size embeddings in the image.

Step 2: Key -> key' (transpose) is computed, and multiplied with Query to give QK' which is N * N. This contains the attention of each token with the rest of the tokens. Since we need to compute the importance of each token w.r.t. each other, softmax operation is applied
row-wise to normalize it from 0 to 1.
This step requires movement to HBM and is the most expensive operation. Entire flash attention is about how to optimize this process.

Step 3: Softmax(QK') * V is computed as the final output matrix. Same dimension as K, Q, V
each row represents the particular words relations with the other words.
e.g. 1 * 5 means, the embeddings of "this" should be changed to incorporate relations with other tokens.

## How is Flash attention implemented?

**Algorithm**
Require: Matrices Q, K, V \[N X d]  in HBM, on-chip SRAM of size M.
1. Set block sizes Bc = ceil(M/4d) , Br = min(ceil(M/4d), d)
2. Initialize O = (0) \[N X d], l = (0) \[N], m = (-inf) \[N] in HBM
3. 