import sys
from collections import OrderedDict

from shared import *

class ViaQuestion(NumberQuestion):

    minimum = 1
    maximum = 5

    choice_labels = (
        'Very much unlike me', 'Unlike me', 'Neutral',
        'Like me', 'Very much like me'
    )


def strength_to_key(s):
    return s.lower().replace(' ', '_')
    
class Via(Inventory):

    name = 'VIA'
    template = 'via.html'
    questions_per_page = 20

    def __init__(self):
        format_str = '{}/app/inventories/via_items.dat'
        infile = open(format_str.format(sys.path[0]))
        
        self.question_text = []
        self.scoring_dict = {}
        self.strength_dict = {}
        
        i = 0
        for line in infile:
            if i % self.questions_per_page == 0:
                page_questions = OrderedDict()
                self.question_text.append(page_questions)
        
            qid_s, text, strength = line.replace('\n', '').split('\t')
            qid = int(qid_s)
            
            page_questions[qid] = text
            
            key = strength_to_key(strength)
            if key not in self.scoring_dict:
                self.scoring_dict[key] = set()
                self.strength_dict[key] = strength
              
            self.scoring_dict[key].add(qid)
            i += 1
    
        self.n_pages = len(self.question_text)

    def set_submission(self, submission):
        self.submission = submission
        
        if self.submission is None:
            current_page = 0
        else:
            current_page = self.submission.current_page       
            
        self.questions = []
        
        for qid, text in self.question_text[current_page].items():
            self.questions.append(ViaQuestion(qid, text))           
           
    def compute_metrics(self):
        self.metrics = {}
        
        for key, qid_set in self.scoring_dict.items():
            total = 0           
            for qid in qid_set:
                total += int(self.answers[qid])
                
            self.metrics[key] = total
            
    def review_process_metrics(self, data, metrics):          
        all_strengths = []
        
        for metric in metrics:
            strength = self.strength_dict[metric.key]
            all_strengths.append({
                'strength': strength,
                'score': int(metric.value),
                'is_signature': False
            })
            
        all_strengths.sort(key=(lambda obj: obj['score']), reverse=True)
        
        for obj in all_strengths[:3]:
            obj['is_signature'] = True
        
        data['strengths'] = all_strengths[:10]
    
        
