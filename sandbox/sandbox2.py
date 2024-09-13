'''
This sandbox is for testing the functionality, don't need to care
'''
import sys, os, time, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.vietnamese import Vietnamese
import utils.preprocess as preprocess
import time


def main():
    # text = text1()
    # text = utils.separate_words(text.lower())
    
    # text = utils.getVietnameseTextFrom_vndictyaml()
    
    start_time = time.time()
    
    with open("data/corpus-title.txt", 'r') as file:
        # Iterate over each line in the file
        max_line = 1000000
        passed = 0
        total = 0
        diff = 0
        rarediff = 0
        l = 0
        for line in file:
            # Process each line here
            # if l > max_line:
            #     break
            
            for word in preprocess.seperate_words(line.strip().lower()):
                cf, rf, t = Vietnamese.analyze(word)
                total += 1
                if cf and not rf:
                    # print(f"Not Vietnamese: {word}")
                    continue
                vword = Vietnamese.synthesize(cf, rf, t)
        
                if word not in vword:
                    diff += 1
                    if rf in ['uy', 'oa', 'oe', 'oong']: # A lot of quý-quí, hóa-hoá, dọa-doạ -> not print
                        print('d', end=' ')
                    else:
                        rarediff += 1
                        print(f"\nRare diff: raw word: `{word}` | Syn(Ana(word)) `{vword}`")
                else:
                    passed += 1
                    # print('.', end='')
            
            l += 1
            if l % 50000 == 0:
                processed_time = time.time() - start_time
                print(f'\n\n~~~ {processed_time}s')
                print(f'Passed: {passed}')
                print(f'Differences: {diff}')
                print(f'Rare fifferences: {rarediff}')
                print(f'TotalW: {total}')
                print(f'Speed: {total/processed_time} word/s')
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

        processed_time = time.time() - start_time
        print(f'\nPassed: {passed}')
        print(f'Differences: {diff}')
        print(f'Rare fifferences: {rarediff}')
        print(f'TotalW: {total}')
        print(f'Speed: {total/processed_time} word/s')
        
def main2():
    for a, b in zip(Vietnamese.rhymes_families, Vietnamese.rhymes_families_with_other_consonants):
        if a != b:
            print(a, b)
            
def main3():
    with open("data/corpus-title.txt", 'r') as file:
        # Iterate over each line in the file
        max_lines = 50000
        words = []
        i = 0
        for line in file:
            words.extend(preprocess.seperate_words(line.strip().lower()))
            i += 1
            if i >= max_lines:
                break
        
        print(len(words))
        ns = [1, 10, 100, 1000, 10000, 100000, 100000, 100000, 100000, 100000]
        for n in ns:
            n_words = words[:n]
            
            start_time = time.time()
            crts = [Vietnamese.analyze(word) for word in n_words]
            total_time = time.time() - start_time
            
            print(f"{n:<10} -> Speed: {n/total_time/1000:.2f} ops/ms")
        
                

def main4():
    print(time.time())
    print(str(time.time()))
    
if __name__ == "__main__":
    main3()
    