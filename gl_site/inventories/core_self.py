# pylint: disable=no-init, no-member

from .shared import NumberQuestion, Inventory
from .view_objects import Slider, SliderMarker

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

        for qid in range(1, len(self.question_text)+1):
            text = self.question_text[qid]
            self.questions.append(CoreSelfQuestion(qid, text))

    def compute_metrics(self):
        score = 0

        for qid, value in self.answers.items():
            if qid % 2 == 0:
                score += 6 - int(value)
            else:
                score += int(value)

        self.metrics = {'score': score / 12.}

    def review_process_metrics(self, data, metrics):
        marker = SliderMarker('you', 'You', metrics[0].value)
        data['slider'] = Slider(1, 5, (marker,))
