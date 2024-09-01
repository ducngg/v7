import json
import time
from ai import tokenizer, get_model, generate, next
from utils import exec

# def main1():
#     model = exec('Load model', get_model)
    
#     sentence = 'tôi đang làm công'
#     output_list = exec('Generate next word', next, seq=sentence, model=model)
#     output_list.remove(0) # Remove the pad token
    
#     matched_ids = exec('Matching', matcher.simple_match, tensor=output_list, rule='v', max=10)
#     words = exec('Detokenize', tokenizer.detokenize, matched_ids)
    
#     print(f"Input: {sentence}")
#     print(f"Next words: {words}")   
        
def main2():
    model = exec('Load model', get_model)
    
    sentence = 'mai tao đi'
    output_list = exec('Generate next words', generate, seq=sentence, model=model, n=30)
   
    print(f"Input: {sentence}")
    print(f"Next words: {' '.join(output_list)}")   
    
    
def main3():
    from imethod.v7ai import AIInputMethod
    inputAgent = AIInputMethod(
        flexible_tones=False,
        strict_k=False,
        flexible_k=False
    )
    combs = inputAgent.predict(
        input_string='b2',
        context=''
    )
    print(len(combs))
    
if __name__ == '__main__':
    main2()