from shared import *

class BigFiveQuestion(NumberQuestion):

    minimum = 1
    maximum = 7
    
    choice_labels = (
        'DS', 'DM', 'DL', 'N',
        'AL', 'AM', 'AS'
    )
    
    
class BigFive:

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
