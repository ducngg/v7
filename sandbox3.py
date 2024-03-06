from vietnamese import Vietnamese, Dictionary
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
    object_size = utils.get_object_size(Dictionary.db_freq)
    print(f"Size of Dictionary: {object_size/1024/1024:.2f} MB")
    print(f"len(db)          ~ {len(Dictionary.db_freq)}")
    print(f"len(db[c])       ~ {len(Dictionary.db_freq['0'])}")
    print(f"len(db[c][r])    ~ {len(Dictionary.db_freq['0']['an'])}")
    print(f"len(db[c][r][t]) ~ {len(Dictionary.db_freq['0']['an'][0])}")
    
    INPUT = ""
    while True:
        INPUT = input(">>> ")
        if INPUT == "quit()":
            break
        
        try:
            if len(INPUT.split()) == 3:
                c, r, t = INPUT.split()
                print(Dictionary.get(c, r, int(t)))
            elif len(INPUT.split()) == 2:
                c, t = INPUT.split()
                print(Dictionary.get(c, None, int(t), max=10))
            elif len(INPUT.split()) == 4:
                c1, t1, c2, t2 = INPUT.split()
                print(Dictionary.get(c1, None, int(t1), max=10))
                print(Dictionary.get(c2, None, int(t2), max=10))
        except Exception:
            pass
    
    

        
if __name__ == "__main__":
    main3()