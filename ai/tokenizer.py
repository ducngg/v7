import json
from models import Triplet, Word

from utils.decorators import singleton

@singleton
class Tokenizer:
    def __init__(
        self, 
        enum_path="checkpoints/enum.json", 
        renum_path="checkpoints/renum.json", 
        renum_crt_path="checkpoints/renum_crt.json",
        verbose=1
    ):  
        self.location = "<ai.tokenizer.Tokenizer>"
        self.PADDING_TOKEN_INDEX = 0
        
        with open(enum_path, 'r') as f:
            self.enum: dict[str, int] = json.load(f)
        with open(renum_path, 'r') as f:
            self.renum: dict[int, str] = json.load(f)
        with open(renum_crt_path, 'r') as f:
            self.renum_crt: list[tuple[str, str, int]] = json.load(f)
        self.renum_triplet = [None] + [Triplet(consonant=c, rhyme=r, tone=t) for c, r, t in self.renum_crt[1:]]
        
        if verbose:
            print(f"{self.location} Loaded: {len(self.renum_triplet)} tokens")

                            
    def tokenize(self, words: list[str]) -> list[int]:
        return [self.enum[word] for word in words if word in self.enum]
    def detokenize(self, tensor: list[int]) -> list[Word]:
        return [self.renum[id] for id in tensor]
    def analyze(self, tensor: list[int]) -> list[tuple[str, str, int]]:
        return [self.renum_crt[id] for id in tensor]
    def triplets(self, tensor: list[int]) -> list[Triplet]:
        return [self.renum_triplet[id] for id in tensor]

tokenizer = Tokenizer()
