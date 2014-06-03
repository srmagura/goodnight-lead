from shared import *

class BigFiveQuestion(NumberQuestion):

    minimum = 1
    maximum = 7
    
    choice_labels = (
        'DS', 'DM', 'DL', 'N',
        'AL', 'AM', 'AS'
    )
    
    
class BigFive(Inventory):

    inventory_id = 0
    name = 'Big Five'
    template = 'big_five.html'

    question_text = {
        1: 'Extraverted, enthusiastic.',
        2: 'Critical, quarrelsome.',
        3: 'Dependable, self-disciplined.',
        4: 'Anxious, easily upset.',
        5: 'Open to new experiences, complex.',
        6: 'Reserved, quiet.',
        7: 'Sympathetic, warm.',
        8: 'Disorganized, careless.',
        9: 'Calm, emotionally stable.',
        10: 'Conventional, uncreative.'
    }

    def __init__(self):
        self.questions = []
        
        for qid, text in self.question_text.items():
            self.questions.append(BigFiveQuestion(qid, text))
           
    def compute_metrics(self):
        keys = ('extraversion', 'agreeableness', 'conscientiousness',
            'emotional_stability', 'openness')
        self.metrics = {k: 0 for k in keys}
        
        # Extraversion: 1, 6R 
        self.metrics['extraversion'] +=\
            int(self.answers[1]) - int(self.answers[6])
            
        # Agreeableness: 2R, 7
        self.metrics['agreeableness'] +=\
            -int(self.answers[2]) + int(self.answers[7])
            
        # Conscientiousness: 3, 8R
        self.metrics['conscientiousness'] +=\
            int(self.answers[3]) - int(self.answers[8])
            
        # Emotional Stability: 4R, 9
        self.metrics['emotional_stability'] +=\
            -int(self.answers[4]) + int(self.answers[9])
            
        # Openness to Experiences: 5, 10R
        self.metrics['openness'] +=\
            int(self.answers[5]) - int(self.answers[10])
