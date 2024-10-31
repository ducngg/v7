from typing import List, Union, Literal
from pydantic import BaseModel
from .primitive import Phrase, Word

class Args(BaseModel):
    verbose: int
    minimal: bool
    size: str
    model: str
    checkpoint_path: str
    lang: Union[Literal["en"], Literal["vi"]]
    ai: bool
    vni_tones: bool
    strict_k: bool
    null_consonant: str
    end_of_rhyme: str
    
class PredictionState(BaseModel):
    raw: str = ""
    lst: List[Phrase] = []
    page: int = 0
    maxpage: int = 0
    buffer: List[Word] = []
    
    def reset(self):
        self.raw = ""
        self.lst = []
        self.page = 0
        self.maxpage = 0
        self.buffer = []
