via_categories = {
    'Wisdom and Knowledge': ['Creativity', 'Curiosity', 'Open Mindedness', 'Love Of Learning', 'Perspective'],
    'Courage': ['Bravery', 'Perserverance', 'Integrity', 'Vitality'],
    'Humanity': ['Love', 'Kindness', 'Social Intelligence'],
    'Justice': ['Citizenship', 'Fairness', 'Leadership'],
    'Temperance': ['Forgiveness', 'Humility', 'Prudence', 'Self Regulation'],
    'Transcendence': ['Appreciation of Beauty', 'Gratitude', 'Hopefulness', 'Humour', 'Spirituality']
}
via_inverse = {}
for key, value in via_categories.items():
    for category in value:
        via_inverse[category] = key
