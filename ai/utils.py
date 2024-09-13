import torch
import torch.nn.functional as F
import time
from utils.preprocess import standardize_data
from .tokenizer import tokenizer
from .configs import MAX_SEQUENCE_LEN, DEVICE, MODEL_PATH
from .model import GPT

def next(model: GPT, seqs: list[str]) -> list[list[int]]:
    # Standardize and tokenize the input sequences
    seqs = [standardize_data(seq).lower() for seq in seqs]
    tokens = [tokenizer.tokenize(seq.split())[-MAX_SEQUENCE_LEN:] for seq in seqs]
    tokens = torch.tensor(tokens, dtype=torch.long).to(DEVICE)

    model = model.to(DEVICE)

    with torch.no_grad():
        # Forward pass through the model
        logits = model(tokens)[0]  # (B, T, vocab_size)
        
        # Take logits at the last position
        logits = logits[:, -1, :]  # (B, vocab_size)
        
        # Get the indices that would sort the logits in descending order
        sorted_indices = torch.argsort(logits, dim=-1, descending=True)
        
        # Convert to list of indices
        sorted_indices_list = sorted_indices.cpu().tolist()
    
    return sorted_indices_list

def generate(model: GPT, seq: str, n: int):
    tokens = tokenizer.tokenize(seq.split())
    tokens = torch.tensor(tokens, dtype=torch.long)
    tokens = tokens.unsqueeze(0)
    
    model = model.to(DEVICE)
    x = tokens.to(DEVICE)
    
    generated_tokens = []
    
    for _ in range(n):
        with torch.no_grad():
            logits = model(x)[0] # (B, T, vocab_size)

            # Take logits at the last position
            logits = logits[:, -1, :] # (B, vocab_size)
            probs = F.softmax(logits, dim=-1) 

            # Take just topk is 50
            topk_probs, topk_indices = torch.topk(probs, 50, dim=-1) # (B, 50)

            ix = torch.multinomial(topk_probs, 1) # (B, 1)
            xcol = torch.gather(topk_indices, -1, ix) # (B, 1)
            
            generated_tokens.append(xcol[0][0].tolist())

            x = torch.cat((x, xcol), dim=1)
            x = x[:, -MAX_SEQUENCE_LEN:] # take just the last MAX_SEQUENCE_LEN tokens
            
    return tokenizer.detokenize(generated_tokens)

def get_model(path=MODEL_PATH, verbose=1):
    model = GPT()
    model.load_state_dict(torch.load(path, map_location=torch.device(DEVICE)), strict=False)
    
    if verbose:
        print(f"\tCheckpoint path: {path}")
        total_params = sum(p.numel() for p in model.parameters())
        print(f"\tTotal number of parameters: {total_params}")
    
    return model
