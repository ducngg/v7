from vietnamese import Vietnamese, Dictionary, InputMethod
from long_text import *
import utils


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
    object_size = utils.get_object_size(Dictionary.db)
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
        

def main3():
    print(f"Size of Dictionary.db_freq    : {utils.get_object_size(Dictionary.db_freq)/1024/1024:.2f} MB")
    print(f"Size of Dictionary.db         : {utils.get_object_size(Dictionary.db)/1024/1024:.2f} MB")
    print(f"Size of Dictionary.dictionary : {utils.get_object_size(Dictionary.dictionary)/1024/1024:.2f} MB")
    inputAgent = InputMethod()
    INPUT = ""
    while True:
        INPUT = input(">>> ")
        if INPUT == "quit()":
            break
        
        try:
            INPUTS = INPUT.split()
            INPUTS = [inputAgent.rawToCVT(inp) for inp in INPUTS]
            words_possibilities = Dictionary.get(INPUTS, max=50)
            # print(words_possibilities)
            print(Dictionary.predict(words_possibilities))
        except Exception:
            pass
    
        
if __name__ == "__main__":
    main3()
