from django.test import TestCase

from big_five import BigFive
from core_self import CoreSelf
from career_commitment import CareerCommitment
from ambiguity import Ambiguity

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
            'extraversion': 3,
            'agreeableness': 4,
            'conscientiousness': 3,
            'emotional_stability': 6,
            'openness': 7
        }  
        
        self.generic_test(BigFive(), answers, expected_metrics)
        
    def test_core_self(self):
        answers = '454454423244'         
        expected_metrics = {'score': 39}  
        
        self.generic_test(CoreSelf(), answers, expected_metrics)
        
    def test_career_commitment(self):
        answers = '43252422'
        expected_metrics = {
            'identity': 16,
            'planning': 16
        }
        
        self.generic_test(CareerCommitment(), answers, expected_metrics)
        
    def test_ambiguity(self):
        answers = '2343255727467626'
        expected_metrics = {'score': 49}
        
        self.generic_test(Ambiguity(), answers, expected_metrics)
