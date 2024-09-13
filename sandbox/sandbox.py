import sys, os, time, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.vietnamese import Vietnamese, Alphabet
from utils.dictionary import Dictionary
from imethod.v7 import InputMethod
import utils.preprocess as preprocess
import time
import numpy as np
import statistics


def main1():
    INPUT = ""
    while True:
        INPUT = input(">>> ")
        if INPUT == "quit()":
            break
        
        try:
            print(Vietnamese.synthesize(*INPUT.split(' ')))
        except Exception:
            pass
        
def main2():
    object_size = preprocess.get_object_size(Dictionary.db)
    print(f"Size of Dictionary: {object_size/1024/1024:.2f} MB")
    print(f"len(db)          ~ {len(Dictionary.db)}")
    print(f"len(db[c])       ~ {len(Dictionary.db['0'])}")
    print(f"len(db[c][r])    ~ {len(Dictionary.db['0']['an'])}")
    print(f"len(db[c][r][t]) ~ {len(Dictionary.db['0']['an'][0])}")

    print(Dictionary.db['k']['u'][4])
    print(Dictionary.db['k']['uông'][6])
    print(Dictionary.db['0']['iên'][1])
    print(Dictionary.db['0']['i'][1])
    print(Dictionary.db['z']['i'][2])
    print(Dictionary.db['ng']['iêm'][7])
    print(Dictionary.db['ng']['iêm'][5])
    print(Dictionary.db['z']['iên'][6])
    print(Dictionary.db['d']['iên'][7])
    print(Dictionary.db['k']['oeo'][5])
    print(Dictionary.db['k']['oang'][0])
    print(Dictionary.db['k']['uông'][2])
    print(Dictionary.db['g']['i'][2])
    print(Dictionary.db['z']['ăng'][7])
    print(Dictionary.db['g']['i'][2])
    print(Dictionary.db['kh']['ung'][3])
    print(Dictionary.db['ng']['ênh'][2])
    print(Dictionary.db['h']['oang'][3])
    print(Dictionary.db['x']['uân'][6])
    print(Dictionary.db['kh']['uênh'][2])
    print(Dictionary.db['kh']['uênh'][7])
    print(Dictionary.db['kh']['uênh'][6])
    print(Dictionary.db['k']['oai'][1])
    print(Dictionary.db['k']['ưu'][3])
    print()
    [print(Dictionary.db[c]['i'][0]) for c in Vietnamese.consonant_families]
    
    print(Dictionary.db['đ']['uôi'][3])
    print(Vietnamese.synthesize('đ', 'uôi', 3))
    print(Vietnamese.analyze('đuổi'))

 
def main22():
    object_size = preprocess.get_object_size(Dictionary.db)
    print(f"Size of Dictionary: {object_size/1024/1024:.2f} MB")
    print(f"len(db)          ~ {len(Dictionary.db)}")
    print(f"len(db[c])       ~ {len(Dictionary.db['0'])}")
    print(f"len(db[c][r])    ~ {len(Dictionary.db['0']['an'])}")
    print(f"len(db[c][r][t]) ~ {len(Dictionary.db['0']['an'][0])}")

    print(Vietnamese.synthesize('k', 'u', 4))
    print(Vietnamese.synthesize('k', 'uông', 6))
    print(Vietnamese.synthesize('0', 'iên', 1))
    print(Vietnamese.synthesize('0', 'i', 1))
    print(Vietnamese.synthesize('z', 'i', 2))
    print(Vietnamese.synthesize('ng', 'iêm', 7))
    print(Vietnamese.synthesize('ng', 'iêm', 5))
    print(Dictionary.db['z']['iên'][6])
    print(Dictionary.db['d']['iên'][7])
    print(Dictionary.db['k']['oeo'][5])
    print(Dictionary.db['k']['oang'][0])
    
    print(Dictionary.db['g']['i'][2])
    print(Dictionary.db['z']['ăng'][7])
    print(Dictionary.db['g']['i'][2])
    print(Dictionary.db['kh']['ung'][3])
    print(Dictionary.db['ng']['ênh'][2])
    print(Dictionary.db['h']['oang'][3])
    print(Dictionary.db['x']['uân'][6])
    print(Dictionary.db['kh']['uênh'][2])
    print(Dictionary.db['kh']['uênh'][7])
    print(Dictionary.db['kh']['uênh'][6])
    print(Dictionary.db['k']['oai'][1])
    print(Dictionary.db['k']['ưu'][3])
    for c in Vietnamese.consonant_families:
        print(Dictionary.db[c]['i'][0])
        

