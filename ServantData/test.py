import json
from pprint import pprint

if __name__ == '__main__':
    with open('servant_data_KR.json', 'r', encoding='utf-8') as f:
        parsed = json.loads(f.read())

        # script condition
        # for servant in parsed:
        #     skills = servant['skills']
        #     for skill in skills:
        #         if skill['script']:
        #             print(servant['collectionNo'])
        #
        # print()

        normal = ['Rate', 'Turn', 'Count', 'Value']
        flag = False
        #
        # non_normal svals
        for servant in sorted(parsed, key=(lambda x: x['collectionNo'])):
            flag = False
            skills = servant['skills']
            for skill in skills:
                funcs = skill['functions']
                for func in funcs:
                    for key in list(func['svals'][0].keys()):
                        if key not in normal:
                            print(servant['name'], func['svals'][0].keys())
                            # flag = True
                            break
                    if flag:
                        break
                if flag:
                    break

        #
        # something like gender condition
        # print()
        # for servant in sorted(parsed, key=(lambda x: x['collectionNo'])):
        #     flag = False
        #     skills = servant['skills']
        #     for skill in skills:
        #         funcs = skill['functions']
        #         for func in funcs:
        #             if func['functvals']:
        #                 print(servant['collectionNo'], func['functvals'])
        #                 flag = True
        #                 break
        #
        #         if flag:
        #             break
        #
        # sval test
        # print()
        # for servant in sorted(parsed, key=(lambda x: x['collectionNo'])):
        #     flag = False
        #     skills = servant['skills']
        #     for skill in skills:
        #         funcs = skill['functions']
        #         for func in funcs:
        #             if 'Count' not in list(func['svals'][0].keys()):
        #                 print(servant['collectionNo'], func['svals'][0].keys())
        #                 flag = True
        #                 break
        #
        #         if flag:
        #             break

        # non buff functypes
        # print()
        # a = set()
        # for servant in sorted(parsed, key=(lambda x: x['collectionNo'])):
        #
        #     skills = servant['skills']
        #     for skill in skills:
        #         funcs = skill['functions']
        #         for func in funcs:
        #             if not func['buffs']:
        #                 print(servant['name'], func['funcType'])
        #                 a.add(func['funcType'])
        # print(a)

        # value2
        # print()
        # for servant in sorted(parsed, key=(lambda x: x['collectionNo'])):
        #     flag = False
        #     skills = servant['skills']
        #     for skill in skills:
        #         funcs = skill['functions']
        #         for func in funcs:
        #             if 'Value2' in list(func['svals'][0].keys()) and not func['buffs']:
        #                 print(servant['name'])
        #                 flag = True
        #                 break
        #         if flag:
        #             break

        # normal = ['Rate', 'Turn', 'Count', 'Value']
        # flag = False
        #
        # # non_normal NP svals
        # for servant in sorted(parsed, key=(lambda x: x['collectionNo'])):
        #     flag = False
        #     nps = servant['noblePhantasms']
        #     for np in nps:
        #         funcs = np['functions']
        #         for func in funcs:
        #             for key in list(func['svals'][0].keys()):
        #                 if key not in normal:
        #                     print(servant['name'], func['svals'][1].keys())
        #
