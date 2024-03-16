from vietnamese import Vietnamese, Alphabet
from dictionary import Dictionary

import re

class InputMethod():
    def __init__(self, flexible_tones=False, strict_k=False) -> None:
        
        self.flexible_tones = flexible_tones        # Accute for both tone 1 and 6, underdot for both tone 5 and 7
        self.strict_k = strict_k

    def parse(self, cvt: str) -> tuple[str, list[str], int]:
        '''
        A recognizer for input string(cvt). Recognizes 3 parts in the string: consonant, rhyme, and tone. The input string can 
        have no rhyme part, in this case rhymes will be all the rhymes in Vietnamese.rhyme_families (wildcard).
        
        Return a tuple of `(consonant, [rhymes], tone)`.
        '''
        cvt = cvt.lower()
        # CHECK TONE
        try:
            tone = int(cvt[-1])
            if tone not in Vietnamese.tones:
                return None
            #
            # Add if tone == 6, 7 for flexible-tones
            #
        except Exception:
            return None
        
        # CHECK CONSONANT        
        # Check if consonant is double consonant
        consonant = cvt[:2]
        rhyme_pos = 2
        if consonant not in Vietnamese.consonant_families + ['dd']:
            # Check if consonant is single consonant
            consonant = cvt[:1]
            rhyme_pos = 1
            if consonant not in Vietnamese.consonant_families + ['c', 'q']:
                consonant = None
                rhyme_pos = 0
        
        if consonant in ['c', 'q']:
            if self.strict_k:
                return None
            consonant = 'k'
            
        if consonant in ['dd']:
            consonant = 'đ'
            
        # CHECK RHYME
        rhymes = self.rhymeRecognizer(cvt[rhyme_pos:-1])
        
        if consonant is None and rhymes:
            consonant = '0'
            
        return consonant, rhymes, tone

    
    def rhymeRecognizer(self, rh) -> list[str]:
        '''
        Return the rhymes that match the rhyme part(rh).
        '''
        possibilities = Vietnamese.rhymes_families.copy()
        # If no vowel -> any
        if not rh:
            return possibilities
        
        #TODO: Recognizer for faster typing like {mj -> manh / minh, ty -> toi, tai, tui...}
        if rh[0] not in Alphabet.VOWELS_Y:
            return []
        
        for idx, char in enumerate(rh):
            possibilities = list(filter(
                lambda rhyme: len(rhyme) > idx and self.match(rhyme[idx], char),
                possibilities
            ))
            
        return possibilities
    
    def match(self, target, char):
        if char == 'a':
            return True if target in ['a', 'ă', 'â'] else False
        if char == 'e':
            return True if target in ['e', 'ê'] else False
        if char == 'i':
            return True if target in ['i'] else False
        if char == 'o':
            return True if target in ['o', 'ô', 'ơ'] else False
        if char == 'u':
            return True if target in ['u', 'ư'] else False

        # uyen: y<->y
        # yen: i<->y
        if char == 'y':
            return True if target in ['i', 'y'] else False
        
        return target == char
        
        
    def seperate_raws(self, raws: str):
        '''
        Seperate raw string of many input string to blocks. The tone number will be the seperator, and belong to the prior term.
        eg. x0chao2m5ngu -> ['x0', 'chao2', 'm5', 'ngu']
        '''
        pattern = r'[a-zA-Z]+(?:\d|$)'
        raws = re.findall(pattern, raws)
        return raws
        
    def predict(self, input_string):
        '''
        Main function of the class, from a raw input string to a prediction list of combinations. Any errors occur will return None.
        '''
        raws = self.seperate_raws(input_string)
        CVsTs = [self.parse(raw) for raw in raws]
        
        # If any is None then return
        if any(list(map(lambda x: not x, CVsTs))):
            return None
        
        if len(CVsTs) == 0:
            return None
        # User may wants to input a word that doesn't exist in the dictionary 0 -> set freq_threshold=0
        elif len(CVsTs) == 1:
            #TODO: If rhyme is not wildcard -> must be exact match: cho1 -> chó/chớ/chố instead of showing chóng/chớm...
            # if len(CVsTs[0][1]) != len(Vietnamese.rhymes_families):
                
            combination_possibilities = Dictionary.get(CVsTs, max=9, freq_threshold=0)[0]
        else:
            words_possibilities = Dictionary.get(CVsTs, max=50)
            combination_possibilities = Dictionary.predict(words_possibilities)
        
        return combination_possibilities