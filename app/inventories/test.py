from django.test import TestCase

from big_five import BigFive
from core_self import CoreSelf

def set_answers(inv, answers):
    inv.answers = {}
        
    i = 1
    for answer in answers:
        inv.answers[i] = answer
        i += 1


class InventoryScoringTest(TestCase):

    def generic_test(self, inv, answers, expected_metrics):
        set_answers(inv, answers)
        
        inv.compute_metrics()
        self.assertEqual(expected_metrics, inv.metrics)

    def test_big_five(self):
        answers = '2615472635'
            
        expected_metrics = {
            'extraversion': -5,
            'agreeableness': -4,
            'conscientiousness': -5,
            'emotional_stability': -2,
            'openness': -1
        }  
        
        self.generic_test(BigFive(), answers, expected_metrics)
        
    def test_core_self(self):
        answers = '454454423244'         
        expected_metrics = {'score': 3}  
        
        self.generic_test(CoreSelf(), answers, expected_metrics)
        
