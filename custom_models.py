from typing import List, Tuple, Optional, Union, Literal
from pydantic import BaseModel

class Args(BaseModel):
    lang: str = Union[Literal["en"], Literal["vi"]]
    ai: bool
    
class CRT(BaseModel):
    consonant: str
    rhyme: str
    tone: int
