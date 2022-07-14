from ServantData.Templates import *

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
np_type = ['gainNp']

target_translate = {'self': '자기 자신', 'ptOne': '아군 한 명', 'ptAll': '아군 전체',
                    'enemyAll': '적군 전체', 'enemy': '적 하나', 'ptOther': '자기 자신 제외 아군 전체'}


def buff_function_input(buff_func: dict):
    remapped = {remap.get(k, k): v for (k, v) in buff_func.items()}
    buff = from_dict(data_class=SkillFunction, data=remapped)
    if buff.type not in non_buff:
        buff.buff_type = buff_func['buffs'][0]['type']
        if buff.svals.Value2:
            buff.name = buff_func['buffs'][0]['detail']
            # 상태 해제 특수 경우 처리 해야함
    if buff.type == 'gainHp':
        buff.name = "HP 회복"

    return buff


def buff_description(buff: SkillFunction) -> (str, List[str]):
    description = ""
    rate_flag = False
    count_flag = False
    value_flag = False
    lv_flag_count = 0
    nested = False

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
        description += f'{int(rate/10)}% 확률로 '

    # target
    if buff.type != target_ex:
        # temp solution
        if buff.target_type in target_translate.keys():
            description += f'{target_translate[buff.target_type]}'
        else:
            description += "NOT IMPLEMENTED"

    # effect
    description += f' [{buff.name}]'

    # apply text
    if buff.svals.Value2:
        description += f' 부여'

    if buff.buff_type:
        buff_limit = " ("
        has_count = False
        # count
        if not count_flag and (count := buff.svals.Count[0]) > 0:
            buff_limit += f'{count}회'
            has_count = True
        # turns
        if (turn := buff.svals.Turn[0]) > 0:
            if has_count:
                buff_limit += ', '
            buff_limit += f'{turn}턴'
        buff_limit += ')'
        description += buff_limit

    if lv_flag_count != 0:
        description += f' <LEVEL>'

    # level
    lv = ['-'] * 10

    if lv_flag_count == 1:
        if rate_flag:
            lv = clean_lv([x/10 for x in buff.svals.Rate])
        elif value_flag:
            if buff.buff_type and buff.buff_type not in non_percent:
                lv = clean_lv([x/10 for x in buff.svals.Value])
            elif buff.type in np_type:
                lv = clean_lv([x/100 for x in buff.svals.Value])
            else:
                lv = buff.svals.Value
        else:
            lv = buff.svals.Count
    elif lv_flag_count == 2:
        print('Exception need for multiple lv values')
        return "None", [1], 'N/A'

    return description, lv, buff.icon


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

    test = {"funcId": 1169, "funcType": "addState", "funcTargetType": "self", "funcTargetTeam": "playerAndEnemy", "funcPopupText": "마력방출 준비", "funcPopupIcon": "https://static.atlasacademy.io/KR/BuffIcons/bufficon_331.png", "functvals": [], "funcquestTvals": [], "funcGroup": [], "buffs": [ { "id": 342, "name": "마력방출 준비", "detail": "1턴 경과 후 공격력 UP", "icon": "https://static.atlasacademy.io/KR/BuffIcons/bufficon_331.png", "type": "delayFunction", "buffGroup": 342, "script": {}, "vals": [ { "id": 3004, "name": "buffPositiveEffect" }, { "id": 3027, "name": "buffAtkUp" } ], "tvals": [], "ckSelfIndv": [], "ckOpIndv": [], "maxRate": 0 } ], "svals": [ { "Rate": 5000, "Turn": 1, "Count": -1, "Value": 960408, "Value2": 1 }, { "Rate": 5000, "Turn": 1, "Count": -1, "Value": 960408, "Value2": 2 }, { "Rate": 5000, "Turn": 1, "Count": -1, "Value": 960408, "Value2": 3 }, { "Rate": 5000, "Turn": 1, "Count": -1, "Value": 960408, "Value2": 4 }, { "Rate": 5000, "Turn": 1, "Count": -1, "Value": 960408, "Value2": 5 }, { "Rate": 5000, "Turn": 1, "Count": -1, "Value": 960408, "Value2": 6 }, { "Rate": 5000, "Turn": 1, "Count": -1, "Value": 960408, "Value2": 7 }, { "Rate": 5000, "Turn": 1, "Count": -1, "Value": 960408, "Value2": 8 }, { "Rate": 5000, "Turn": 1, "Count": -1, "Value": 960408, "Value2": 9 }, { "Rate": 5000, "Turn": 1, "Count": -1, "Value": 960408, "Value2": 10 } ] }
    test2 = { "funcId": 5217, "funcType": "subState", "funcTargetType": "self", "funcTargetTeam": "playerAndEnemy", "funcPopupText": "죽음의 구렁 해제", "functvals": [], "funcquestTvals": [], "funcGroup": [], "traitVals": [ { "id": 2613, "name": "unknown" } ], "buffs": [], "svals": [ { "Rate": 5000 }, { "Rate": 5000 }, { "Rate": 5000 }, { "Rate": 5000 }, { "Rate": 5000 }, { "Rate": 5000 }, { "Rate": 5000 }, { "Rate": 5000 }, { "Rate": 5000 }, { "Rate": 5000 } ] }
    test3 = { "funcId": 3855, "funcType": "subState", "funcTargetType": "ptOne", "funcTargetTeam": "playerAndEnemy", "funcPopupText": "약화 효과 해제", "functvals": [], "funcquestTvals": [], "funcGroup": [], "traitVals": [ { "id": 3005, "name": "buffNegativeEffect" } ], "buffs": [], "svals": [ { "Rate": 1000, "Value": 0, "Value2": 1 }, { "Rate": 1000, "Value": 0, "Value2": 1 }, { "Rate": 1000, "Value": 0, "Value2": 1 }, { "Rate": 1000, "Value": 0, "Value2": 1 }, { "Rate": 1000, "Value": 0, "Value2": 1 }, { "Rate": 1000, "Value": 0, "Value2": 1 }, { "Rate": 1000, "Value": 0, "Value2": 1 }, { "Rate": 1000, "Value": 0, "Value2": 1 }, { "Rate": 1000, "Value": 0, "Value2": 1 }, { "Rate": 1000, "Value": 0, "Value2": 1 } ] }
    print(get_description(test))
    print(get_description(test2))
    print(get_description(test3))
