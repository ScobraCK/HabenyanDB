from Templates import *
import ServantData.Buffs.FunctionInput as buffs

remap = {'collectionNo': 'collection_no', 'className': 'class_name',
        'starAbsorb': 'star_absorb', 'starGen': 'star_gen',
         'instantDeathChance': 'death_chance','hitsDistribution': 'hit_distribution',
        'atkBase': 'atk_base', 'atkMax': 'atk_max', 'hpBase': 'hp_base', 'hpMax': 'hp_max',
         'atkGrowth': 'atk_growth', 'hpGrowth': 'hp_growth',
         'bondGrowth': 'bond', 'expGrowth': 'exp'}


def servant_input(servant_data: dict):
    # Beasts
    exceptions = [1700100, 9935400, 9935500, 9935530, 9939130, 9941730]
    if servant_data['id'] in exceptions:
        remapped = {remap.get(k, k): v for (k, v) in servant_data.items()}
        return from_dict(data_class=ServantInput, data=remapped)

    remapped = {remap.get(k, k): v for (k, v) in servant_data.items()}
    servant_dict = from_dict(data_class=ServantInput, data=remapped).__dict__

    servant_dict['skills'] = skill_input(servant_data['skills'])

    np_data = servant_data['noblePhantasms']
    servant_dict['np_gain'] = np_data[0]['npGain']['np'][0]
    servant_dict['np_gain_hit'] = np_data[0]['npGain']['defence'][0]

    return from_dict(data_class=Servant, data=servant_dict)


def skill_input(skill_data: dict):
    skill_dict = {1: [], 2: [], 3: []}
    for sk in skill_data:
        sk['cooldown'] = sk.pop('coolDown')
        skill_obj = from_dict(data_class=Skill, data=sk)  # dataclass obj

        # add buff list
        buff_list = []
        for buff_func in sk['functions']:
            buff_obj = buff_input(buff_func)
            if buff_obj:
                buff_list.append(buff_obj)
        skill_obj.buff_list = buff_list

        skill_dict[skill_obj.num].append(skill_obj)
    return skill_dict


def buff_input(buff_func):
    buff_data = buffs.get_description(buff_func)
    if buff_data:
        return Buff(*buff_data)


if __name__ == '__main__':
    import json
    from pprint import pprint

    with open('servant_data_KR.json', 'r', encoding='utf-8') as f:
        parsed = json.loads(f.read())
        for i, s in enumerate(parsed, 1):
            t = servant_input(s)

            # Beasts
            exceptions = [1700100, 9935400, 9935500, 9935530, 9939130, 9941730]
            if t.id in exceptions:
                continue

            print(f'{i}: {t.name}\n---------------')
            skills = t.skills

            print('1스킬\n---------------')
            for skill in skills[1]:
                print(skill.name)
                for buff in skill.buff_list:
                    print(buff.description, buff.level)

            print('2스킬\n---------------')
            for skill in skills[2]:
                print(skill.name)
                for buff in skill.buff_list:
                    print(buff.description, buff.level)

            print('3스킬\n---------------')
            for skill in skills[3]:
                print(skill.name)
                for buff in skill.buff_list:
                    print(buff.description, buff.level)
            print()


