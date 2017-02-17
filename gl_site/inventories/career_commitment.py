"""
Definition of Career Commitment inventory, which measures how
committed the user is to their specific major/field
"""
# pylint: disable=no-init, no-member

from .shared import Inventory, NumberQuestion
from .view_objects import Slider, SliderContainer, SliderMarker

class CareerCommitmentQuestion(NumberQuestion):
    """
    Questions in the Career Commitment inventory are scored on a 1 to 5
    scale: strongly disagree to strongly agree
    """

    minimum = 1
    maximum = 5

    choice_labels = (
        'DS', 'D', 'N', 'A', 'AS'
    )


class CareerCommitment(Inventory):
    """
    Define the questions and score computation
    """

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
        """
        Create question objects

        TODO: Code duplicated across many inventories?
        """
        self.questions = []

        for qid in range(1, len(self.question_text)+1):
            text = self.question_text[qid]
            self.questions.append(CareerCommitmentQuestion(qid, text))

    def compute_metrics(self):
        """
        Compute the identity and planning metrics. Some items are
        reverse scored.
        """
        def reverse(s):
            return 6 - int(s)

        self.metrics = {
            'identity': (int(self.answers[1]) +
                int(self.answers[2]) +
                reverse(self.answers[3]) +
                int(self.answers[4]))/4.,
            'planning': (reverse(self.answers[5]) +
                int(self.answers[6]) +
                reverse(self.answers[7]) +
                reverse(self.answers[8]))/4.
        }

    def review_process_metrics(self, data, metrics):
        """
        Create sliders for the review page.

        Two sliders: identity factor and planning factor
        """
        labels = {
            'identity': 'Identity factor',
            'planning': 'Planning factor'
        }

        data['slider_containers'] = {}

        min_score = 1
        max_score = 5

        for metric in metrics:
            marker = SliderMarker('you', 'You', metric.value)
            slider = Slider(min_score, max_score, (marker,))

            labels2 = (labels[metric.key], '')
            data['slider_containers'][metric.key] = SliderContainer(labels2, slider)
