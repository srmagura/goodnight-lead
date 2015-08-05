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
