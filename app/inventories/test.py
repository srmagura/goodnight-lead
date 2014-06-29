from django.test import TestCase

from big_five import BigFive
from core_self import CoreSelf
from career_commitment import CareerCommitment
from ambiguity import Ambiguity
from firo_b import FiroB

def set_answers(inv, answers):
    if type(answers) is dict:
        inv.answers = answers
    else:
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
        
    # Check that all question ID's appear in the table exactly once
    def test_firo_b_scoring_table(self):
        qid_list = []
        for items in FiroB.scoring_table.values():
            for qid, a, b in items:
                qid_list.append(qid)
                
        qid_list.sort()
        self.assertEqual(tuple(qid_list), tuple(range(1, 55)))
        
    def test_firo_b0(self):
        answers = {
            1: 2, 2: 2, 3: 4, 4: 3, 5: 4,
            6: 5, 7: 3, 8: 3, 9: 3, 10: 6,
            11: 2, 12: 4, 13: 3, 14: 2, 15: 3, 
            16: 3, 17: 1, 18: 3, 19: 2, 20: 3,
            21: 4, 22: 5, 23: 4, 24: 6, 25: 4,
            26: 3, 27: 4, 28: 3, 29: 2, 30: 5,
            31: 3, 32: 3, 33: 3, 34: 3, 35: 4,
            36: 2, 37: 2, 38: 1, 39: 3, 40: 5, 
            41: 5, 42: 3, 43: 3, 44: 3, 45: 2,
            46: 5, 47: 5, 48: 2, 49: 3, 50: 4,
            51: 2, 52: 4, 53: 2, 54: 3
        }
        
        expected_metrics = {
            'expressed_inclusion': 5,
            'wanted_inclusion': 3,
            'expressed_control': 4,
            'wanted_control': 5,
            'expressed_affection': 2,
            'wanted_affection': 4,
            'total_expressed': 11,
            'total_wanted': 12,
            'total_inclusion': 8,
            'total_control': 9,
            'total_affection': 6,
            'social_interaction_index': 23          
        }
        
        self.generic_test(FiroB(), answers, expected_metrics)
        
    def test_firo_b1(self):
        answers = {
            1: 2, 2: 2, 3: 1, 4: 1, 5: 3,
            6: 3, 7: 2, 8: 1, 9: 2, 10: 5,
            11: 2, 12: 1, 13: 4, 14: 3, 15: 4,
            16: 2, 17: 2, 18: 3, 19: 3, 20: 3,
            21: 1, 22: 3, 23: 1, 24: 4, 25: 3, 26: 3,
            27: 1, 28: 1, 29: 1, 30: 2, 31: 1,
            32: 1, 33: 3, 34: 1, 35: 4, 36: 1,
            37: 1, 38: 1, 39: 1, 40: 5, 41: 3,
            42: 1, 43: 1, 44: 1, 45: 1, 46: 5,
            47: 3, 48: 1, 49: 1, 50: 3, 51: 1,
            52: 5, 53: 1, 54: 3
        }

        expected_metrics = {
            'expressed_inclusion': 6,
            'wanted_inclusion': 9,
            'expressed_control': 7,
            'wanted_control': 7,
            'expressed_affection': 7,
            'wanted_affection': 8,
            'total_expressed': 20,
            'total_wanted': 24,
            'total_inclusion': 15,
            'total_control': 14,
            'total_affection': 15,
            'social_interaction_index': 44       
        }
        
        self.generic_test(FiroB(), answers, expected_metrics)
        
