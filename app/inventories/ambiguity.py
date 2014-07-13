from shared import *
from view_objects import *

class AmbiguityQuestion(NumberQuestion):

    minimum = 1
    maximum = 7
    
    choice_labels = (
        'DS', 'DM', 'DL', 'N',
        'AL', 'AM', 'AS'
    )
    
    
class Ambiguity(Inventory):

    name = 'Ambiguity'
    template = 'ambiguity.html'

    question_text = {
        1: 'An expert who doesn\'t come up with a definite answer probably doesn\'t know much.',
        2: 'I would like to live in a foreign country for a while.',
        3: 'There is really no such thing as a problem that can\'t be solved.',
        4: 'People who fit their lives to a schedule probably miss most of the joy of living.',
        5: 'A good job is one where what is to be done and how it is to be done are always clear.',
        6: 'It is more fun to tackle a complicated problem than to solve a simple one.',
        7: 'In the long run it is possible to get more done by tackling small, simple problems rather than large and complicated ones.',
        8: 'Often the most interesting and stimulating people are those who don\'t mind being different and original.',
        9: 'What we are used to is always preferable to what is unfamiliar.',
        10: 'People who insist upon a yes or no answer just don\'t know how complicated things really are.',
        11: 'A person who leads an even, regular life in which few surprises or unexpected happenings arise really has a lot to be grateful for.',
        12: 'Many of our most important decisions are based upon insufficient information.',
        13: 'I like parties where I know most of the people more than ones where all or most of the people are complete strangers.',
        14: 'Teachers and supervisors who hand out vague assignments give one a chance to show initiative and originality.',
        15: 'The sooner we all acquire similar values and ideals the better.',
        16: 'A good teacher is one who makes you wonder about your way of looking at things.'
    }

    def __init__(self):
        self.questions = []
        
        for qid in range(1, len(self.question_text)+1):
            text = self.question_text[qid]
            self.questions.append(AmbiguityQuestion(qid, text))
           
    def compute_metrics(self):
        score = 0
        
        for qid, answer in self.answers.items():
            if qid % 2 == 0:
                score += 8 - int(answer)
            else:
                score += int(answer)
    
        self.metrics = {'score': score}
            
    def review_process_metrics(self, data, metrics):           
        score = int(metrics[0].value)
        marker = SliderMarker('you', 'You', score)
        slider = Slider(16, 112, (marker,))
        data['slider_container'] = SliderContainer(('', ''), slider)

    
        
