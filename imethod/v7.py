from utils.vietnamese import Vietnamese, Alphabet
from utils.dictionary import Dictionary

import re
from typing import List, Optional
from models import RhymeFamily, RawTriplet, Raw, MatchingTriplet, Word, Phrase

class InputMethod():
    location = "<imethod.v7.InputMethod>"
    def __init__(
        self, 
        *, 
        vni_tones=False, 
        strict_k=False, 
        null_consonant='hh', 
        end_of_rhyme='.'
    ) -> None:
        self.mode = "[Dictionary]"
        self.vni_tones = vni_tones        # Accute for both tone 1 and 6, underdot for both tone 5 and 7
        self.strict_k = strict_k
        self.null_consonant = null_consonant # Currently support 1 or 2 character only.
        self.end_of_rhyme = end_of_rhyme # `co5ve4tr0` cannot yields `cọ vẽ tranh`, and it`s impossible to type `cọ vẽ tranh` using CASE 4 typing because `cọ` is not frequently used. `end_of_rhyme` is created to fix this: `co{EOR}5ve4tr0`'. Currently support 1 character only.
        
    def parse(self, crt: Raw) -> RawTriplet:
        '''
        A recognizer for input string(cvt). Recognizes 3 parts in the string: consonant, rhyme, and tone. 
        Return a tuple of `(consonant_part, rhyme_part, tone_part)`.
        '''
        crt = crt.lower()
        # CHECK TONE
        try:
            tone = int(crt[-1])
            if tone not in Vietnamese.tones:
                return None
            #
            # TODO: Add if tone == 6, 7 for vni_tones
            #
        except Exception:
            return None
        
        # CHECK CONSONANT   
        # Check if null consonant is used
        if crt[:2] == self.null_consonant: consonant, rhyme_pos = self.null_consonant, 2
        elif crt[:1] == self.null_consonant: consonant, rhyme_pos = self.null_consonant, 1
        else:   
            # Check if consonant is double consonant
            consonant = crt[:2]
            rhyme_pos = 2
            if consonant not in Vietnamese.consonant_families + ['dd']:
                # Check if consonant is single consonant
                consonant = crt[:1]
                rhyme_pos = 1
                if consonant not in Vietnamese.consonant_families + ['c', 'q']:
                    consonant = ''
                    rhyme_pos = 0
                
        # CHECK RHYME
        rhyme = crt[rhyme_pos:-1]
        
        return RawTriplet(consonant=consonant, rhyme=rhyme, tone=tone)

    def find(self, raw_triplet: RawTriplet) -> MatchingTriplet:
        '''
        Receive 3 parts of the raw: consonant, rhyme, and tone. Rhyme part can be empty, in this case rhymes will be all the rhymes in Vietnamese.rhyme_families (wildcard).
        
        Return a `MatchingTriplet`.
        '''
        IS_Q_CASE = False
        if not raw_triplet:
            return None
        
        consonant, rhyme, tone = raw_triplet.unpack()
        
        if consonant in ['c', 'q']:
            if self.strict_k:
                return None
            # User may input qua/que instead of coa/coe -> replace `u` to `o`
            if consonant == 'q':
                IS_Q_CASE = True
                        
        if consonant in ['dd']:
            consonant = 'đ'
        if consonant in ['', self.null_consonant]:
            consonant = '0'
            
        # CHECK RHYME
        rhymes = self.rhymeRecognizer(rhyme, IS_Q_CASE)
        
        if not rhymes:
            return None
        
        return MatchingTriplet(consonant=consonant, rhyme=rhymes, tone=tone)
    
    def rhymeRecognizer(self, raw_rhyme: str, is_q_case = False) -> List[RhymeFamily]:
        '''
        Return the rhymes that match the rhyme part(rh).
        '''
        if is_q_case:
            possibilities = Vietnamese.rhymes_families_with_q.copy()
        else:
            possibilities = Vietnamese.rhymes_families.copy()
        
        # If no vowel -> any
        if not raw_rhyme:
            if is_q_case:
                possibilities = list(map(
                    lambda rhyme: rhyme.replace('ua', 'oa').replace('uă' ,'oă').replace('ue', 'oe'),
                    possibilities
                ))
                
            return possibilities
        
        # TODO: Recognizer for faster typing like {mj -> manh / minh, ty -> toi, tai, tui...}
        if raw_rhyme[0] not in Alphabet.VOWELS_Y:
            return []
        
        # Entering final consonants to original final consonant
        raw_rhyme = raw_rhyme.replace('t', 'n').replace('ch', 'nh').replace('c', 'ng').replace('p', 'm')
        
        for idx, char in enumerate(raw_rhyme):
            if char == self.end_of_rhyme:
                possibilities = list(filter(
                    lambda rhyme: len(rhyme) == idx,
                    possibilities
                ))
                break
            else:
                possibilities = list(filter(
                    lambda rhyme: len(rhyme) > idx and self.match(rhyme[idx], char),
                    possibilities
                ))
        
        if is_q_case and len(raw_rhyme) >= 2 and raw_rhyme[1] in ['a', 'e']: # see Vietnamese.rhymes_families_with_q
            possibilities = list(map(
                lambda rhyme: rhyme.replace('ua', 'oa').replace('uă' ,'oă').replace('ue', 'oe'),
                possibilities
            ))
            
        return possibilities
    
    def match(self, target: str, char: str):
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
        
    def seperate_raws(self, raws: str) -> List[Raw]:
        '''
        Seperate raw string of many input string to blocks. The tone number will be the seperator, and belong to the prior term.
        eg. x0chao2m5ngu -> ['x0', 'chao2', 'm5', 'ngu']
        '''
        pattern = r'[a-zA-Z{}]+(?:\d|$)'.format(re.escape(self.end_of_rhyme))
        raws = re.findall(pattern, raws)
        return raws
    
    def apply_capitalization(self, words: Phrase, cap_pos: List[bool]) -> Phrase:
        words = words.split()
        return ' '.join([word.capitalize() if cap else word for word, cap in zip(words, cap_pos)])
        
    def get(self, triplets: List[MatchingTriplet], max=25, freq_threshold=2):
        '''
        Use Dictionary.get() with self configurations. 
        '''      
        # If strict_k then we don't need to care
        if self.strict_k:
            words_possibilities = Dictionary.get(triplets, max=max, freq_threshold=freq_threshold)
            return words_possibilities
        # If not -> Just take the words that start with original `consonant` in crts
        else:
            query_triplets: List[MatchingTriplet] = []
            for triple in triplets:
                c, rs, t = triple.unpack()
                if c in ['c', 'q', 'k']:
                    query_c = 'k'
                else:
                    query_c = c
                query_triplets.append(MatchingTriplet(consonant=query_c, rhyme=rs, tone=t))
            words_possibilities = Dictionary.get(query_triplets, max=max, freq_threshold=freq_threshold)
            if words_possibilities is None:
                return None

            final_words_possibilities: List[List[Word]] = []
            for word_possibilities, triplet in zip(words_possibilities, triplets):
                c, rs, t = triplet.unpack()
                if c in ['c', 'q', 'k']:
                    word_possibilities = list(filter(lambda word: word[0] == c, word_possibilities))
                    # CASE 4 can make this list empty because `max` is very low -> Query again with high `max`
                    if not word_possibilities:
                        word_possibilities = Dictionary.get([MatchingTriplet(consonant='k', rhyme=rs, tone=t)], max=50, freq_threshold=0)[0]
                        word_possibilities = list(filter(lambda word: word[0] == c, word_possibilities))[:max]
                final_words_possibilities.append(word_possibilities)
                
            return final_words_possibilities
    
    def predict(self, input_string: str, **kwargs) -> List[Phrase]:
        '''
        Main function of the class, from a raw input string to a prediction list of combinations. Any errors occur or invalid raw string will return None.
        
        There are 4 case of inputs that result in different predictions.
        - Case 1: Just one raw, wildcard rhyme: Predict all rhymes with descending frequency.
            - eg. `th3` -> [`thủ`, `thể`, `thủy`, ...]
                - Complexity = max=100 ~ O(1)
        - Case 2: Just one raw, provided rhyme: Result will be the exact word with provided (c,v,t). (Don't need to be in the dictionary)
            - eg. `co1` -> [`có`, `cố`, `cớ`] (instead of showing others like `cốm`, `cống`, ...)
                - Complexity = max=100 (+ max=default)? ~ O(1)
        - Case 3: Multiple raws (<=3), have the phrases with that pattern in the dictionary: Result will be those phrases. If no phrases with that pattern in the dictionary, switch to Case 4.
            - eg. `t3k6` -> [`tổng kết`, `tổng quát`, `tổ quốc`, `tẩm quất`] (strict_k=True)
                - Complexity = (max=50)**n (+ (max=5|3|2)**n)? ~ O(50^n): n<=3
        - Case 4: Multiple raws (>3) or unrecognized Case 3: Result will be the most frequent words of each raw combined.
            - eg. `thu6dde0` -> [`thức đêm`, `thức đen`, `thuốc đêm`, `thuốc đen`] (Note that all of the words are most frequent used words)
                - Complexity = (max=2)**n ~ O(2^n)
        '''
        raws = self.seperate_raws(input_string)
        cap_pos = [raw[0].isupper() for raw in raws]
        
        raws_parts = [self.parse(raw.lower()) for raw in raws]
        CRsTs = [self.find(raw_parts) for raw_parts in raws_parts]
                
        # Return None if any is None (failed to find consonant/rhymes/tone)
        if any(list(map(lambda x: not x, CRsTs))):
            return None
        
        if len(CRsTs) == 0:
            return None
        
        elif len(CRsTs) == 1:
            raw_c, raw_r, _ = raws_parts[0].unpack()
            c, rs, t = CRsTs[0].unpack()
                        
            # NOTE: Case 1: Wildcard rhyme
            if raw_r == '':
                # Set high max because when filter out `c`, `q`, `k`, the list may return less than 9 words.
                combination_possibilities = self.get(CRsTs, max=100)[0]
                
            # NOTE: Case 2: User may wants to input a word that doesn't exist in the dictionary 0 -> set freq_threshold=0
            else:
                # Must be exact rhyme -> case user input `-c`, the final rhyme is `-ng`
                coequal_rs = list(filter(lambda rhyme: 
                    len(rhyme) == len(raw_r) if raw_r[-1] != 'c' else len(rhyme) == len(raw_r) + 1, 
                    rs
                ))
                
                # If user input something like hie2/cu6, there will be no combination_possibilities associated with `coequal_rs``, then just use `rs`.
                combination_possibilities = self.get([MatchingTriplet(consonant=c, rhyme=coequal_rs, tone=t)], max=100, freq_threshold=0) # This may return None

                if not combination_possibilities:
                    combination_possibilities = self.get([MatchingTriplet(consonant=c, rhyme=rs, tone=t)], freq_threshold=0)
                
                combination_possibilities = combination_possibilities[0]
            
        else:
            combination_possibilities = None
            
            if len(CRsTs) == 2:
                # NOTE: Case 3.1:
                words_possibilities = self.get(CRsTs, max=100)
                combination_possibilities = Dictionary.predict(words_possibilities)
            elif len(CRsTs) == 3:
                # NOTE: Case 3.2:
                words_possibilities = self.get(CRsTs, max=50)
                combination_possibilities = Dictionary.predict(words_possibilities)
                                
            if not combination_possibilities:
            # NOTE: Case 4:
            # If no combination_possibilities, get `max` most frequent words of each raw string to produce.
            # In this case, user should provide as much information as possible in the raw string to get best result.
                n_terms = len(CRsTs)
                if n_terms == 2: max = 5
                elif n_terms == 3: max = 3
                else: max = 2
                words_possibilities = self.get(CRsTs, max=max, freq_threshold=0)
                combination_possibilities = Dictionary.predict(words_possibilities, any=True)
        
        if not any(cap_pos):
            return combination_possibilities
        else:
            return [self.apply_capitalization(combination, cap_pos) for combination in combination_possibilities]

