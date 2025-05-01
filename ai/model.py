import os
import math
import time
import inspect
from dataclasses import dataclass
import torch
import torch.nn as nn
from torch.nn import functional as F

from .configs import MAX_SEQUENCE_LEN, TOTAL_WORDS
from .tokenizer import tokenizer

# -----------------------------------------------------------------------------
# From Andrej Karpathy build nanoGPT

@dataclass
class GPTConfig:
    block_size: int # Current max sequence length
    vocab_size: int # Run overview.py for more information
    n_layer: int # number of layers
    n_head: int # number of heads
    n_embd: int # embedding dimension

class CausalSelfAttention(nn.Module):
    def __init__(self, config: GPTConfig):
        super().__init__()
        assert config.n_embd % config.n_head == 0
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd)
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)
        self.c_proj.NANOGPT_SCALE_INIT = 1
        # regularization
        self.n_head = config.n_head
        self.n_embd = config.n_embd

    def forward(self, x: torch.Tensor, attention_mask: torch.Tensor = None, is_causal=False):
        B, T, C = x.size()  # batch size, sequence length, embedding dimension
        qkv = self.c_attn(x)
        q, k, v = qkv.split(self.n_embd, dim=2)
        k = k.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)  # (B, nh, T, hs)
        q = q.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)  # (B, nh, T, hs)
        v = v.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)  # (B, nh, T, hs)
        
        # Apply scaled dot-product attention with masking
        y = F.scaled_dot_product_attention(q, k, v, attn_mask=attention_mask, is_causal=bool(is_causal))
        
        y = y.transpose(1, 2).contiguous().view(B, T, C)  # reassemble head outputs
        y = self.c_proj(y)
        return y


class MLP(nn.Module):

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.c_fc    = nn.Linear(config.n_embd, 4 * config.n_embd)
        self.gelu    = nn.GELU(approximate='tanh')
        self.c_proj  = nn.Linear(4 * config.n_embd, config.n_embd)
        self.c_proj.NANOGPT_SCALE_INIT = 1

    def forward(self, x):
        x = self.c_fc(x)
        x = self.gelu(x)
        x = self.c_proj(x)
        return x

class Block(nn.Module):

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd)
        self.mlp = MLP(config)

    def forward(self, x: torch.Tensor, attention_mask: torch.Tensor = None, is_training=False):
        x = x + self.attn(self.ln_1(x), attention_mask, is_causal=is_training)
        x = x + self.mlp(self.ln_2(x))
        return x
    
class GPT(nn.Module):

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.config = config

        self.transformer = nn.ModuleDict(dict(
            wte = nn.Embedding(config.vocab_size, config.n_embd),
            wpe = nn.Embedding(config.block_size, config.n_embd),
            h = nn.ModuleList([Block(config) for _ in range(config.n_layer)]),
            ln_f = nn.LayerNorm(config.n_embd),
        ))
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)

        # weight sharing scheme
        self.transformer.wte.weight = self.lm_head.weight

        # init params
        self.apply(self._init_weights)
    
    @property
    def device(self):
        return next(self.parameters()).device

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            std = 0.02
            if hasattr(module, 'NANOGPT_SCALE_INIT'):
                std *= (2 * self.config.n_layer) ** -0.5
            torch.nn.init.normal_(module.weight, mean=0.0, std=std)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, tensors, targets=None, attention_mask=None, is_training=False):
        B, T = tensors.size()
        assert T <= self.config.block_size, f"Sequence length exceeds {self.config.block_size=}"
        
        # Token and position embeddings
        pos = torch.arange(0, T, dtype=torch.long, device=tensors.device)
        tok_emb = self.transformer.wte(tensors)
        pos_emb = self.transformer.wpe(pos)
        x = tok_emb + pos_emb

        # Generate mask if not provided
        if attention_mask is None:
            attention_mask = (tensors != tokenizer.PADDING_TOKEN_INDEX).unsqueeze(1).unsqueeze(2)  # (B, 1, 1, T)
            attention_mask = attention_mask.to(dtype=x.dtype)  # Convert to float for scaling
            # print(attention_mask, attention_mask.shape)
             
        # Transformer blocks
        for block in self.transformer.h:
            x = block(x, attention_mask=attention_mask, is_training=is_training)
        
        # Final layer norm and head
        x = self.transformer.ln_f(x)
        logits = self.lm_head(x)

        # TODO: Move loss outside train
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1), ignore_index=tokenizer.PADDING_TOKEN_INDEX)
        
        return logits, loss

    # def configure_optimizers(self, weight_decay, learning_rate, device_type):
    #     # start with all of the candidate parameters (that require grad)
    #     param_dict = {pn: p for pn, p in self.named_parameters()}
    #     param_dict = {pn: p for pn, p in param_dict.items() if p.requires_grad}
    #     # create optim groups. Any parameters that is 2D will be weight decayed, otherwise no.
    #     # i.e. all weight tensors in matmuls + embeddings decay, all biases and layernorms don't.
    #     decay_params = [p for n, p in param_dict.items() if p.dim() >= 2]
    #     nodecay_params = [p for n, p in param_dict.items() if p.dim() < 2]
    #     optim_groups = [
    #         {'params': decay_params, 'weight_decay': weight_decay},
    #         {'params': nodecay_params, 'weight_decay': 0.0}
    #     ]
    #     num_decay_params = sum(p.numel() for p in decay_params)
    #     num_nodecay_params = sum(p.numel() for p in nodecay_params)
    #     if master_process:
    #         print(f"num decayed parameter tensors: {len(decay_params)}, with {num_decay_params:,} parameters")
    #         print(f"num non-decayed parameter tensors: {len(nodecay_params)}, with {num_nodecay_params:,} parameters")
    #     # Create AdamW optimizer and use the fused version if it is available
    #     fused_available = 'fused' in inspect.signature(torch.optim.AdamW).parameters
    #     use_fused = fused_available and device_type == "cuda"
    #     if master_process:
    #         print(f"using fused AdamW: {use_fused}")
    #     optimizer = torch.optim.AdamW(optim_groups, lr=learning_rate, betas=(0.9, 0.95), eps=1e-8, fused=use_fused)
    #     return optimizer
