import torch
import torch.nn as nn
import torch.nn.functional as F

from .configs import MAX_SEQUENCE_LEN, TOTAL_WORDS

class SmallTransformerEncoderModel(nn.Module):
    def __init__(self, vocab_size=TOTAL_WORDS, embed_dim=128, num_heads=8, num_layers=3, hidden_dim=512, max_seq_len=MAX_SEQUENCE_LEN):
        super(SmallTransformerEncoderModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.pos_embedding = nn.Embedding(max_seq_len, embed_dim)
        transformer_layer = nn.TransformerEncoderLayer(embed_dim, num_heads, hidden_dim)
        self.transformer = nn.TransformerEncoder(transformer_layer, num_layers)
        self.fc = nn.Linear(embed_dim, vocab_size)

    def forward(self, x):
        seq_len = x.size(1)
        pos = torch.arange(0, seq_len, device=x.device).unsqueeze(0)
        x = self.embedding(x) + self.pos_embedding(pos)
        x = self.transformer(x)
        x = self.fc(x)
        return F.log_softmax(x, dim=-1)
    