def main3():
    print(f"Size of Dictionary.db_freq    : {preprocess.get_object_size(Dictionary.db_freq)/1024/1024:.2f} MB")
    print(f"Size of Dictionary.db         : {preprocess.get_object_size(Dictionary.db)/1024/1024:.2f} MB")
    print(f"Size of Dictionary.dictionary : {preprocess.get_object_size(Dictionary.dictionary)/1024/1024:.2f} MB")
    inputAgent = InputMethod()
    INPUT = ""
    while True:
        INPUT = input(">>> ")
        if INPUT == "quit()":
            break
        
        try:
            print(inputAgent.predict(INPUT))
        except Exception:
            pass
    
def main4():
    phrases = list(Dictionary.dictionary)
    original_lens = []
    v7_lens = []
    for phrase in phrases[:]:
        phrase_len = len(phrase)
        v7_len = 0
        viet = True
        
        words = phrase.split()
        if len(words) == 1:
            continue
        
        phrase_len += len(words) * 1.2 # average 1.2 more key for each words
        
        for word in words:
            c, v, t = Vietnamese.analyze(word)
            if v is None:
                viet = False
            else:
                v7_len += len(c) + 1 # one for tone
                
        if not viet:
            continue
        
        v7_len += 1 # one for choosing
        # print(phrase_len, phrase)
        # print(v7_len)
        
        original_lens.append(phrase_len)
        v7_lens.append(v7_len)
        
    # print(original_lens, v7_lens)
    
    percents = [(o-v)/o*100 for o, v in zip(original_lens, v7_lens)]
    import statistics
    # print(percents)
    print()
    print(statistics.mean(percents))
    print(statistics.stdev(percents))

def main5():
    rand_cons = lambda: np.random.choice(Vietnamese.consonant_families)
    rand_vowl = lambda: np.random.choice(Alphabet.VOWELS + ['', ''])
    rand_tone = lambda: str(np.random.choice(Vietnamese.tones))
    rand_len = lambda: np.random.randint(1,4)
    
    inputAgent = InputMethod()
    RAWS = []
    RESS = []
    TIME = []
    
    for i in range(1000):
        raw = ''
        l = rand_len()
        for _ in range(l):
            c = rand_cons()
            if c == '0':
                continue
            if c == 'đ':
                c = 'dd'
            raw += c + rand_tone()
        
        if raw == '':
            continue
        
        start_time = time.time()
        
        phrase = inputAgent.predict(raw)[0]
        TIME.append((l, time.time() - start_time))
        RAWS.append(raw)
        RESS.append(phrase)
        
        if i % 10000 == 0 and i > 100:
            TIME1 = [t[1] for t in TIME if t[0] == 1]
            TIME2 = [t[1] for t in TIME if t[0] == 2]
            TIME3 = [t[1] for t in TIME if t[0] == 3]
            
            print(f'Len=1: Mean: {statistics.mean(TIME1):.5f}             Std:{statistics.stdev(TIME1):.5f}    ({len(TIME1)} records) {i}')
            print(f'Len=2: Mean: {statistics.mean(TIME2):.5f}             Std:{statistics.stdev(TIME2):.5f}    ({len(TIME2)} records)')
            print(f'Len=3: Mean: {statistics.mean(TIME3):.5f}             Std:{statistics.stdev(TIME3):.5f}    ({len(TIME3)} records)')
        
def main6():
    inputAgent = InputMethod()
    print(inputAgent.predict('xi0chao2mo5ng2'))
    print(inputAgent.predict('xi0chao2mo')) # Not completed
    print(inputAgent.predict('ximg0ch2')) # No match (`ximg`)
    print(inputAgent.predict('xi0')) # Exact match when predict just one word
    print(inputAgent.predict('b7')) # Wildcard rhyme
    print(inputAgent.predict('b7t2'))
    print(inputAgent.predict('ba7ti2'))
    print(inputAgent.predict('bac7ti2'))
    
def main7():
    print(Dictionary.get([('0', 'any', 0)], max=50))
if __name__ == "__main__":
    main7()
