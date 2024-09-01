import json

class Tokenizer:
    def __init__(
        self, 
        enum_path="checkpoints/enum.json", 
        renum_path="checkpoints/renum.json", 
        renum_crt_path="checkpoints/renum_crt.json"
    ):
        with open(enum_path, 'r') as f:
            self.enum: dict[str, int] = json.load(f)
        with open(renum_path, 'r') as f:
            self.renum: dict[int, str] = json.load(f)
        with open(renum_crt_path, 'r') as f:
            self.renum_crt: dict[int, tuple[str, str, int]] = json.load(f)
                            
    def tokenize(self, words: list[str]) -> list[int]:
        return [self.enum[word] for word in words if word in self.enum]
    def detokenize(self, tensor: list[int]) -> list[str]:
        return [self.renum[id] for id in tensor]
    def analyze(self, tensor: list[int]) -> list[tuple[str, str, int]]:
        return [self.renum_crt[id] for id in tensor]

tokenizer = Tokenizer()
