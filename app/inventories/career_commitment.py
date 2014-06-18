from shared import *

class CareerCommitmentQuestion(NumberQuestion):

    minimum = 1
    maximum = 5
    
    choice_labels = (
        'DS', 'D', 'N', 'A', 'AS'
    )
    
    
class CareerCommitment(Inventory):

    name = 'Career Commitment'
    template = 'career_commitment.html'

    question_text = {
        1: 'My major/career field is an important part of who I am.',
        2: 'My major/career field has a great deal of personal meaning to me.',
        3: 'I do not feel "emotionally attached" to my major/career field.',
        4: 'I strongly identify with my chosen major/career field.',
        5: 'I do not have a strategy for achieving my goals in my major/career field.',
        6: 'I have created a plan for my development in my major/career field.',
        7: 'I do not identify specific goals for my development in my major/career field.',
        8: 'I do not often think about my personal development in my major/career field.'
    }

    def __init__(self):
        self.questions = []
        
        for qid, text in self.question_text.items():
            self.questions.append(CareerCommitmentQuestion(qid, text))
           
    def compute_metrics(self):
        def reverse(s):
            return 6 - int(s)
    
        self.metrics = {
            'identity': int(self.answers[1]) +
                int(self.answers[2]) +
                reverse(self.answers[3]) +
                int(self.answers[4]),
            'planning': reverse(self.answers[5]) +
                int(self.answers[6]) +
                reverse(self.answers[7]) +
                reverse(self.answers[8])
        }
            
    def review_process_metrics(self, data, metrics):          
        for metric in metrics:
            data[metric.key + '_factor'] = int(metric.value)
    
        
