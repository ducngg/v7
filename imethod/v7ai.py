from .v7 import InputMethod
from ai import get_model, next, tokenizer

from typing import List
from models import Raw, Triplet, MatchingTriplet, Word, Phrase

class AIInputMethod(InputMethod):
    location = "<imethod.v7ai.AIInputMethod>"
    def __init__(
        self, 
        *, 
        vni_tones=False, 
        strict_k=False, 
        null_consonant='hh', 
        end_of_rhyme='.', 
        verbose=1
    ) -> None:
        super().__init__(
            vni_tones=vni_tones, 
            strict_k=strict_k, 
            null_consonant=null_consonant, 
            end_of_rhyme=end_of_rhyme
        )
        self.mode = "[AI]"
        self.SOS = "tôi" # start of string
        
        if verbose:
            print(f"{AIInputMethod.location} Loaded:")
        self.model = get_model(verbose=verbose)
    
    def accept(self, crt: Triplet, crst: MatchingTriplet, word: Word):
        
        consonant, rhyme, tone = crt.unpack() # Triplet of the AI-predicted word
        consonant_rule, rhymes_rule, tone_rule = crst.unpack() # Possibilities from user
        
        if self.vni_tones:
            # Still accept tone=6 or tone=7 although tone_rule is 1 or 5
            if tone == 6 and tone_rule == 1:
                tone = 1
            if tone == 7 and tone_rule == 5:
                tone = 5
        
        if tone != tone_rule:
            return False
        if rhyme not in rhymes_rule:
            return False
        if consonant == 'k':
            if consonant_rule in ['k', 'c', 'q'] and consonant_rule == word[0]:
                return True
            else:
                return False
        if consonant != consonant_rule:
            return False
                
        return True
        
    def predict(self, input_string: str, context: str):
        if context.strip() == "":
            context = self.SOS
        raws = self.seperate_raws(input_string)
        cap_pos = [raw[0].isupper() for raw in raws]
        
        raws_parts = [self.parse(raw.lower()) for raw in raws]
        CRsTs = [self.find(raw_parts) for raw_parts in raws_parts]

        # Return None if any is None (failed to find consonant/rhymes/tone)
        if len(CRsTs) == 0 or not all(CRsTs):
            return None
        
        # TODO: Should have same behaviour as the pinyin
        # if len(CRsTs) == 1:
        #     combination_possibilities = self.predict_1(input_string, CRsTs, context)
        # elif len(CRsTs) == 2:
        #     combination_possibilities = self.predict_2(input_string, CRsTs, context)
        # else:
        #     combination_possibilities = self.predict_super(input_string, CRsTs, context)
        
        combination_possibilities = self.top_1_predict(input_string, CRsTs, context)
    
        return [self.apply_capitalization(combination, cap_pos) for combination in combination_possibilities]

    # def basic_predict(self, input_string, CRsTs, context: str):        
    #     prediction = next(self.model, [context])[0]
    #     prediction.remove(0)
            
    #     FIRST_LIMIT = 9
    #     valid_words = []
    #     for crt, word in zip(tokenizer.analyze(prediction), tokenizer.detokenize(prediction)):
    #         if len(valid_words) >= FIRST_LIMIT:
    #             break
    #         if self.accept(crt, CRsTs[0]):
    #             valid_words.append(word)
                
    #     results = [word for word in valid_words]
    #     updated_contextes = [context + ' ' + word for word in valid_words]
        
    #     for CRsT in CRsTs[1:]:
    #         predictions = next(self.model, updated_contextes)
    #         [prediction.remove(0) for prediction in predictions]
            
    #         for idx, prediction in enumerate(predictions):
    #             for crt, word in zip(tokenizer.analyze(prediction), tokenizer.detokenize(prediction)):
    #                 if self.accept(crt, CRsT):
    #                     results[idx] += ' ' + word
    #                     updated_contextes[idx] += ' ' + word
    #                     break
                                                    
    #     return results
    
    def top_1_predict(self, input_string, CRsTs: List[MatchingTriplet], context: str):  
        
        current_result = []
        for CRsT in CRsTs[:-1]:
            prediction = next(self.model, [context])[0]
            prediction.remove(0)
            
            for triplet, word in zip(tokenizer.triplets(prediction), tokenizer.detokenize(prediction)):
                if self.accept(triplet, CRsT, word):
                    context += ' ' + word
                    current_result.append(word)
                    break
                          
        prediction = next(self.model, [context])[0]
        prediction.remove(0)
            
        LIMIT = 36
        results: List[Phrase] = []
        for triplet, word in zip(tokenizer.triplets(prediction), tokenizer.detokenize(prediction)):
            if len(results) >= LIMIT:
                break
            if self.accept(triplet, CRsTs[-1], word):
                results.append(' '.join(current_result + [word]))
                                                    
        return results
    
    # def predict_1(self, input_string, CRsTs, context: str):
    #     prediction = next(self.model, [context])[0]
    #     prediction.remove(0)
            
    #     combination_possibilities = []
    #     for crt, word in zip(tokenizer.analyze(prediction), tokenizer.detokenize(prediction)):
    #         if self.accept(crt, CRsTs[0]):
    #             combination_possibilities.append(word)
        
    #     return combination_possibilities
    
    # def predict_2(self, input_string, CRsTs, context: str):
    #     first_prediction = next(self.model, [context])[0]
    #     first_prediction.remove(0)
            
    #     FIRST_LIMIT = 9 # previous 3
    #     first_combination_possibilities: list[str] = []
    #     for crt, word in zip(tokenizer.analyze(first_prediction), tokenizer.detokenize(first_prediction)):
    #         if len(first_combination_possibilities) >= FIRST_LIMIT:
    #             break
    #         if self.accept(crt, CRsTs[0]):
    #             first_combination_possibilities.append(word)
                
    #     updated_contextes = [context + ' ' + word for word in first_combination_possibilities]
        
    #     second_predictions = next(self.model, updated_contextes)
    #     [second_prediction.remove(0) for second_prediction in second_predictions]
        
    #     final_combination_possibilities = []
    #     SECOND_LIMITS = [1 for _ in range(9)] # previous [4, 3, 2] (len=FIRST_LIMIT)
    #     for first_word, second_prediction, SECOND_LIMIT in zip(first_combination_possibilities, second_predictions, SECOND_LIMITS):
    #         second_combination_possibilities = []
    #         for crt, word in zip(tokenizer.analyze(second_prediction), tokenizer.detokenize(second_prediction)):
    #             if len(second_combination_possibilities) >= SECOND_LIMIT:
    #                 break
    #             if self.accept(crt, CRsTs[1]):
    #                 second_combination_possibilities.append(first_word + ' ' + word)
                    
    #         final_combination_possibilities.extend(second_combination_possibilities)
        
    #     return final_combination_possibilities
        
        
    
    def predict_super(self, input_string, CRsTs, context: str):
        combination_possibilities = super().predict(input_string)
        return combination_possibilities

    