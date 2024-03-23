from inputmethod import InputMethod
from vietnamese import Vietnamese
from dictionary import Dictionary

from functools import reduce
import statistics


class TelexOrVNI():
    '''
    For comparison, not for use!
    '''
    keys_needed_rhyme_family = {
        'a': 1,
        'an': 2,
        'anh': 3,
        'ang': 3,
        'am': 2,
        'ăn': 3,
        'ăng': 4,
        'ăm': 3,
        'ân': 3,
        'âng': 4,
        'âm': 3,
        'e': 1,
        'en': 2,
        'eng': 3,
        'em': 2,
        'ê': 2,
        'ên': 3,
        'ênh': 4,
        'êm': 3,
        'i': 1,
        'in': 2,
        'inh': 3,
        'im': 2,
        'o': 1,
        'on': 2,
        'ong': 3,
        'om': 2,
        'ô': 2,
        'ôn': 3,
        'ông': 4,
        'ôm': 3,
        'ơ': 2,
        'ơn': 3,
        'ơm': 3,
        'u': 1,
        'un': 2,
        'ung': 3,
        'um': 2,
        'ư': 2,
        'ưn': 3,
        'ưng': 4,
        'ưm': 3,
        'ai': 2,
        'ay': 2,
        'ây': 3,
        'oi': 2,
        'ôi': 3,
        'ơi': 3,
        'ui': 2,
        'ưi': 3,
        'oa': 2, ## q -> 1
        'oan': 3,
        'oanh': 4,
        'oang': 4,
        'oam': 3,
        'oăn': 4,
        'oăng': 5,
        'oăm': 4,
        'uân': 4,
        'uâng': 5,
        'oe': 2,
        'oen': 3,
        'uê': 3,
        'uên': 4,
        'uênh': 5, 
        'uy': 2,
        'uyn': 3,
        'uynh': 4,
        'uym': 3,
        'ua': 2,
        'uôn': 4,
        'uông': 5,
        'uôm': 4,
        'uơ': 3,
        'uơn': 4,
        'ia': 2,
        'iên': 4,
        'iêng': 5,
        'iêm': 4,
        'ưa': 3,
        'ươn': 4,
        'ương': 5,
        'ươm': 4,
        'ao': 2,
        'au': 2,
        'âu': 3,
        'eo': 2,
        'êu': 3,
        'iu': 2,
        'ưu': 3,
        'iêu': 4,
        'ươu': 4,
        'oai': 3,
        'oay': 3,
        'uây': 4,
        'uôi': 4,
        'uơi': 4,
        'ươi': 4,
        'uya': 3,
        'uyên': 5,
        'oao': 3,
        'oau': 3,
        'oeo': 3,
        'uyu': 3,
        'oong': 4,
    }
    
    keys_needed_consonant_families = {
        '0': 0,
        'b': 1, 
        'ch': 2, 
        'd': 1, 
        'đ': 2, 
        'g': 1, # might be 2 gh
        'z': 2, # gi giet gieng case not included 
        'h': 1, 
        'k': 1, 
        'kh': 2, 
        'l': 1, 
        'm': 1, 
        'n': 1, 
        'ng': 2, # might be 3 ngh 
        'nh': 2,
        'p': 1, 
        'ph': 2, 
        'r': 1, 
        's': 1, 
        't': 1, 
        'th': 2, 
        'tr': 2,
        'v': 1, 
        'x': 1
    }
    
    @staticmethod
    def get_keys_needed_from_word(word: str):
        word = word.lower()
        return TelexOrVNI.get_keys_needed_from_crt(Vietnamese.analyze(word))
        cf, rf, t = Vietnamese.analyze(word)
    @staticmethod
    def get_keys_needed_from_crt(crt: str):
        cf, rf, t = crt
        if not rf:
            return None
        
        total_keys = 0
        # ng -> c
        if rf.endswith('ng') and t in [6, 7]:
            total_keys -= 1
            
        # redundant i
        if cf == 'z' and rf in ['i', 'in', 'iên', 'iêng']:
            total_keys -= 1
        
        # additional tone
        if t > 0:
            total_keys += 1
        
        # additional h
        if cf in ['g', 'ng'] and rf in Vietnamese.rhymes_families_with_ngh_gh:
            total_keys += 1
        
        return total_keys + TelexOrVNI.keys_needed_consonant_families[cf] + TelexOrVNI.keys_needed_rhyme_family[rf]
