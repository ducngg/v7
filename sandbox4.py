from ast import mod
from vietnamese import Vietnamese, Alphabet
from dictionary import Dictionary
from inputmethod import InputMethod
from model import MarkovModel
import utils
import time
import numpy as np
import statistics


def main():
    model = MarkovModel(checkpoint='model_threshold_6.json')
    object_size = utils.get_object_size(model.model)
    print(f"Size of model: {object_size/1024/1024:.2f} MB")
    object_size = utils.get_object_size(model.normalized_model)
    print(f"Size of normalized_model: {object_size/1024/1024:.2f} MB")
    
    print(model.top('anh', 10))
    print(model.top('tuấn', 10))
    print(model.top('tháng', 10))
    print(model.next('tôi', 100))
    
def main2():
    l = 0
    max_line = 100
    processed = 0
    start_time = time.time()
    for words in utils.get_words_line_by_line('data/fb_comment_10m'):
        # if l > max_line:
        #     break
        l += 1
        processed += len(words)
        if l % 10000 == 0:
            processed_time = time.time() - start_time
            
            print(f'\n\n~~~ {processed_time:.2f}s ~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(f'Line : {l}')
            print(f'Speed: {l/processed_time:.2f} lines/s')
            print(f'Processed : {processed}')
            print(f'Speed: {processed/processed_time:.2f} words/s')
            print('~~~~~~~~~~~~~~~~~~~~~ saved checkpoint ~~~~~~~~~~~~~~~~~~\n')
    
    print(l)
                 
def main3():
    l = 0
    max_line = 10
    processed = 0
    start_time = time.time()
    for line in utils.get_line_by_line('data/fb_comment_10m'):
        if l > max_line:
            break
        l += 1
        print(line)
    
    print(l)
                 
if __name__ == "__main__":
    main3()
