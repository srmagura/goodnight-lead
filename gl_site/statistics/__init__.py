via_categories = {
    'Wisdom and Knowledge': ['creativity', 'curiosity', 'open_mindedness', 'love_of_learning', 'perspective'],
    'Courage': ['bravery', 'perserverance', 'integrity', 'vitality'],
    'Humanity': ['love', 'kindness', 'social_intelligence'],
    'Justice': ['citizenship', 'fairness', 'leadership'],
    'Temperance': ['forgiveness', 'humility', 'prudence', 'self_regulation'],
    'Transcendence': ['appreciation_of_beauty', 'gratitude', 'hopefulness', 'humour', 'spirituality']
}
via_inverse = {}
for key, value in via_categories.items():
    for category in value:
        via_inverse[category] = key

inventory_keys = [
    {
        'name': 'Big Five',
        'keys': ('extraversion', 'agreeableness', 'conscientiousness', 'emotional_stability', 'openness')
    },
    {
        'name': 'Core Self Evaluation Scale',
        'keys': ('score',)
    },
    {
        'name': 'Career Commitment',
        'keys': ('identity', 'planning')
    },
    {
        'name': 'Ambiguity',
        'keys': ('score',)
    },
    {
        'name': 'FIRO-B',
        'keys': ('expressed_inclusion', 'wanted_inclusion','expressed_control', 'wanted_control', 'expressed_affection', 'wanted_affection', 'social_interaction_index'),
    },
    {
        'name': "VIA",
        'keys': (
            'creativity', 'curiosity', 'open_mindedness', 'love_of_learning', 'perspective',
            'bravery', 'perserverance', 'integrity', 'vitality', 'love', 'kindness', 'social_intelligence',
            'citizenship', 'fairness', 'leadership', 'forgiveness', 'humility', 'prudence', 'self_regulation',
            'appreciation_of_beauty', 'gratitude', 'hopefulness', 'humour', 'spirituality'
        )
    }
]
