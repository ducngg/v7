'''
This sandbox is for testing the functionality, don't need to care
'''
from vietnamese import Vietnamese
import utils
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
            
            for word in utils.separate_words(line.strip().lower()):
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
    ...
    
if __name__ == "__main__":
    main2()
    