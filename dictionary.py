from vietnamese import Vietnamese
import json
import copy
import time
import sys
import os
import utils
from functools import reduce
from itertools import product

class Dictionary():
    location = "<dictionary.Dictionary>"
    db = {} # database
    
    db = {consonant: {} for consonant in Vietnamese.consonant_families}
    for consonant in db.keys():
        if consonant == 'z':
            real_rhymes = Vietnamese.rhymes_families_with_gi.copy()
            real_rhymes[real_rhymes.index('')] = 'i'
            real_rhymes[real_rhymes.index('êng')] = 'iêng'
            real_rhymes[real_rhymes.index('ên')] = 'iên'
            real_rhymes[real_rhymes.index('n')] = 'in'
            db[consonant] = {rhyme: [] for rhyme in real_rhymes}
        else:
            db[consonant] = {rhyme: [] for rhyme in Vietnamese.rhymes_families}
    for consonant in db.keys():
        for rhyme in db[consonant].keys():
            _01234567_01234567 = Vietnamese.word_with_tones(consonant, rhyme)
            n_tones = len(_01234567_01234567[0])
            tone_obj = {}
            for t in range(n_tones):
                tt = []
                for _01234567 in _01234567_01234567:
                    tt.append(_01234567[t])
                tone_obj[t] = tt
            db[consonant][rhyme] = tone_obj
    
    db_freq = {}
    # db_freq = copy.deepcopy(db)
    # for consonant in db_freq.keys():
    #     for rhyme in db_freq[consonant].keys():
    #         for tone in db_freq[consonant][rhyme].keys():
    #             db_freq[consonant][rhyme][tone] = list(map(lambda word: {'value': word, 'freq': 0}, db[consonant][rhyme][tone]))
        
    dictionary = set()

    @staticmethod
    def get(crts: list[tuple[str, str|list[str], int]], max=25, freq_threshold=2) -> list[list[str]]:
        '''
        Return the word possibilities of each tuple given the list of tuple: `list[tuple[consonant: str, rhyme: str | list[str] | 'any', tone: str]]`
        
        `rhyme` can be one rhyme, or a list of rhymes, or `any` for all possible rhymes.
        
        Params:
        - `max`: n most frequently words per tuple (default is 25).
        - `freq_threshold`: just take the words that have frequency higher than or equal this threshold.
        '''
        words_possibilities = []
        for consonant, rhyme, tone in crts:
                    
            if consonant not in Vietnamese.consonant_families and tone not in Vietnamese.tones:
                return None
            
            if isinstance(rhyme, list) or rhyme == 'any':
                if rhyme == 'any':
                    rhymes = Vietnamese.rhymes_families
                else:
                    rhymes = rhyme
                possibilities = []
                for rh in rhymes:
                    try:
                        possibilities += Dictionary.db_freq[consonant][rh][tone]
                    except Exception:
                        pass
                
            else:
                if rhyme not in Vietnamese.rhymes_families:
                    return None
                try:
                    possibilities = Dictionary.db_freq[consonant][rhyme][tone]
                except Exception:
                    return None
                
                possibilities = sorted(possibilities, key=lambda word_obj: word_obj['freq'], reverse=True)
            
            # No possibilities
            if not possibilities:    
                return None
            
            # Filter out words that never appeared
            possibilities = list(filter(lambda word_obj: word_obj['freq'] >= freq_threshold, possibilities))
            # Sort by frequency
            possibilities = sorted(possibilities, key=lambda word_obj: word_obj['freq'], reverse=True)
                
            word_possibilities = [word_obj['value'] for word_obj in possibilities[:max]]
            words_possibilities.append(word_possibilities)
        
        return words_possibilities
    
    @staticmethod
    def predict(words_possibilities: list[list[str]], verbose=False, any=False) -> list[str]:
        '''
        May not optimized yet.
        Receive a list of word possibilities(`list[list[str]]`) and then make all n-gram combinations with the order of the list.
        
        Then filter out which combinations are in the dictionary.
        Set `any` to True will skip the filter part.
        '''
        if verbose:
            lens = []
            for word_possibilities in words_possibilities:
                lens.append(str(len(word_possibilities)))
            print('*'.join(lens))
        combinations = list(product(*words_possibilities))
        combinations = [' '.join(words) for words in combinations]

        if any:
            return combinations
        return list(filter(lambda comb: comb in Dictionary.dictionary, combinations))
    
    @staticmethod
    def update_db_freq(path):
        '''
        Please ignore this
        '''
        SAVE_PATH = os.path.join('checkpoints', 'db.json')
        LOG_PATH = os.path.join('checkpoints', 'db_update_log.txt')
        
        if os.path.isdir(path):
            file_paths = os.listdir(path)
        else:
            file_paths = [path]
            
        all_l = []
        all_total = []
        all_processed = []
            
        start_time = time.time()
        for file_path in file_paths:
            if not file_path.endswith(".txt"):
                continue
            
            file_path = os.path.join(path, file_path)
            total_lines = utils.count_lines(file_path)
            
            print(f'Processing on {file_path}...')
            with open(LOG_PATH, 'a') as f:
                f.write(f'Processing on {file_path}...')
            
            with open(file_path, 'r') as file:
                # Iterate over each line in the file
                l = 0
                total = 0
                processed = 0
                
                internal_start_time = time.time()
                
                for line in file:
                    # Process each line here
                    l += 1
                    line = utils.standardize_data(line)
                    
                    for word in line.split():
                        cf, rf, t = Vietnamese.analyze(word)
                        total += 1
                        if cf and not rf:
                            continue
                
                        else:
                            for word_obj in Dictionary.db_freq[cf][rf][t]:
                                if word_obj['value'] == word:
                                    word_obj['freq'] += 1
                            processed += 1
                    
                    if l % 50000 == 0:
                        processed_time = time.time() - start_time
                        internal_processed_time = time.time() - internal_start_time
                        with open(LOG_PATH, 'a') as f:
                            f.write(f'\n~~~~~~~~~~~~ {internal_processed_time:.2f}s :: {processed_time}s ~~~~~~~~~~~~~~~~~~~~\n')
                            f.write(f'Total     : {total}\n')
                            f.write(f'Processed : {processed}\n')
                            f.write(f'Speed: {total/internal_processed_time:.2f} word/s\n')
                            f.write(f'About: {100*l/total_lines:.2f} %\n')
                            f.write('~~~~~~~~~~~~~~~~~~~~~ saved checkpoint ~~~~~~~~~~~~~~~~~~\n')
                        print(f"est: {(total_lines-l)/(l/internal_processed_time)}s")
                        Dictionary.save_db_json(SAVE_PATH)
                
                all_l.append(l)
                all_total.append(total)
                all_processed.append(processed)
            
            print(f'DONE processing on {file_path}({time.time() - internal_start_time:.2f}s :: {time.time() - start_time:.2f}s )...')
        
        print(f"DONE ALL")
        print(f'Total lines: {sum(all_l)}')
        print(f'Total words: {sum(all_total)}')
        print(f'Total processed words: {sum(all_processed)}')
        print(f'Total time: {time.time() - start_time}s')
        

                    
    @staticmethod
    def save_db_json(path):
        '''
        Please ignore this
        '''
        with open(path, 'w') as f:
            json.dump(Dictionary.db_freq, f, indent=4)
            
    @staticmethod
    def update_dict():
        '''
        Please ignore this
        '''
        SAVE_PATH = os.path.join('checkpoints', 'dict.json')
        LOG_PATH = os.path.join('checkpoints', 'dict_update_log.txt')
        
        start_time = time.time()
        # text = utils.getVietnameseTextFrom_vndictyaml()
        # text = utils.standardize_data(text)
            
        # Dictionary.dictionary = set(
        #     text.splitlines()
        # )
        
        Dictionary.dictionary = set()
        with open('dictionaries/words.txt', 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                data = json.loads(line)
                text_value = data["text"]
                Dictionary.dictionary.add(text_value.lower())
                
                if i % 50000 == 0:
                    processed_time = time.time() - start_time
                    print(f'\n\n~~~ {processed_time:.2f}s ~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                    print(f'Speed: {i/processed_time:.2f} term/s')
                    print('~~~~~~~~~~~~~~~~~~~~~ saved checkpoint ~~~~~~~~~~~~~~~~~~\n')
                    Dictionary.save_dict_json()
            
        Dictionary.save_dict_json(SAVE_PATH)
        
    def reload(verbose=0):
        word_count = 0
        with open('checkpoints/db.json', 'r') as f:
            Dictionary.db_freq = json.load(f)
            for consonant in Dictionary.db_freq.keys():
                for rhyme in Dictionary.db_freq[consonant].keys():
                    Dictionary.db_freq[consonant][rhyme] = {int(k): v for k, v in Dictionary.db_freq[consonant][rhyme].items()}
                    word_count += len(Dictionary.db_freq[consonant][rhyme])
                    
        if verbose:
            print(f"{Dictionary.location} Loaded: {word_count} words")
        
        dictionary = []
        with open('checkpoints/dict.json', 'r') as f:
            dictionary = dictionary + json.load(f)
            
        if os.path.exists('checkpoints/common.json'):
            with open('checkpoints/common.json', 'r') as f:
                dictionary = dictionary + json.load(f)
            
        Dictionary.dictionary = set(dictionary)
        if verbose:
            print(f"{Dictionary.location} Loaded: {len(Dictionary.dictionary)} phrases")
            
        
    @staticmethod
    def save_dict_json(path):
        '''
        Please ignore this
        '''
        with open(path, 'w') as f:
            json.dump(list(Dictionary.dictionary), f, indent=4)
        
if __name__ == "__main__":
    '''
    Please ignore this, this is for updating db.json and dict.json from my private data folder.
    '''
    if len(sys.argv) < 3:
        pass
    else:
        if 'update' in sys.argv[1]:
            # Running big corpus to save the word database into a JSON file
            if 'freq' in sys.argv[2]:
                print('Running on text data to update db.json... Press control-C right now if you want to stop...')
                time.sleep(10)
                Dictionary.update_db_freq(os.path.join('data', 'news'))
                print('Done update db.json based on text data...')
            if 'dict' in sys.argv[2]:
                print('Running on text data to update dict.json... Press control-C right now if you want to stop...')
                time.sleep(10)
                Dictionary.update_dict()
                print('Done update dict.json based on text data...')
            
else: 
    Dictionary.reload(verbose=1)
    