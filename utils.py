import re
from functools import reduce

def separate_words(paragraph):
    # Define the regular expression pattern to split the paragraph into words
    pattern = r'\b\w+\b'  # This pattern matches word boundaries (\b), followed by one or more word characters (\w+), and another word boundary (\b)

    # Use re.findall to extract all matching words from the paragraph
    words = re.findall(pattern, paragraph)
    return words

def getVietnameseTextFrom_vndictyaml(verbosity=0):
    with open('dictionaries/vn.dict.yaml', 'r') as yaml:
        lines = yaml.readlines()[:]
        
        lines = [reduce(lambda word1, word2: word1 + ' ' + word2, line.split(' ')[:int((len(line.split(' '))) / 2)], ' ')
                for line in lines]
        
        text = reduce(lambda line1, line2: line1 + '\n' + line2, lines)
        
        if verbosity >= 1:
            print(len(text))
            print(len(separate_words(text)))

    return text