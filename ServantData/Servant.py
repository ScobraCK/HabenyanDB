import json
from pprint import pprint

flag_servant = ['id', 'collectionNo', 'name', 'className', 'rarity', 'cost', 'attribute',
        'starAbsorb', 'starGen', 'instantDeathChance', 'cards', 'hitsDistribution',
        'atkBase', 'atkMax', 'hpBase', 'hpMax', 'atkGrowth', 'hpGrowth', 'bondGrowth', 'expGrowth']


class Servant:
    def __init__(self, servant_dict):
        for key in servant_dict and flag_servant:
            setattr(self, key, servant_dict[key])


if __name__ == '__main__':
    with open('test.json', 'r', encoding='utf-8') as f:
        parsed = json.loads(f.read())
        a = Servant(parsed)

        #pprint(a.__dict__, sort_dicts=False)
        print(parsed['skills'][2]['functions'][1])

