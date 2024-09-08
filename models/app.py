from typing import Union, Literal
from pydantic import BaseModel

class Args(BaseModel):
    lang: str = Union[Literal["en"], Literal["vi"]]
    ai: bool
    flexibletones: bool
