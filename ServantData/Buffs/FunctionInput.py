from BuffTemplate import *

remap = {'funcType': 'type', 'funcTargetType': 'target_type',
                   'funcTargetTeam': 'target_team', 'funcPopupText': 'name',
                   'funcPopupIcon': 'icon'}
target_ally = ['self', 'ptOne', 'ptAll', 'ptOther', 'ptOneOther', 'ptSelfAnotherFirst']
non_buff = ['gainNpBuffIndividualSum', 'delayNpturn', 'cardReset', 'lossHpSafe',
            'gainHpFromTargets', 'gainStar', 'subState', 'lossStar', 'absorbNpturn',
            'hastenNpturn', 'gainNpFromTargets', 'none', 'shortenSkill', 'gainNp',
            'fixCommandcard', 'gainHp', 'lossNp']

# target exception
target_ex = ['gainStar']

# buff types
non_percent = []
np_type = []

target_translate = {'self': '자기 자신', 'ptOne': '아군 한 명', 'ptAll': '아군 전체'}


def buff_function_input(buff_func: dict):
    remapped = {remap.get(k, k): v for (k, v) in buff_func.items()}
    buff = from_dict(data_class=SkillFunction, data=remapped)
    if buff.type not in non_buff:
        buff.buff_type = buff_func['buffs'][0]['type']

    return buff


def buff_description(buff: SkillFunction) -> (str, List[str]):
    description = ""
    rate_flag = False
    count_flag = False
    value_flag = False
    lv_flag_count = 0
    nested = False

    if buff.svals.Value2:
        print('Not implemented')
        return None

    # Ignore case for enemy only targets
    if (buff.target_type in target_ally) and (buff.target_team == 'enemy'):
        return None

    # check what changes per lv
    if buff.svals.Rate[0] != buff.svals.Rate[-1]:
        lv_flag_count += 1
        rate_flag = True
    if val := buff.svals.Count:
        if val[0] != val[-1]:
            lv_flag_count += 1
            count_flag = True
    if val := buff.svals.Value:
        if val[0] != val[-1]:
            lv_flag_count += 1
            value_flag = True

    # rate
    if not rate_flag and (rate := buff.svals.Rate[0]) != 1000:
        description += f'{rate/10}% 확률로 '

    # target
    if buff.type != target_ex:
        description += f'{target_translate[buff.target_type]}'

    # effect
    description += f' [{buff.name}]'

    if buff.buff_type:
        # turns
        if (turn := buff.svals.Turn[0]) > 0:
            description += f' ({turn}턴)'

    if lv_flag_count != 0:
        description += f'<LEVEL>'

    # level
    lv = ['-'] * 10

    if lv_flag_count == 1:
        if rate_flag:
            lv = clean_lv([x/10 for x in buff.svals.Rate])
        elif value_flag:
            if buff.buff_type and buff.buff_type not in non_percent:
                lv = clean_lv([x/10 for x in buff.svals.Value])
            else:
                lv = buff.svals.Value
        else:
            lv = buff.svals.Count
    elif lv_flag_count == 2:
        print('Exception need for multiple lv values')
        return None

    return description, lv


def clean_lv(lv: list):
    flag = True
    for x in lv:
        if int(x) != x:
            flag = False
            break
    if flag:
        return [int(x) for x in lv]
    else:
        return lv


def get_description(buff_func):
    buff = buff_function_input(buff_func)
    return buff_description(buff)


