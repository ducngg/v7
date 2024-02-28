from vietnamese import Vietnamese
from long_text import *
import utils
    
rhymes = set()

text = utils.getVietnameseTextFrom_vndictyaml()

for word in utils.separate_words(text):
    cf, rf, t = Vietnamese.CRT(word.lower())
    if rf is not None:
        rhymes.add(rf)
    else:
        print(word)

print(len(rhymes))
print(len(Vietnamese.rhymes_families))

print(rhymes.issubset(Vietnamese.rhymes_families))

rhymes_set = Vietnamese.rhymes_families
for rhyme in rhymes:
    try:
        rhymes_set.remove(rhyme)
    except Exception:
        print(rhyme + " not found")

print(rhymes_set)

