from .v7 import InputMethod
from ai import get_model, next, tokenizer

class AIInputMethod(InputMethod):
    def __init__(self, flexible_tones=False, strict_k=False, flexible_k=False, null_consonant='hh', end_of_rhyme='.') -> None:
        super().__init__(flexible_tones, strict_k, flexible_k, null_consonant, end_of_rhyme)
        self.mode = "[AI]"
        self.SOS = "tôi" # start of string
        self.model = get_model()
    
    def accept(self, crt, crst):
        consonant, rhyme, tone = crt
        consonant_rule, rhymes_rule, tone_rule = crst
        if consonant == 'k' and consonant_rule in ['c', 'q']:
            # TODO: we don't have the information of raw crt here so cannot filter c q k
            consonant_rule = 'k' # Code got here means that have used self.find() -> Have checked strict k
        
        if self.flexible_tones:
            # Still accept tone=6 or tone=7 although tone_rule is 1 or 5
            if tone == 6 and tone_rule == 1:
                tone = 1
            if tone == 7 and tone_rule == 5:
                tone = 5            

        if (tone != tone_rule):
            return False
        
        if (consonant != consonant_rule) or (rhyme not in rhymes_rule):
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

    def basic_predict(self, input_string, CRsTs, context: str):        
        prediction = next(self.model, [context])[0]
        prediction.remove(0)
            
        FIRST_LIMIT = 9
        valid_words = []
        for crt, word in zip(tokenizer.analyze(prediction), tokenizer.detokenize(prediction)):
            if len(valid_words) >= FIRST_LIMIT:
                break
            if self.accept(crt, CRsTs[0]):
                valid_words.append(word)
                
        results = [word for word in valid_words]
        updated_contextes = [context + ' ' + word for word in valid_words]
        
        for CRsT in CRsTs[1:]:
            predictions = next(self.model, updated_contextes)
            [prediction.remove(0) for prediction in predictions]
            
            for idx, prediction in enumerate(predictions):
                for crt, word in zip(tokenizer.analyze(prediction), tokenizer.detokenize(prediction)):
                    if self.accept(crt, CRsT):
                        results[idx] += ' ' + word
                        updated_contextes[idx] += ' ' + word
                        break
                                                    
        return results
    
    def top_1_predict(self, input_string, CRsTs, context: str):  
        
        current_result = []
        for CRsT in CRsTs[:-1]:
            prediction = next(self.model, [context])[0]
            prediction.remove(0)
            
            for crt, word in zip(tokenizer.analyze(prediction), tokenizer.detokenize(prediction)):
                if self.accept(crt, CRsT):
                    context += ' ' + word
                    current_result.append(word)
                    break
                          
        prediction = next(self.model, [context])[0]
        prediction.remove(0)
            
        LIMIT = 36
        results = []
        for crt, word in zip(tokenizer.analyze(prediction), tokenizer.detokenize(prediction)):
            if len(results) >= LIMIT:
                break
            if self.accept(crt, CRsTs[-1]):
                results.append(' '.join(current_result + [word]))
                                                    
        return results
    
    def predict_1(self, input_string, CRsTs, context: str):
        prediction = next(self.model, [context])[0]
        prediction.remove(0)
            
        combination_possibilities = []
        for crt, word in zip(tokenizer.analyze(prediction), tokenizer.detokenize(prediction)):
            if self.accept(crt, CRsTs[0]):
                combination_possibilities.append(word)
        
        return combination_possibilities
    
    def predict_2(self, input_string, CRsTs, context: str):
        first_prediction = next(self.model, [context])[0]
        first_prediction.remove(0)
            
        FIRST_LIMIT = 9 # previous 3
        first_combination_possibilities: list[str] = []
        for crt, word in zip(tokenizer.analyze(first_prediction), tokenizer.detokenize(first_prediction)):
            if len(first_combination_possibilities) >= FIRST_LIMIT:
                break
            if self.accept(crt, CRsTs[0]):
                first_combination_possibilities.append(word)
                
        updated_contextes = [context + ' ' + word for word in first_combination_possibilities]
        
        second_predictions = next(self.model, updated_contextes)
        [second_prediction.remove(0) for second_prediction in second_predictions]
        
        final_combination_possibilities = []
        SECOND_LIMITS = [1 for _ in range(9)] # previous [4, 3, 2] (len=FIRST_LIMIT)
        for first_word, second_prediction, SECOND_LIMIT in zip(first_combination_possibilities, second_predictions, SECOND_LIMITS):
            second_combination_possibilities = []
            for crt, word in zip(tokenizer.analyze(second_prediction), tokenizer.detokenize(second_prediction)):
                if len(second_combination_possibilities) >= SECOND_LIMIT:
                    break
                if self.accept(crt, CRsTs[1]):
                    second_combination_possibilities.append(first_word + ' ' + word)
                    
            final_combination_possibilities.extend(second_combination_possibilities)
        
        return final_combination_possibilities
        
        
    
    def predict_super(self, input_string, CRsTs, context: str):
        combination_possibilities = super().predict(input_string)
        return combination_possibilities

    