from typing import List, Tuple, Optional, Union, Literal, TypedDict
from pydantic import BaseModel
from .primitive import Triplet
    
Raw = str # Looks like `v7` / `ho2` / 'tie1`, ...

class RawTriplet(Triplet):
    rhyme: Union[str, Literal['']]
    
    def unpack(self):
        return self.consonant, self.rhyme, self.tone
