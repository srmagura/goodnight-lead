from collections import OrderedDict

from shared import *

class FiroBQuestion(NumberQuestion):

    minimum = 1
    maximum = 6
    
class FiroBQuestion0(FiroBQuestion):
    choice_labels = (
        'Usually', 'Often', 'Sometimes',
        'Occasionally', 'Rarely', 'Never'
    )
 
class FiroBQuestion1(FiroBQuestion):
    choice_labels = (
        'Most people', 'Many people', 'Some people',
        'A few people',  'One or two people', 'Nobody'
    )   
   
question_cls_list = (FiroBQuestion0, FiroBQuestion1, FiroBQuestion0)
    
class FiroB(Inventory):

    name = 'Fundamental Interpersonal Relations Orientation-behavior'
    template = 'firo_b.html'

    question_text = (
        OrderedDict((
            (1, 'I try to be with people.'),
            (2, 'I let other people decide what to do.'),
            (3, 'I join social groups.'),
            (4, 'I try to have close relationships with people.'),
            (5, 'I tend to join social organizations when I have an opportunity.'),
            (6, 'I let other people strongly influence my actions.'),
            (7, 'I try to be included in informal social activities.'),
            (8, 'I try to have close, personal relationships with people.'),
            (9, 'I try to include other people in my plans.'),
            (10, 'I let other people control my actions.'),
            (11, 'I try to have people around me.'),
            (12, 'I try to get close and personal with people.'),
            (13, 'When people are doing things together I tend to join in.'),
            (14, 'I am easily led by people.'),
            (15, 'I try to avoid being alone.'),
            (16, 'I try to participate in group activities.')
        )),
        OrderedDict((
            (17, 'I try to be friendly to people.'),
            (18, 'I let other people decide what to do.'),
            (19, 'My personal relations with people are cool and distant.'),
            (20, 'I let other people take charge of things.'),
            (21, 'I try to have close relationships with people.'),
            (22, 'I let other people strongly influence my actions.'),
            (23, 'I try to get close and personal with people.'),
            (24, 'I let other people control my actions.'),
            (25, 'I act cool and distant with people.'),
            (26, 'I am easily led by people.'),
            (27, 'I try to have close, personal relationships with people.'),
            (28, 'I like people to invite me to things.'),
            (29, 'I like people to act close and personal with me.'),
            (30, 'I try to influence strongly other people\'s actions.'),
            (31, 'I like people to invite me to join in their activities.'),
            (32, 'I like people to act close toward me.'),
            (33, 'I try to take charge of things when I am with people.'),
            (34, 'I like people to include me in their activities.'),
            (35, 'I like people to act cool and distant toward me.'),
            (36, 'I like to have other people do things the way I want them done.'),
            (37, 'I like people to ask me to participate in their discussions.'),
            (38, 'I like people to act friendly toward me.'),
            (39, 'I like people to invite me to participate in activities.'),
            (40, 'I like people to act distant toward me.')
        )),
        OrderedDict((
            (41, 'I try to be the dominant person when I am with people.'),
            (42, 'I like people to invite me to things.'),
            (43, 'I like people to act close toward me.'),
            (44, 'I like to have other people do things I want done.'),
            (45, 'I like people to invite me to join their activities.'),
            (46, 'I like people to act cool and distant toward me.'),
            (47, 'I try to influence strongly other people\'s actions.'),
            (48, 'I like people to include me in their activities.'),
            (49, 'I like people to act close and personal with me.'),
            (50, 'I try to take charge of things when I\'m with people.'),
            (51, 'I like people to invite me to participate in activities.'),
            (52, 'I like people to act distant toward me.'),
            (53, 'I try to have other people do things the way I want them done.'),
            (54, 'I take charge of things when I\'m with people.')
        ))
    )
    
    scoring_table = {
        'expressed_inclusion': (
            (1, 1, 3), (3, 1, 4), (5, 1, 4), (7, 1, 3),
            (9, 1, 2), (11, 1, 2), (13, 1, 2), (15, 1, 1),
            (16, 1, 1)
        ),
        'wanted_inclusion': (
            (28, 1, 2), (31, 1, 2), (34, 1, 2), (37, 1, 1),
            (39, 1, 1), (42, 1, 2), (45, 1, 2), (48, 1, 2),
            (51, 1, 2)
        ),
        'expressed_control': (
            (30, 1, 3), (33, 1, 3), (36, 1, 2), (41, 1, 4),
            (44, 1, 3), (47, 1, 3), (50, 1, 2), (53, 1, 2),
            (54, 1, 2)
        ),
        'wanted_control': (
            (2, 1, 4), (6, 1, 4), (10, 1, 3), (14, 1, 3),
            (18, 1, 3), (20, 1, 3), (22, 1, 4), (24, 1, 3),
            (26, 1, 3)
        ),
        'expressed_affection': (
            (4, 1, 2), (8, 1, 2), (12, 1, 1), (17, 1, 2),
            (19, 4, 6), (21, 1, 2), (23, 1, 2), (25, 4, 6),
            (27, 1, 2)
        ),
        'wanted_affection': (
            (29, 1, 2), (32, 1, 2), (35, 5, 6), (38, 1, 2),
            (40, 5, 6), (43, 1, 1), (46, 5, 6), (49, 1, 2),
            (52, 5, 6)
        )
    }

    def __init__(self):
        self.n_pages = len(self.question_text)

    def set_submission(self, submission):
        self.submission = submission
        
        if self.submission is None:
            current_page = 0
        else:
            current_page = self.submission.current_page       
            
        self.questions = []
        
        for qid, text in self.question_text[current_page].items():
            cls = question_cls_list[current_page]
            self.questions.append(cls(qid, text))           
           
    def compute_metrics(self):
        self.metrics = {}
        
        for metric_name, items in self.scoring_table.items():
            score = 0
            
            for qid, a, b in items:
                ans = int(self.answers[qid])
                if a <= ans and ans <= b:
                    score += 1
                    
            self.metrics[metric_name] = score
            
        modifiers = ('expressed', 'wanted')
        categories = ('inclusion', 'control', 'affection')
        
        self.metrics['social_interaction_index'] = 0
            
        for modifier in modifiers:
            key = 'total_' + modifier
            self.metrics[key] = 0
            
            for category in categories:
                key2 = modifier + '_' + category
                self.metrics[key] += self.metrics[key2]
                
            self.metrics['social_interaction_index'] += self.metrics[key]
                
        for category in categories:
            key = 'total_' + category
            self.metrics[key] = 0
            
            for modifier in modifiers:
                key2 = modifier + '_' + category
                self.metrics[key] += self.metrics[key2]
            
    def review_process_metrics(self, data, metrics):          
        data['metrics'] = []
        
        for metric in metrics:
            data['metrics'].append(
                {'key': metric.key, 'value': int(metric.value)})

    
        
