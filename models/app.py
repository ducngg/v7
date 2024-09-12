from typing import Union, Literal
from pydantic import BaseModel

class Args(BaseModel):
    lang: str = Union[Literal["en"], Literal["vi"]]
    ai: bool
    vni_tones: bool
    strict_k: bool
    null_consonant: str
    end_of_rhyme: str
