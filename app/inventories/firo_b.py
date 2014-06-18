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
        {
            1: 'I try to be with people.',
            2: 'I let other people decide what to do.',
            3: 'I join social groups.',
            4: 'I try to have close relationships with people.',
            5: 'I tend to join social organizations when I have an opportunity.',
            6: 'I let other people strongly influence my actions.',
            7: 'I try to be included in informal social activities.',
            8: 'I try to have close, personal relationships with people.',
            9: 'I try to include other people in my plans.',
            10: 'I let other people control my actions.',
            11: 'I try to have people around me.',
            12: 'I try to get close and personal with people.',
            13: 'When people are doing things together I tend to join in.',
            14: 'I am easily led by people.',
            15: 'I try to avoid being alone.',
            16: 'I try to participate in group activities.'
        },
        {
            17: 'I try to be friendly to people.',
            18: 'I let other people decide what to do.',
            19: 'My personal relations with people are cool and distant.',
            20: 'I let other people take charge of things.',
            21: 'I try to have close relationships with people.',
            22: 'I let other people strongly influence my actions.',
            23: 'I try to get close and personal with people.',
            24: 'I let other people control my actions.',
            25: 'I act cool and distant with people.',
            26: 'I am easily led by people.',
            27: 'I try to have close, personal relationships with people.',
            28: 'I like people to invite me to things.',
            29: 'I like people to act close and personal with me.',
            30: 'I try to influence strongly other people\'s actions.',
            31: 'I like people to invite me to join in their activities.',
            32: 'I like people to act close toward me.',
            33: 'I try to take charge of things when I am with people.',
            34: 'I like people to include me in their activities.',
            35: 'I like people to act cool and distant toward me.',
            36: 'I like to have other people do things the way I want them done.',
            37: 'I like people to ask me to participate in their discussions.',
            38: 'I like people to act friendly toward me.',
            39: 'I like people to invite me to participate in activities.',
            40: 'I like people to act distant toward me.'
        },
        {
            41: 'I try to be the dominant person when I am with people.',
            42: 'I like people to invite me to things.',
            43: 'I like people to act close toward me.',
            44: 'I like to have other people do things I want done.',
            45: 'I like people to invite me to join their activities.',
            46: 'I like people to act cool and distant toward me.',
            47: 'I try to influence strongly other people\'s actions.',
            48: 'I like people to include me in their activities.',
            49: 'I like people to act close and personal with me.',
            50: 'I try to take charge of things when I\'m with people.',
            51: 'I like people to invite me to participate in activities.',
            52: 'I like people to act distant toward me.',
            53: 'I try to have other people do things the way I want them done.',
            54: 'I take charge of things when I\'m with people.'
        }
    )

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
            
    def review_process_metrics(self, data, metrics):          
        pass

    
        
