from inputmethod import InputMethod, TelexOrVNI, V7
from vietnamese import Vietnamese
from dictionary import Dictionary

from functools import reduce
import statistics

def main1():
    corpus = "kiểm soát phối hợp tra cứu trực tiếp trên máy tính để phát hiện phương tiện vi phạm qua hình ảnh mà đã có thông báo chưa đến nộp phạt thì tổ tra cứu sẽ thông báo"

    # Analyze each word in the corpus
    for word in corpus.split(' '):
        print(word, TelexOrVNI.get_keys_needed_from_word(word), V7.get_keys_needed_from_word(word))
        
def compare():
    samples = list(Dictionary.dictionary)[:]
    len_samples = len(samples)
    records = []
    records_len_1 = []
    records_len_2 = []
    records_len_3 = []
    records_len_4 = []
    for idx, phrase in enumerate(samples, 1):
        words = phrase.split()
        # print(phrase)
        try:
            if len(words) == 1:
                total_v7_method = V7.get_least_from_words(words) + 1 + 1 # +1 page because many words appear, +1 for choosing key
            else:
                total_v7_method = V7.get_least_from_words(words) + 1 # +1 for choosing key
        except Exception:
            continue
            
        total_other_input_method = 0
        # total_other_input_method += len(words) - 1 # spaces
        
        for word in words:
            total_other_input_method += TelexOrVNI.get_keys_needed_from_word(word)
            
        records.append((phrase, total_other_input_method, total_v7_method))
        if len(words) == 1:
            records_len_1.append((phrase, total_other_input_method, total_v7_method))
        elif len(words) == 2:
            records_len_2.append((phrase, total_other_input_method, total_v7_method))
        elif len(words) == 3:
            records_len_3.append((phrase, total_other_input_method, total_v7_method))
        else:
            records_len_4.append((phrase, total_other_input_method, total_v7_method))
            
        print(f'\r{idx}/{len_samples}', end='')
        
    diffs = [other - v7 for _, other, v7 in records]
    faster_rate = [(other - v7)/other for _, other, v7 in records]
    
    diffs_len_1 = [other - v7 for _, other, v7 in records_len_1]
    faster_rate_len_1 = [(other - v7)/other for _, other, v7 in records_len_1]
    diffs_len_2 = [other - v7 for _, other, v7 in records_len_2]
    faster_rate_len_2 = [(other - v7)/other for _, other, v7 in records_len_2]
    diffs_len_3 = [other - v7 for _, other, v7 in records_len_3]
    faster_rate_len_3 = [(other - v7)/other for _, other, v7 in records_len_3]
    diffs_len_4 = [other - v7 for _, other, v7 in records_len_4]
    faster_rate_len_4 = [(other - v7)/other for _, other, v7 in records_len_4]
    
    print()
    print(f'Diff all        mean: {statistics.mean(diffs)}' f'std:  {statistics.stdev(diffs)}')
    print(f'Faster rate all mean: {statistics.mean(faster_rate)}' f'std:  {statistics.stdev(faster_rate)}')
    print(f'LEN1 Diff all        mean: {statistics.mean(diffs_len_1)}' f'std:  {statistics.stdev(diffs_len_1)}')
    print(f'LEN1 Faster rate all mean: {statistics.mean(faster_rate_len_1)}' f'std:  {statistics.stdev(faster_rate_len_1)}')
    print(f'LEN2 Diff all        mean: {statistics.mean(diffs_len_2)}' f'std:  {statistics.stdev(diffs_len_2)}')
    print(f'LEN2 Faster rate all mean: {statistics.mean(faster_rate_len_2)}' f'std:  {statistics.stdev(faster_rate_len_2)}')
    print(f'LEN3 Diff all        mean: {statistics.mean(diffs_len_3)}' f'std:  {statistics.stdev(diffs_len_3)}')
    print(f'LEN3 Faster rate all mean: {statistics.mean(faster_rate_len_3)}' f'std:  {statistics.stdev(faster_rate_len_3)}')
    print(f'LEN4+ Diff all        mean: {statistics.mean(diffs_len_4)}' f'std:  {statistics.stdev(diffs_len_4)}')
    print(f'LEN4+ Faster rate all mean: {statistics.mean(faster_rate_len_4)}' f'std:  {statistics.stdev(faster_rate_len_4)}')
    
    
if __name__ == '__main__':
    compare()
    