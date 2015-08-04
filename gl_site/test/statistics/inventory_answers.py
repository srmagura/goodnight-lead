import random

def _get_answers(n_questions, min, max):
    """
    Generate a random answer dictionary for an inventory.

    Answers are chosen randomly from random.randrange(min, max+1).

    n_questions -- number of questions in the inventory
    """
    result = {}

    for i in range(1, n_questions+1):
        result[i] = random.randrange(min, max+1)

    return result

def get_answers(class_name):
    """
    Return a random answer dictionary for the inventory whose Python
    class name matches `class_name`.
    """
    if class_name == 'BigFive':
        return _get_answers(10, 1, 7)
    elif class_name == 'CoreSelf':
        return _get_answers(12, 1, 5)
    elif class_name == 'CareerCommitment':
        return _get_answers(8, 1, 5)
    elif class_name == 'Ambiguity':
        return _get_answers(16, 1, 7)
    elif class_name == 'FiroB':
        return _get_answers(54, 1, 6)
    elif class_name == 'Via':
        return _get_answers(120, 1, 5)
