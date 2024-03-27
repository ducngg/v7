'''
Not yet developed properly yet, try it in sandbox4.py
'''
import random
import json
from vietnamese import Vietnamese
import copy
import utils
import sys
import time
import heapq
            
class MarkovModel():
    def __init__(self, n_gram=1, load_checkpoint=True, checkpoint='model_threshold_3.json') -> None:
        self.model = {}
        self.normalized_model = {}
        self.n_gram = n_gram
        '''
        model = {
            word_1: {
                next_word_1: count,  # the number of times this pair appears in the text
                next_word_2: count,  # the number of times this pair appears in the text
                ...
                next_word_n: count,  # the number of times this pair appears in the text
            }
            ...
            word_n: {
                next_word_1: count,  # the number of times this pair appears in the text
                next_word_2: count,  # the number of times this pair appears in the text
                ...
                next_word_n: count,  # the number of times this pair appears in the text
            }
        }
        '''
        if load_checkpoint:
            self.load(checkpoint)
                    
    def learn(self, words):
        '''
        Update next_state of each words.
        '''
        for i in range(len(words) - self.n_gram - 1):
            curr_state, next_state = "", ""
            for j in range(self.n_gram):
                curr_state += words[i+j] + " "
                next_state += words[i+j+self.n_gram] + " "
            curr_state = curr_state[:-1]
            next_state = next_state[:-1]
            if curr_state not in self.model:
                self.model[curr_state] = {}
                self.model[curr_state][next_state] = 1
            else:
                if next_state in self.model[curr_state]:
                    self.model[curr_state][next_state] += 1
                else:
                    self.model[curr_state][next_state] = 1
        
    def update(self):
        '''
        Update normalized_model, use this before inference
        '''
        self.normalized_model: dict[str, dict[str, int]] = copy.deepcopy(self.model)
        # calculating transition probabilities
        for curr_state, transition in self.normalized_model.items():
            total = sum(transition.values())
            for next_state, count in transition.items():
                self.normalized_model[curr_state][next_state] = count/total
    
    def next(self, start, step=1):
        '''
        Next n steps from start
        '''
        i = 0
        curr_state = start
        next_state = None
        nexts = []
        while i < step:
            tops = self.top(curr_state, 10)
            total_probability = sum([top[1] for top in tops])
            normalized_probabilities = [top[1] / total_probability for top in tops]
            next_state = random.choices(
                [top[0] for top in tops],
                normalized_probabilities
            )
            curr_state = next_state[0]
            nexts.append(curr_state)
            i += 1
        return nexts

    def top(self, start, n=5):
        '''
        Top next n words with highest probability
        '''
        if self.normalized_model is None:
            raise ValueError("Normalized model is not initialized. Please use self.update() first.")
        if start not in self.normalized_model:
            raise KeyError(f"Key '{start}' not found in normalized model.")
            
        # Sort dictionary items by values in descending order
        sorted_items = sorted(self.normalized_model[start].items(), key=lambda x: x[1], reverse=True)
        
        return sorted_items[:n]
    
    def load(self, path):
        with open(path, 'r') as f:
            self.model = json.load(f)
        self.update()
                
    def save(self):
        with open('model.json', 'w') as f:
            json.dump(self.model, f, indent=4)
            
    def train_on_data(self, path):
        l = 0
        max_line = 50000000
        processed = 0
        start_time = time.time()

        for words in utils.get_words_line_by_line(path):
            if l > max_line:
                break
            self.learn(words)
            l += 1
            processed += len(words)
            if l % 50000 == 0:
                processed_time = time.time() - start_time
                self.save()
                
                print(f'\n\n~~~ {processed_time:.2f}s ~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print(f'Processed : {processed}')
                print(f'Speed: {processed/processed_time:.2f} words/s')
                print('~~~~~~~~~~~~~~~~~~~~~ saved checkpoint ~~~~~~~~~~~~~~~~~~\n')
                
        self.save()
    
if __name__ == '__main__':
    '''
    Please ignore this, this is for updating model.json from my private data folder.
    '''
    if len(sys.argv) < 3:
        pass
    else:
        if 'train' in sys.argv[1]:
            # Running big corpus to save the chain into a JSON file
            if 'markov' in sys.argv[2]:
                print('Running on text data to update model.json... Press control-C right now if you want to stop...')
                time.sleep(10)
                learning_model = MarkovModel(load_checkpoint=False)
                learning_model.train_on_data('data/corpus-title.txt')
                        
                print('Done update model.json based on text data...')
        
        if 'simplify' in sys.argv[1]:
            if 'markov' in sys.argv[2]:
                # python model.py simplify markov 3
                if 'thresh' in sys.argv[3]:
                    if int(sys.argv[4]) > 0:
                        threshold = int(sys.argv[4])
                        print(f'Simplify model.json to model_threshold_{threshold}.json, any records < {threshold} will be skipped ... Press control-C right now if you want to stop...')
                        time.sleep(10)
                        
                        model = MarkovModel()
                        simplify_model: dict[str, dict[str, int]] = model.model
                        
                        for word in simplify_model.keys():
                            simplify_model[word] = {next_word: count for next_word, count in simplify_model[word].items() if count >= threshold}

                        with open(f'model_threshold_{threshold}.json', 'w') as f:
                            json.dump(simplify_model, f, indent=4)

                        print(f'Done simplify model.json to model_threshold_{threshold}.json...')
                
                # python model.py simplify markov top 10
                if 'top' in sys.argv[3]:
                    if int(sys.argv[4]) > 0:
                        top = int(sys.argv[4])
                        print(f'Simplify model.json to model_top_{top}.json, just keep maximum {top} counts for each entries ... Press control-C right now if you want to stop...')
                        time.sleep(10)
                        
                        model = MarkovModel()
                        simplify_model: dict[str, dict[str, int]] = model.model
                        
                        for word, next_words in simplify_model.items():
                            top_next_words = heapq.nlargest(top, next_words, key=next_words.get)
                            simplify_model[word] = {next_word: next_words[next_word] for next_word in top_next_words}

                        with open(f'model_top_{top}.json', 'w') as f:
                            json.dump(simplify_model, f, indent=4)
                        
                        print(f'Done simplify model.json to model_top_{top}.json...')
                