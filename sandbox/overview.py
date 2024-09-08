import sys, os, time, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vietnamese import Vietnamese, Alphabet
from dictionary import Dictionary
import utils
import time
import numpy as np
import statistics
import json

def main():
    total_words = []
    replicate_sounds = 0
    none_sounds = 0
    
    Cs = len(Vietnamese.consonant_families)
    Rs = len(Vietnamese.rhymes_families)
    ERs = len(list(filter(lambda rhyme: rhyme[-1] in ['n', 'g', 'm', 'h'], Vietnamese.rhymes_families)))
    nERs = Rs - ERs
    print()
    print(f"Cs:    {Cs} (consonant families)")
    print(f"Rs:    {Rs} (rhyme families)")
    print(f"ERs:   {ERs} (enterable rhymes)")
    print(f"nERs:  {nERs} (non-enterable rhymes)")
    print()
    print(f"CERs:  {Cs*ERs*8}")
    print(f"CnERs: {Cs*nERs*6}")
    
    print()
    print(f"Loop for each consonant family and each rhyme family")
    # Count how many Vietnamese distinc words
    for c in Vietnamese.consonant_families:
        for r in Vietnamese.rhymes_families:
            wordss = Vietnamese.word_with_tones(c, r)
                
            if wordss is None:
                print(f"\tNone case:     ({c}, {r}) -> {wordss}")
                none_sounds += 8
                
                continue
            
            if len(wordss) > 1:
                print(f"\tMultiple case: ({c}, {r}) -> {wordss}")
                replicate_sounds += len(wordss[1])
            
            wordss = [word for words in wordss for word in words]
            total_words += wordss
    
    # total_words is sure distinct

    print()
    print(f"Total distict words:  {len(total_words)}")
    print(f"Total distict sounds: {len(total_words) - replicate_sounds}") # equal to Cs*ERs*8 + Cs*nERs*6 - none_sounds
    
    sounds = []
    with open("checkpoints/db.json", 'r') as f:
        db = json.load(f)
        for c in db:
            for r in db[c]:
                for t in db[c][r]:
                    sounds += [obj['value'] for obj in db[c][r][t]]
    
    enum = {}
    for no, sound in enumerate(sounds, start=1):
        enum[sound] = no
    # save enum to checkpoints/enum.json
    with open("checkpoints/enum.json", 'w') as f:
        json.dump(enum, f, indent=2)    
    
    # print('---')
    # for word in total_words:
    #     if word not in sounds:
    #         print(word)
    # print('---')
    # for word in sounds:
    #     if word not in total_words:
    #         print(word)
    # print('---')
        
                 
if __name__ == "__main__":
    main()
