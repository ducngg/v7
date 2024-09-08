from typing import List, Union, Literal, TypedDict
from .primitive import Triplet, RhymeFamily, Word

class MatchingTriplet(Triplet):
    rhyme: Union[List[RhymeFamily], Literal['any']]
    
    def unpack(self):
        return self.consonant, self.rhyme, self.tone

class WordFreq(TypedDict):
    value: Word
    freq: int
