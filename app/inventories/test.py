from django.test import TestCase

from big_five import BigFive

class InventoryScoringTest(TestCase):

    def test_big_five(self):
        inv = BigFive()
        inv.answers = {
            1: '2',
            2: '6',
            3: '1',
            4: '5',
            5: '4',
            6: '7',
            7: '2',
            8: '6',
            9: '3',
            10: '5'
        }
        
        inv.compute_metrics()
        
        expected_metrics = {
            'extraversion': -5,
            'agreeableness': -4,
            'conscientiousness': -5,
            'emotional_stability': -2,
            'openness': -1
        }
        
        self.assertEqual(expected_metrics, inv.metrics)
        
