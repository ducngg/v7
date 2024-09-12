from typing import List, Union, Literal, TypedDict
from .primitive import Triplet, ConsonantFamily, RhymeFamily, Word

class MatchingTriplet(Triplet):
    consonant: Union[ConsonantFamily, Literal['q'], Literal['c']]
    rhyme: Union[List[RhymeFamily], Literal['any']]
    
    def unpack(self):
        return self.consonant, self.rhyme, self.tone

class WordFreq(TypedDict):
    value: Word
    freq: int
