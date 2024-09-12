from typing import Union, Literal
from .primitive import ConsonantFamily, Triplet
    
Raw = str # Looks like `v7` / `ho2` / 'tie1` / 'a1', ...

class RawTriplet(Triplet):
    consonant: Union[ConsonantFamily, Literal['q'], Literal['c'], Literal['']]
    rhyme: Union[str, Literal['']]
    
    def unpack(self):
        return self.consonant, self.rhyme, self.tone
