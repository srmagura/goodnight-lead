from django.test import TestCase

from app.inventories.big_five import BigFive
from app.inventories.core_self import CoreSelf
from app.inventories.career_commitment import CareerCommitment
from app.inventories.ambiguity import Ambiguity


class InventoryScoringTest(TestCase):

    def generic_test(self, inv, answers, expected_metrics):
        self.set_answers(inv, answers)
                
        inv.compute_metrics()
        self.assertEqual(expected_metrics, inv.metrics)
        
    def set_answers(self, inv, answers):
        if type(answers) is dict:
            inv.answers = answers
        else:
            inv.answers = {}
            i = 1
            for answer in answers:
                inv.answers[i] = answer
                i += 1


class SimpleTest(InventoryScoringTest):

    def test_big_five(self):
        answers = '2615472635'
            
        expected_metrics = {
            'extraversion': 1.5,
            'agreeableness': 2,
            'conscientiousness': 1.5,
            'emotional_stability': 3,
            'openness': 3.5
        }  
        
        self.generic_test(BigFive(), answers, expected_metrics)
        
    def test_core_self(self):
        answers = '454454423244'         
        expected_metrics = {'score': 39/12.}  
        
        self.generic_test(CoreSelf(), answers, expected_metrics)
        
    def test_career_commitment(self):
        answers = '43252422'
        expected_metrics = {
            'identity': 4,
            'planning': 4
        }
        
        self.generic_test(CareerCommitment(), answers, expected_metrics)
        
    def test_ambiguity(self):
        answers = '2343255727467626'
        expected_metrics = {'score': 49}
        
        self.generic_test(Ambiguity(), answers, expected_metrics)
