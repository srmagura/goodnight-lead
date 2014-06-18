from shared import *

class CoreSelfQuestion(NumberQuestion):

    minimum = 1
    maximum = 5
    
    choice_labels = (
        'DS', 'D', 'N', 'A', 'AS'
    )
    
    
class CoreSelf(Inventory):

    name = 'Core Self Evaluation Scale'
    template = 'core_self.html'

    question_text = {
        1: 'I am confident I get the success I deserve in life.',
        2: 'Sometimes I feel depressed.',
        3: 'When I try, I generally succeed.',
        4: 'Sometimes when I fail I feel worthless.',
        5: 'I complete tasks successfully.',
        6: 'Sometimes, I do not feel in control of my work.',
        7: 'Overall, I am satisfied with myself.',
        8: 'I am filled with doubts about my competence.',
        9: 'I determine what will happen in my life.',
        10: 'I do not feel in control of my success in my career.',
        11: 'I am capable of coping with most of my problems.',
        12: 'There are times when things look pretty bleak and hopeless to me.'
    }

    def __init__(self):
        self.questions = []
        
        for qid, text in self.question_text.items():
            self.questions.append(CoreSelfQuestion(qid, text))
           
    def compute_metrics(self):
        reverse_score = {2, 4, 6, 8, 10, 12}
        score = 0
        
        for qid, value in self.answers.items():
            if qid in reverse_score:
                score -= int(value)
            else:
                score += int(value)
        
        self.metrics = {'score': score}    
            
    def review_add_data(self, data):
        if not data['metrics']:
            return
            
        data['score'] = int(data['metrics'][0].value)
    
        