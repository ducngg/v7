'''
This sandbox is for testing the functionality, don't need to care
'''
from vietnamese import Vietnamese
from long_text import *
import utils
    
rhymes = set()

text = utils.getVietnameseTextFrom_vndictyaml()

for word in utils.separate_words(text):
    cf, rf, t = Vietnamese.CRT(word.lower())
    if rf is not None:
        # if rf == 'uym':
        #     print(word)
        rhymes.add(rf)
        # print(f'{word} -> {cf, rf, t}')
    else:
        print(word, end=' ')
        pass
        

print(len(rhymes))
print(len(Vietnamese.rhymes_families))

print(rhymes.issubset(Vietnamese.rhymes_families))

rhymes_set = Vietnamese.rhymes_families.copy()
for rhyme in rhymes:
    try:
        rhymes_set.remove(rhyme)
    except Exception:
        print(rhyme + " not found")

print(rhymes_set)

print(Vietnamese.analyze('quỉn'))