class V7():
    '''
    For comparison, not for use!
    '''
    inputAgent = InputMethod()
    @staticmethod
    def get_full_from_crt(crt):
        cf, rf, t = crt
        if not rf:
            return None
        
        total_keys = 0
        if cf == '0':
            total_keys -= 1
            
        if cf == 'đ':
            total_keys += 1
            
        # ng -> c
        if rf.endswith('ng') and t in [6, 7]:
            total_keys -= 1 
            
        return total_keys + len(cf) + len(rf) + 1
    
    @staticmethod
    def get_least_from_words(words: list[str]):
        crts = [Vietnamese.analyze(word) for word in words]
        for crt in crts:
            if None in crt:
                raise Exception
        
        if len(words) == 1:
            cf, rf, t = crts[0]
            if cf == '0':
                return V7.get_full_from_crt((cf, rf, t))
            else:
                relative_raw = cf + str(t)
                relative_raw = relative_raw.replace('đ', 'dd')
                
                '''
                # Pass it in inputAgent: To see if it's in the first page?
                res = V7.inputAgent.predict(relative_raw)
                relative_raw
                '''
        elif len(words) <= 3:            
            relative_raw: str = reduce(lambda res, curr: res+curr[0]+str(curr[2]) if curr[0] != '0' else res+curr[1][0]+str(curr[2]), crts, '')
            relative_raw = relative_raw.replace('đ', 'dd')
        else:
            total = 0
            for crt in crts:
                total += V7.get_full_from_crt(crt)
            return total - len(words) - 1 # Arbitrary number
        
        return len(relative_raw)
        
        
    @staticmethod
    def get_keys_needed_from_word(word: str):
        word = word.lower()
        return V7.get_keys_needed_from_crt(Vietnamese.analyze(word))
        cf, rf, t = Vietnamese.analyze(word)
    @staticmethod
    def get_keys_needed_from_crt(crt: str):
        cf, rf, t = crt
        if not rf:
            return None
        
        return V7.get_full_from_crt((cf, rf, t))

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
        total_other_input_method += len(words) - 1 # spaces
        
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
    print(f'LEN1 Diff all        mean: {statistics.mean(diffs_len_1)}' f'std:  {statistics.stdev(diffs_len_1)} ({len(diffs_len_1)})')
    print(f'LEN1 Faster rate all mean: {statistics.mean(faster_rate_len_1)}' f'std:  {statistics.stdev(faster_rate_len_1)}')
    print(f'LEN2 Diff all        mean: {statistics.mean(diffs_len_2)}' f'std:  {statistics.stdev(diffs_len_2)} ({len(diffs_len_2)})')
    print(f'LEN2 Faster rate all mean: {statistics.mean(faster_rate_len_2)}' f'std:  {statistics.stdev(faster_rate_len_2)}')
    print(f'LEN3 Diff all        mean: {statistics.mean(diffs_len_3)}' f'std:  {statistics.stdev(diffs_len_3)} ({len(diffs_len_3)})')
    print(f'LEN3 Faster rate all mean: {statistics.mean(faster_rate_len_3)}' f'std:  {statistics.stdev(faster_rate_len_3)}')
    print(f'LEN4+ Diff all        mean: {statistics.mean(diffs_len_4)}' f'std:  {statistics.stdev(diffs_len_4)} ({len(diffs_len_4)})')
    print(f'LEN4+ Faster rate all mean: {statistics.mean(faster_rate_len_4)}' f'std:  {statistics.stdev(faster_rate_len_4)}')
    
    
if __name__ == '__main__':
    compare()
    