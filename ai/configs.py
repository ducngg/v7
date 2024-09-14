import torch

# FIXED
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
TOTAL_WORDS = 17788+1
MAX_SEQUENCE_LEN = 32
MODEL_PATH = "checkpoints/v7gpt.pth"
