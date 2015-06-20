# Import test case
from django.test import TestCase

# Import inventories
from gl_site.inventories.big_five import BigFive
from gl_site.inventories.core_self import CoreSelf
from gl_site.inventories.career_commitment import CareerCommitment
from gl_site.inventories.ambiguity import Ambiguity

# Test case to verify an inventory scores
# as expected.
class InventoryScoringTest(TestCase):

    # Test scoring by setting inventory answers, computing
    # metrics, and comparing actual to expected.
    #
    # Inputs:
    #   inv              - Instance of Inventory to be tested. Used to compute
    #                      metrics in comparison against expected.
    #   answers          - Pre-defined answers to the inventory questions.
    #                      Answers should correspond to expected metrics.
    #   expected_metrics - Metrics expected when the enventory scores itself.
    def generic_test(self, inv, answers, expected_metrics):
        self.set_answers(inv, answers)

        inv.compute_metrics()
        self.assertEqual(expected_metrics, inv.metrics)

    # Imports provided answers into an inventory's
    # answers dictionary.
    #
    # Inputs:
    #   inv     - Instance of Inventory which the answers will be
    #             imported to.
    #   answers - Set of pre-defined answers for an inventory.
    def set_answers(self, inv, answers):
        if type(answers) is dict:
            inv.answers = answers
        else:
            inv.answers = {}
            i = 1
            for answer in answers:
                inv.answers[i] = answer
                i += 1

# Simple test case. Tests an inventory by defining a set
# of answers and corresponding expected metrics. Verifies
# that the expected metrics match the actual metrics as
# calculated by the inventory.
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