test = {'funcId': 152, 'funcType': 'addStateShort', 'funcTargetType': 'ptAll', 'funcTargetTeam': 'playerAndEnemy', 'funcPopupText': '공격력 UP', 'funcPopupIcon': 'https://static.atlasacademy.io/KR/BuffIcons/bufficon_300.png', 'functvals': [], 'funcquestTvals': [], 'funcGroup': [], 'buffs': [{'id': 126, 'name': '공격력 UP', 'detail': '공격력 UP', 'icon': 'https://static.atlasacademy.io/KR/BuffIcons/bufficon_300.png', 'type': 'upAtk', 'buffGroup': 0, 'script': {}, 'vals': [{'id': 3004, 'name': 'buffPositiveEffect'}, {'id': 3006, 'name': 'buffIncreaseDamage'}, {'id': 3027, 'name': 'buffAtkUp'}], 'tvals': [], 'ckSelfIndv': [], 'ckOpIndv': [], 'maxRate': 5000}], 'svals': [{'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 90}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 99}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 108}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 117}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 126}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 135}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 144}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 153}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 162}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 180}]}
test2 = {'funcId': 120, 'funcType': 'addStateShort', 'funcTargetType': 'self', 'funcTargetTeam': 'playerAndEnemy', 'funcPopupText': '버스터 UP', 'funcPopupIcon': 'https://static.atlasacademy.io/KR/BuffIcons/bufficon_314.png', 'functvals': [], 'funcquestTvals': [], 'funcGroup': [], 'buffs': [{'id': 102, 'name': '버스터 UP', 'detail': '버스터 카드의 성능 UP', 'icon': 'https://static.atlasacademy.io/KR/BuffIcons/bufficon_314.png', 'type': 'upCommandall', 'buffGroup': 0, 'script': {}, 'vals': [{'id': 3004, 'name': 'buffPositiveEffect'}, {'id': 3006, 'name': 'buffIncreaseDamage'}], 'tvals': [{'id': 5000, 'name': 'canBeInBattle'}, {'id': 4002, 'name': 'cardBuster'}], 'ckSelfIndv': [{'id': 4002, 'name': 'cardBuster'}], 'ckOpIndv': [], 'maxRate': 5000}], 'svals': [{'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 300}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 320}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 340}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 360}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 380}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 400}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 420}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 440}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 460}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 500}]}
test3 = {'funcId': 476, 'funcType': 'gainStar', 'funcTargetType': 'self', 'funcTargetTeam': 'player', 'funcPopupText': '스타 획득', 'functvals': [], 'funcquestTvals': [], 'funcGroup': [], 'buffs': [], 'svals': [{'Rate': 1000, 'Value': 5}, {'Rate': 1000, 'Value': 6}, {'Rate': 1000, 'Value': 7}, {'Rate': 1000, 'Value': 8}, {'Rate': 1000, 'Value': 9}, {'Rate': 1000, 'Value': 10}, {'Rate': 1000, 'Value': 11}, {'Rate': 1000, 'Value': 12}, {'Rate': 1000, 'Value': 13}, {'Rate': 1000, 'Value': 15}]}
test4 = {'funcId': 215, 'funcType': 'addStateShort', 'funcTargetType': 'self', 'funcTargetTeam': 'enemy', 'funcPopupText': '크리티컬 발생 UP', 'funcPopupIcon': 'https://static.atlasacademy.io/KR/BuffIcons/bufficon_327.png', 'functvals': [], 'funcquestTvals': [], 'funcGroup': [], 'buffs': [{'id': 144, 'name': '크리티컬 발생 UP', 'detail': '크리티컬 발생률 UP', 'icon': 'https://static.atlasacademy.io/KR/BuffIcons/bufficon_327.png', 'type': 'upCriticalrate', 'buffGroup': 0, 'script': {}, 'vals': [{'id': 3004, 'name': 'buffPositiveEffect'}, {'id': 3006, 'name': 'buffIncreaseDamage'}, {'id': 3032, 'name': 'buffCritRateUp'}], 'tvals': [], 'ckSelfIndv': [], 'ckOpIndv': [], 'maxRate': 5000}], 'svals': [{'Rate': 1000, 'Turn': 2, 'Count': -1, 'Value': 200}, {'Rate': 1000, 'Turn': 2, 'Count': -1, 'Value': 200}, {'Rate': 1000, 'Turn': 2, 'Count': -1, 'Value': 200}, {'Rate': 1000, 'Turn': 2, 'Count': -1, 'Value': 200}, {'Rate': 1000, 'Turn': 2, 'Count': -1, 'Value': 200}, {'Rate': 1000, 'Turn': 2, 'Count': -1, 'Value': 200}, {'Rate': 1000, 'Turn': 2, 'Count': -1, 'Value': 200}, {'Rate': 1000, 'Turn': 2, 'Count': -1, 'Value': 200}, {'Rate': 1000, 'Turn': 2, 'Count': -1, 'Value': 200}, {'Rate': 1000, 'Turn': 2, 'Count': -1, 'Value': 200}]}


if __name__ == '__main__':
    import json

    with open('../test.json', 'r', encoding='utf-8') as f:
        parsed = json.loads(f.read())
        skills = parsed['skills']
        for i, skill in enumerate(skills, 1):
            print(f'스킬{i}:')
            for j, func in enumerate(skill['functions'], 1):
                print(f'{j}: {get_description(func)}')
            print()
