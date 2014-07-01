from __future__ import division
from shared import *
from view_objects import Slider, SliderMarker, SliderContainer

class BigFiveQuestion(NumberQuestion):

    minimum = 1
    maximum = 7
    
    choice_labels = (
        'DS', 'DM', 'DL', 'N',
        'AL', 'AM', 'AS'
    )
    
    
class BigFive(Inventory):

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
            
        for key in self.metrics:
            self.metrics[key] /= 2
            
    def review_process_metrics(self, data, metrics):
        keys = (
            'extraversion',
            'agreeableness',
            'conscientiousness',
            'emotional_stability',
            'openness'
        )
         
        means = (
            4, # 4.44
            4, # 5.23 
            4, # 5.4 
            4, #4.83
            4, # 5.38  
        )
                
        labels = (
            ('Introverted', 'Extroverted'),
            ('Assertive', 'Agreeable'),
            ('Impulsive', 'Conscientious'),
            ('Anxious', 'Emotionally stable'),
            ('Traditional', 'Open to experience')  
        )
                
        values = {}
        for metric in metrics:
            values[metric.key] = int(metric.value)
            
        slider_containers = []
            
        for i in range(len(keys)):
            key = keys[i]
            
            marker_you = SliderMarker('you', 'You', values[key])
            marker_mean = SliderMarker('mean', 'Mean', means[i])
            slider = Slider(1, 7, (marker_you, marker_mean))
            
            slider_container = SliderContainer(labels[i], slider)
            slider_containers.append(slider_container)
        
        data['slider_containers'] = slider_containers
        
