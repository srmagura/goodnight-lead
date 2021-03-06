"""
Definition of Big Five inventory.
"""

# pylint: disable=no-init, no-member

from .shared import Inventory, NumberQuestion
from .view_objects import Slider, SliderMarker, SliderContainer

class BigFiveQuestion(NumberQuestion):
    """
    Question definition for Big Five inventory.

    Answer is on a scale of 1 to 7 (strong disagree to strongly agree).
    """

    minimum = 1
    maximum = 7

    choice_labels = (
        'DS', 'DM', 'DL', 'N',
        'AL', 'AM', 'AS'
    )


class BigFive(Inventory):
    """
    Big Five inventory. 10 questions assessing 5 different core personality
    traits
    """

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
        """
        Create question objects
        """
        self.questions = []

        for qid in range(1, len(self.question_text)+1):
            text = self.question_text[qid]
            self.questions.append(BigFiveQuestion(qid, text))

    def compute_metrics(self):
        """
        Compute the five metrics defined by the inventory: extraversion,
        agreeableness, conscientiousness, emotional_stability, and openness.

        In the comments below, we say which question numbers are associated
        with each metric. The letter R indicates a reverse-scored question.
        """
        def reverse(s):
            return 8 - int(s)

        self.metrics = {}

        # Extraversion: 1, 6R
        self.metrics['extraversion'] =\
            int(self.answers[1]) + reverse(self.answers[6])

        # Agreeableness: 2R, 7
        self.metrics['agreeableness'] =\
            reverse(self.answers[2]) + int(self.answers[7])

        # Conscientiousness: 3, 8R
        self.metrics['conscientiousness'] =\
            int(self.answers[3]) + reverse(self.answers[8])

        # Emotional Stability: 4R, 9
        self.metrics['emotional_stability'] =\
            reverse(self.answers[4]) + int(self.answers[9])

        # Openness to Experiences: 5, 10R
        self.metrics['openness'] =\
            int(self.answers[5]) + reverse(self.answers[10])

        # Each metric has two questions
        # Divide by two to get the average of the two responses
        for key in self.metrics:
            self.metrics[key] /= 2

    def review_process_metrics(self, data, metrics):
        """
        Provide the labels, values, and sliders for the review page.
        """
        keys = (
            'extraversion',
            'agreeableness',
            'conscientiousness',
            'emotional_stability',
            'openness'
        )

        # Mean metric values
        means = (4.44, 5.23, 5.4, 4.83, 5.38)

        # Labels for the two ends of each slider, along with descriptive
        # explanations for what the terms mean
        labels = (
            (
                ('Introverted', 'Extroverted'),
                ('shy, reserved', 'kind, sociable')
            ),
            (
                ('Assertive', 'Agreeable'),
                ('aggressive', 'cooperative')
            ),
            (
                ('Impulsive', 'Conscientious'),
                ('act on the moment', 'responsible, self-disciplined')
            ),
            (
                ('Anxious', 'Emotionally stable'),
                ('moody, worrisome', 'calm, self-confident')
            ),
            (
                ('Traditional', 'Open to experience'),
                ('conventional', 'curious, reflective')
            )
        )

        values = {}
        for metric in metrics:
            values[metric.key] = metric.value

        # Create sliders
        slider_containers = []

        for i in range(len(keys)):
            key = keys[i]

            marker_you = SliderMarker('you', 'You', values[key])
            marker_mean = SliderMarker('mean', 'Mean', means[i])
            slider = Slider(1, 7, (marker_you, marker_mean))

            slider_container = SliderContainer(labels[i][0], slider)
            slider_container.sublabels = labels[i][1]
            slider_containers.append(slider_container)

        # Pass to view
        data['slider_containers'] = slider_containers
