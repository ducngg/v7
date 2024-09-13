import re
from functools import reduce
import sys

def seperate_words(paragraph):
    # Define the regular expression pattern to split the paragraph into words
    pattern = r'\b\w+\b'  # This pattern matches word boundaries (\b), followed by one or more word characters (\w+), and another word boundary (\b)

    # Use re.findall to extract all matching words from the paragraph
    words = re.findall(pattern, paragraph)
    return words

def getVietnameseTextFrom_vndictyaml(verbosity=0):
    '''
    Returns words seperated by \\n
    '''
    with open('dictionaries/vn.dict.yaml', 'r') as yaml:
        lines = yaml.readlines()[:]
        
        lines = [reduce(lambda word1, word2: word1 + ' ' + word2, line.split()[:int((len(line.split())) / 2)], ' ')
                for line in lines]
        
        text = reduce(lambda line1, line2: line1.strip().lower() + '\n' + line2.strip().lower(), lines)
        
        if verbosity >= 1:
            print(len(text))
            print(len(seperate_words(text)))

    return text

def get_object_size(obj):
    """
    Recursively calculate the total size of all nested objects.
    """
    # Initialize the size of the object
    total_size = sys.getsizeof(obj)
    
    # If the object is a list or a dictionary, recursively calculate the size of its elements
    if isinstance(obj, (list, dict)):
        for item in obj:
            total_size += get_object_size(obj[item]) if isinstance(obj, dict) else get_object_size(item)
    
    return total_size

# Hàm chuẩn hoá câu
def standardize_data(row):
    # Xóa dấu chấm, phẩy, hỏi ở cuối câu
    row = re.sub(r"[\.,\?]+$-", "", row)
    # Xóa tất cả dấu chấm, phẩy, chấm phẩy, chấm thang, ... trong câu
    row = row.replace(",", " ").replace(".", " ") \
        .replace(";", " ").replace("“", " ") \
        .replace(":", " ").replace("”", " ") \
        .replace('"', " ").replace("'", " ") \
        .replace("!", " ").replace("?", " ") \
        .replace("-", " ").replace("?", " ") \
        .replace("(", " ").replace(")", " ") \
        .replace("/", " ").replace("[", " ") \
        .replace("]", " ").replace("{", " ") \
        .replace("{", " ")
        
        
    row = row.strip().lower()
    return row

def count_lines(file_path):
    print(f'Reading {file_path}...')
    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count

def get_words_line_by_line(path):
    from .vietnamese import Vietnamese
    with open(path, 'r') as file:
        for line in file:
            line = standardize_data(line)
            words = []
            for word in line.split():
                cf, rf, t = Vietnamese.analyze(word)
                if rf is None:
                    continue
                else:
                    words.append(word)
            yield words

def get_line_by_line(path):
    with open(path, 'r') as file:
        for line in file:
            yield line
