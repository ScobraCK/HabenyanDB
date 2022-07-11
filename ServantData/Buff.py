buffExceptions = []
flag_buff = ['funcType', 'funcTargetType', 'funcTargetTeam', 'funcPopupText']
non_rate_buffs = ['gainStar']
temp_list = ['gainStar']

test = {'funcId': 152, 'funcType': 'addStateShort', 'funcTargetType': 'ptAll', 'funcTargetTeam': 'playerAndEnemy', 'funcPopupText': '공격력 UP', 'funcPopupIcon': 'https://static.atlasacademy.io/KR/BuffIcons/bufficon_300.png', 'functvals': [], 'funcquestTvals': [], 'funcGroup': [], 'buffs': [{'id': 126, 'name': '공격력 UP', 'detail': '공격력 UP', 'icon': 'https://static.atlasacademy.io/KR/BuffIcons/bufficon_300.png', 'type': 'upAtk', 'buffGroup': 0, 'script': {}, 'vals': [{'id': 3004, 'name': 'buffPositiveEffect'}, {'id': 3006, 'name': 'buffIncreaseDamage'}, {'id': 3027, 'name': 'buffAtkUp'}], 'tvals': [], 'ckSelfIndv': [], 'ckOpIndv': [], 'maxRate': 5000}], 'svals': [{'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 90}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 99}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 108}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 117}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 126}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 135}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 144}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 153}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 162}, {'Rate': 1000, 'Turn': 3, 'Count': -1, 'Value': 180}]}
test2 = {'funcId': 120, 'funcType': 'addStateShort', 'funcTargetType': 'self', 'funcTargetTeam': 'playerAndEnemy', 'funcPopupText': '버스터 UP', 'funcPopupIcon': 'https://static.atlasacademy.io/KR/BuffIcons/bufficon_314.png', 'functvals': [], 'funcquestTvals': [], 'funcGroup': [], 'buffs': [{'id': 102, 'name': '버스터 UP', 'detail': '버스터 카드의 성능 UP', 'icon': 'https://static.atlasacademy.io/KR/BuffIcons/bufficon_314.png', 'type': 'upCommandall', 'buffGroup': 0, 'script': {}, 'vals': [{'id': 3004, 'name': 'buffPositiveEffect'}, {'id': 3006, 'name': 'buffIncreaseDamage'}], 'tvals': [{'id': 5000, 'name': 'canBeInBattle'}, {'id': 4002, 'name': 'cardBuster'}], 'ckSelfIndv': [{'id': 4002, 'name': 'cardBuster'}], 'ckOpIndv': [], 'maxRate': 5000}], 'svals': [{'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 300}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 320}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 340}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 360}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 380}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 400}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 420}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 440}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 460}, {'Rate': 1000, 'Turn': 1, 'Count': -1, 'Value': 500}]}
test3 = {'funcId': 476, 'funcType': 'gainStar', 'funcTargetType': 'self', 'funcTargetTeam': 'player', 'funcPopupText': '스타 획득', 'functvals': [], 'funcquestTvals': [], 'funcGroup': [], 'buffs': [], 'svals': [{'Rate': 1000, 'Value': 5}, {'Rate': 1000, 'Value': 6}, {'Rate': 1000, 'Value': 7}, {'Rate': 1000, 'Value': 8}, {'Rate': 1000, 'Value': 9}, {'Rate': 1000, 'Value': 10}, {'Rate': 1000, 'Value': 11}, {'Rate': 1000, 'Value': 12}, {'Rate': 1000, 'Value': 13}, {'Rate': 1000, 'Value': 15}]}

class Buff:
    def __init__(self, buff_func: dict):
        # need exception like for Hyde

        for key in buff_func and flag_buff:
            setattr(self, key, buff_func[key])
        if self.funcType not in temp_list:
            self.name = buff_func['buffs'][0]['name']
            self.buffIcon = buff_func['buffs'][0]['icon']
            self.buffType = buff_func['buffs'][0]['type']
        else: #temp solution
            self.buffType = self.funcType
            self.name = buff_func['funcPopupText']

        self.rate = []
        self.turn = []
        self.count = []
        self.value = []
        self.key_map = {'Rate': self.rate, 'Turn': self.turn,
                        'Count': self.count, 'Value': self.value}
        self.lvFlag = None

        svals = buff_func['svals']
        sval_keys = list(svals[0].keys())

        for key in sval_keys:
            self.get_svals(key, svals)
        if self.buffType not in non_rate_buffs:
            self.value = [f'{x/10}%' for x in self.value]
            self.key_map['Value'] = self.value  # Don't know why this is needed

        self.description = ""

    def get_svals(self, key: str, svals: dict):
        for lv in svals:
            self.key_map[key].append(lv[key])
        if self.key_map[key][0] != self.key_map[key][-1]:
            self.lvFlag = key

    def get_description(self):
        # rate
        if self.lvFlag != 'Rate' and (rate := self.rate[0]) != 1000:
            self.description += f'{rate/10}% 확률로'

        # target
        if self.funcTargetType == 'ptAll':
            self.description += ' 아군 전체에게'
        elif self.funcTargetType == 'self':
            self.description += ' 자신에게'

        # buff type
        self.description += f' {self.name}'

        # value
        if self.lvFlag != 'Value':
            self.description += f' {self.value}%'

        self.description += ' 부여'

        return self.description

    def get_buff(self):
        description = self.get_description()
        if not self.lvFlag:
            return description, ['-']*10
        else:
            return description, self.key_map[self.lvFlag]


if __name__ == '__main__':
    b = Buff(test)
    b1 = Buff(test2)
    b2 = Buff(test3)
    print(b.get_buff())
    print(b1.get_buff())
    print(b2.get_buff())