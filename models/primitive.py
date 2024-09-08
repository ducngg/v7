from typing import List, Union, Literal, TypedDict
from pydantic import BaseModel

ConsonantFamily = str
RhymeFamily = str
Tone = int

Word = str
Phrase = str
    
class Triplet(BaseModel):
    """
    A tuple of Consonant, Rhyme, and Tone.
    This represent a sound (some words may have the same sound)
    """
    consonant: ConsonantFamily
    rhyme: RhymeFamily
    tone: Tone

    def unpack(self):
        return self.consonant, self.rhyme, self.tone
    def __iter__(self):
        return self.unpack()
    