import torch
import torch.nn as nn
import numpy as np


class ScaledDotProductAttention(nn.Module):
    """ Scaled Dot-Product Attention """

    def __init__(self, temperature):
        super().__init__()
        self.temperature = temperature
        self.softmax = nn.Softmax(dim=2)

    def forward(self, q, k, v, mask=None):
        # for AMP
        q = q.to(torch.float32)
        k = k.to(torch.float32)
        attn = torch.bmm(q, k.transpose(1, 2))
        # batchを無視して, 第2,3次元で行列計算↑
        attn = attn / self.temperature

        if mask is not None:
            attn = attn.masked_fill(mask, -np.inf)
            # softmaxをとるので-infで埋める.

        attn = self.softmax(attn)
        output = torch.bmm(attn, v)

        return output, attn
