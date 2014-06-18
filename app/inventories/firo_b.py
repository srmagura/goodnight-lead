from shared import *

class FiroBQuestion(NumberQuestion):

    minimum = 1
    maximum = 6
    
    choice_labels = (
        'Usually', 'Often', 'Sometimes',
        'Occasionally', 'Rarely', 'Never'
    )
    
    
class FiroB(Inventory):

    name = 'Fundamental Interpersonal Relations Orientation-behavior'
    template = 'firo_b.html'

    question_text = (
        {
            1: 'An expert who doesn\'t come up with a definite answer probably doesn\'t know much.',
        },
        {
            2: 'I would like to live in a foreign country for a while.',
        },
        {
            3: 'There is really no such thing as a problem that can\'t be solved.',
        },
    )

    def __init__(self):
        pass

    def set_submission(self, submission):
        self.submission = submission
        
        if self.submission is None:
            current_page = 0
        else:
            current_page = self.submission.current_page       
            
        self.questions = []
        
        for qid, text in self.question_text[current_page].items():
            self.questions.append(FiroBQuestion(qid, text))           
           
    def compute_metrics(self):
        pass
            
    def review_add_data(self, data):
        if not data['metrics']:
            return
            
        pass

    
        
