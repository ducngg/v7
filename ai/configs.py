import torch

# FIXED
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
TOTAL_WORDS = 17788+1
MAX_SEQUENCE_LEN = 32

# CHECKPOINT PATH
BASE_MODEL_CHECKPOINT_PATH = "checkpoints/v7gpt-1.3.pth"

# MODEL CONFIGURATIONS
MODEL_SIZES = {
    'base': {
        'block_size': MAX_SEQUENCE_LEN,
        'vocab_size': TOTAL_WORDS,
        'n_layer': 8,
        'n_head': 8,
        'n_embd': 256,
    }
}
