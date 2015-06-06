from test_inventories import InventoryScoringTest
from app.inventories.via import Via

# pylint:disable=no-member, E1002, no-init
# Disable no member and super on old style class
# warnings because pylint was having trouble finding
# members existing in superclasses imported from
# separate modules.

def print_answers(answers):
    for x in answers:
        print(x)

class ViaTest(InventoryScoringTest):

    def test_scoring_dict(self):
        self.assertEqual(len(Via().scoring_dict), 24)

    def test0(self):
        answers = (
            4, 4, 5, 2, 1, 2, 4, 3, 2, 4,
            1, 2, 3, 4, 3, 1, 2, 2, 4, 4,
            2, 4, 3, 5, 2, 3, 5, 1, 2, 4,
            5, 5, 3, 5, 5, 4, 3, 1, 3, 3,
            4, 3, 4, 2, 3, 3, 2, 4, 5, 3,
            5, 1, 1, 4, 3, 4, 3, 2, 1, 3,
            4, 1, 2, 2, 2, 3, 2, 2, 1, 2,
            1, 2, 3, 4, 2, 1, 4, 1, 2, 2,
            5, 1, 2, 5, 5, 2, 2, 5, 4, 5,
            1, 2, 1, 2, 4, 4, 3, 2, 1, 3,
            2, 1, 5, 1, 4, 5, 3, 3, 1, 5,
            1, 2, 1, 5, 5, 1, 4, 5, 5, 1
        )

        expected_metrics = {
            'creativity': 13,
            'bravery': 19,
            'perserverance': 17,
            'integrity': 17,
            'self_regulation': 12,
            'hopefulness': 14,
            'spirituality': 18,
            'social_intelligence': 17,
            'kindness': 12,
            'love': 10,
            'leadership': 13,
            'forgiveness': 15,
            'curiosity': 11,
            'love_of_learning': 13,
            'fairness': 14,
            'prudence': 13,
            'appreciation_of_beauty': 16,
            'humility': 15,
            'citizenship': 15,
            'gratitude': 15,
            'open_mindedness': 20,
            'perspective': 11,
            'vitality': 9,
            'humour': 18
        }

        self.generic_test(Via(), answers, expected_metrics)
