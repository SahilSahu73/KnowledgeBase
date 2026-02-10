from logger_config import logger
import torch
from multi_head import MultiHeadSelfAttention


if __name__ == "__main__":
    """
    B = Batch size, T = Sequence length of a particular row of data (assume as context length),
    d_model = Embedding dim, n_head = no. of heads that needs to be configured in our scaled
    dot product attention mechanism
    Core idea is to that the d_model i.e. the embedding dimensions gets splits into the
    no. of heads we configure in n_head.
    as per below config, each head will be of size 12/3 = 4
    """
    B, T, d_model, n_head = 1, 5, 12, 3
    d_head = d_model // n_head
    assert d_model % n_head == 0, "The embedding dims is not divisible by the # heads!!!!"

    x = torch.randn(B, T, d_model)
    attn = MultiHeadSelfAttention(d_model, n_head, trace_shapes=True)

    logger.info(f"Input x: {tuple(x.shape)} = (B, T, d_model)")
    qkv = attn.qkv(x)  # (B, T, 3*d_model) is returned, which represents q, k and v matrices concatenated.
    logger.info(f"Linear qkv(x): {tuple(qkv.shape)} = (B, T, 3*d_model)")

    qkv = qkv.view(B, T, 3, n_head, d_head)
    logger.info(f"view to 5D: {tuple(qkv.shape)} = (B, T, 3, n_head, d_head)")

    q, k, v = qkv.unbind(dim=2)
    logger.info(f"q,k,v split:  q={tuple(q.shape)} k={tuple(k.shape)} v={tuple(v.shape)}")

    q = q.transpose(1, 2)
    k = k.transpose(1, 2)
    v = v.transpose(1, 2)
    logger.info(f"Transpose heads: q = {q.shape}")
