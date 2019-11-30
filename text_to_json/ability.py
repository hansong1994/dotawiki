import json
import os
import copy
import math


# 查询数据范围
def findtb(source, start, end, tb, brace=0):
    i = j = 0
    tb[0] = start
    tb[1] = end
    for i in range(start, end):
        if source[i] == '{':
            brace += 1
            if brace > 0:
                tb[0] = i + 1
                for j in range(i + 1, tb[1]):
                    if source[j] == '{':
                        brace += 1
                    elif source[j] == '}':
                        brace -= 1
                        if brace == 0:
                            tb[1] = j - 1
                            return True
        elif source[i] == '}':
            return False
    return False


def findabilityname(source, tb):
    i = source.rfind('\"', 0, tb[0])
    j = source.rfind('\"', 0, i - 1)
    return source[j + 1:i]


# 寻找属性（查询源字符串，数据存储位置，上下限，属性序数，是否为存在属性）
def findabilitypro(source, data, tb, pro, bool=False):
    if bool:
        i = source.find(pro[1], tb[0], tb[1])
        if i != -1:
            data[pro[1]] = {"1": 1}
    else:
        i = source.find('\"' + pro[1] + '\"', tb[0], tb[1])
        if i != -1:
            j = source.find('\"', i + 1, tb[1])
            j = source.find('\"', j + 1, tb[1])
            k = source.find('\"', j + 1, tb[1])
            splitit = source[j + 1:k].split(' ')
            data[pro[1]] = {}
            bool = True
            for j in range(len(splitit)):
                data[pro[1]][str(j + 1)] = float(splitit[j])
                bool = bool and splitit[0] == splitit[j]
            if bool:
                data[pro[1]] = {"1": data[pro[1]]["1"]}
    return


def findabilityspecial(source, data, tb):
    i = source.find("AbilitySpecial", tb[0], tb[1])
    if i == -1:
        return
    else:
        k = source.find("{", i, tb[1])
        while True:
            j = source.find("{", k + 1, tb[1])
            k = source.find("}", k + 1, tb[1])
            if j < k and j != -1:
                r = [0, 0, 0, 0]
                r[0] = source.find('\"', j, k) + 1
                r[0] = source.find('\"', r[0], k) + 1
                r[0] = source.find('\"', r[0], k) + 1
                r[0] = source.find('\"', r[0], k) + 1
                r[0] = source.find('\"', r[0], k) + 1
                r[1] = source.find('\"', r[0], k)
                r[2] = source.find('\"', r[1] + 1, k) + 1
                r[3] = source.find('\"', r[2], k)
                splitit = source[r[2]:r[3]].split(' ')
                if splitit[0] != '':
                    data[source[r[0]:r[1]]] = {}
                    bool = True
                    for l in range(len(splitit)):
                        data[source[r[0]:r[1]]][str(l + 1)] = float(splitit[l])
                        bool = bool and splitit[0] == splitit[l]
                    if bool:
                        data[source[r[0]:r[1]]] = {"1": data[source[r[0]:r[1]]]["1"]}
            else:
                return


def get_hero_data_from_txt(base_txt,address):
    this_file = open("E:/Steam/steamapps/common/dota 2 beta/game/dota/scripts/npc/npc_abilities.txt", mode="r")
    this_string = this_file.read()
    tb = [0, 0]
    findtb(this_string, 0, len(this_string), tb, -1)
    while (True):
        if (findtb(this_string, tb[1] + 2, len(this_string), tb, 0)):
            name = findabilityname(this_string, tb)
            base_txt[name] = {}
            for i in abilitypro_num:
                findabilitypro(this_string, base_txt[name], tb, i, False)
            for i in abilitypro_bool:
                findabilitypro(this_string, base_txt[name], tb, i, True)
            findabilityspecial(this_string, base_txt[name], tb)
        else:
            break


def get_source_to_data(all_json, upgrade_json,version):
    for ijk in all_json['技能']:
        unit_dic=copy.deepcopy(all_json['技能'][ijk])
        unit_dic["分类"] = "技能"
        unit_dic["版本"] = version
        unit_dic["应用"] = 1
        if unit_dic["技能排序"] == "":
            if unit_dic["默认按键"] == "Q":
                unit_dic["技能排序"] = "d"
            elif unit_dic["默认按键"] == "W":
                unit_dic["技能排序"] = "e"
            elif unit_dic["默认按键"] == "E":
                unit_dic["技能排序"] = "f"
            elif unit_dic["默认按键"] == "D":
                unit_dic["技能排序"] = "g"
            elif unit_dic["默认按键"] == "F":
                unit_dic["技能排序"] = "h"
            elif unit_dic["默认按键"] == "R":
                unit_dic["技能排序"] = "i"
            elif unit_dic["默认按键"] == "T":
                unit_dic["技能排序"] = "j"
            else:
                unit_dic["技能排序"] = "z"
        temp1 = copy.deepcopy(all_json['技能源'][unit_dic["数据来源"]])
        if unit_dic["次级分类"] == "天赋技能":
            unit_dic["图片"] = all_json["英雄"][unit_dic["技能归属"]]["图片"]
            unit_dic["迷你图片"] = all_json["英雄"][unit_dic["技能归属"]]["迷你图片"]
        elif unit_dic["次级分类"] == "物品技能":
            unit_dic["图片"] = all_json["物品"][unit_dic["技能归属"]]["图片"]
            unit_dic["迷你图片"] = all_json["物品"][unit_dic["技能归属"]]["迷你图片"]
        else:
            unit_dic["图片"] = "spellicons " + temp1["代码"] + ".png"
            unit_dic["迷你图片"] = "spellicons " + temp1["代码"] + ".png"
        for i in temp1:
            if i in ability_trait_level[0]:
                unit_dic[i] = temp1[i]
            elif i in ability_trait_level[1]:
                unit_dic[i] = {}
                j = 0
                while True:
                    j += 1
                    if str(j) in temp1[i]:
                        unit_dic[i][str(j)] = group_source(temp1[i][str(j)])
                    else:
                        break
            elif i in ability_trait_level[2]:
                unit_dic[i] = {}
                j = 0
                while True:
                    j += 1
                    if str(j) in temp1[i]:
                        unit_dic[i][str(j)] = {}
                        k = 0
                        while True:
                            k += 1
                            if str(k) in temp1[i][str(j)]:
                                unit_dic[i][str(j)][str(k)] = group_source(temp1[i][str(j)][str(k)])
                            else:
                                break
                        if '名称' in temp1[i][str(j)]:
                            unit_dic[i][str(j)]['名称'] = temp1[i][str(j)]['名称']
                    else:
                        break
            elif i == "升级":
                if "A杖" in temp1[i] or "技能" in temp1[i] or "混合" in temp1[i]:
                    upgrade_json[unit_dic["页面名"]] = copy.deepcopy(temp1[i])
            elif i == "页面名":
                continue
            else:
                unit_dic[i] = group_source(temp1[i])
        all_json["技能"][unit_dic["页面名"]] = copy.deepcopy(unit_dic)


def group_source(a):
    temp = {"1": {}}
    for i in a:
        if i == "名称" or i == "后缀":
            temp[i] = a[i]
        else:
            temp["1"][i] = a[i]
    return temp


def input_upgrade(all_json, upgrade_json):
    for i in upgrade_json:
        for j in upgrade_json[i]["A杖"]:
            if upgrade_json[i]["A杖"][j]["目标"]["1"] == "":
                upgrade_json[i]["A杖"][j]["目标"]["1"] = "技能"
            if upgrade_json[i]["A杖"][j]["目标"]["2"] == "":
                upgrade_json[i]["A杖"][j]["目标"]["2"] = i
            if "代码" in upgrade_json[i]["A杖"][j]["值"]:
                if "1" in upgrade_json[i]["A杖"][j]["值"]["代码"] and upgrade_json[i]["A杖"][j]["值"]["代码"]["1"] == "":
                    upgrade_json[i]["A杖"][j]["值"]["代码"]["1"] = "技能"
                if "2" in upgrade_json[i]["A杖"][j]["值"]["代码"] and upgrade_json[i]["A杖"][j]["值"]["代码"]["2"] == "":
                    upgrade_json[i]["A杖"][j]["值"]["代码"]["2"] = all_json["技能"][i]["代码"]
            k = 1
            temp = all_json[upgrade_json[i]["A杖"][j]["目标"]["1"]]
            while True:
                k += 1
                if str(k) in upgrade_json[i]["A杖"][j]["目标"]:
                    temp = temp[upgrade_json[i]["A杖"][j]["目标"][str(k)]]
                else:
                    break
            if "0" in upgrade_json[i]["A杖"][j]["目标"] and upgrade_json[i]["A杖"][j]["目标"]["0"] == "替换":
                if "2" not in temp:
                    temp["2"] = copy.deepcopy(temp["1"])
                for k in upgrade_json[i]["A杖"][j]["值"]:
                    temp["2"][k] = copy.deepcopy(upgrade_json[i]["A杖"][j]["值"][k])
            else:
                temp["2"] = upgrade_json[i]["A杖"][j]["值"]
        for j in upgrade_json[i]["技能"]:
            if "代码" in upgrade_json[i]["A杖"][j]["值"]:
                if "1" in upgrade_json[i]["A杖"][j]["值"]["代码"] and upgrade_json[i]["A杖"][j]["值"]["代码"]["1"] == "":
                    upgrade_json[i]["A杖"][j]["值"]["代码"]["1"] = "技能"
                if "2" in upgrade_json[i]["A杖"][j]["值"]["代码"] and upgrade_json[i]["A杖"][j]["值"]["代码"]["2"] == "":
                    upgrade_json[i]["A杖"][j]["值"]["代码"]["2"] = all_json["技能"][i]["代码"]
            k = 1
            temp = all_json[upgrade_json[i]["技能"][j]["目标"]["1"]]
            while True:
                k += 1
                if str(k) in upgrade_json[i]["技能"][j]["目标"]:
                    temp = temp[upgrade_json[i]["技能"][j]["目标"][str(k)]]
                else:
                    break
            if "0" in upgrade_json[i]["技能"][j]["目标"] and upgrade_json[i]["技能"][j]["目标"]["0"] == "替换":
                if "3" not in temp:
                    temp["3"] = copy.deepcopy(temp["1"])
                for k in upgrade_json[i]["技能"][j]["值"]:
                    temp["3"][k] = copy.deepcopy(upgrade_json[i]["技能"][j]["值"][k])
            else:
                temp["3"] = upgrade_json[i]["技能"][j]["值"]
            temp["3"]["升级来源"] = {"1": {"名称": i}}
            if all_json["技能"][i]["次级分类"] == "天赋技能":
                temp["3"]["升级来源"]["1"]["图片"] = "talent.png"
            else:
                temp["3"]["升级来源"]["1"]["图片"] = all_json["技能"][i]["迷你图片"]
        for j in upgrade_json[i]["混合"]:
            if "代码" in upgrade_json[i]["A杖"][j]["值"]:
                if "1" in upgrade_json[i]["A杖"][j]["值"]["代码"] and upgrade_json[i]["A杖"][j]["值"]["代码"]["1"] == "":
                    upgrade_json[i]["A杖"][j]["值"]["代码"]["1"] = "技能"
                if "2" in upgrade_json[i]["A杖"][j]["值"]["代码"] and upgrade_json[i]["A杖"][j]["值"]["代码"]["2"] == "":
                    upgrade_json[i]["A杖"][j]["值"]["代码"]["2"] = all_json["技能"][i]["代码"]
            k = 1
            temp = all_json[upgrade_json[i]["混合"][j]["目标"]["1"]]
            while True:
                k += 1
                if str(k) in upgrade_json[i]["混合"][j]["目标"]:
                    temp = temp[upgrade_json[i]["混合"][j]["目标"][str(k)]]
                else:
                    break
            if "0" in upgrade_json[i]["混合"][j]["目标"] and upgrade_json[i]["混合"][j]["目标"]["0"] == "替换":
                if "3" not in temp:
                    temp["3"] = copy.deepcopy(temp["1"])
                for k in upgrade_json[i]["混合"][j]["值"]:
                    temp["3"][k] = copy.deepcopy(upgrade_json[i]["混合"][j]["值"][k])
            else:
                temp["3"] = upgrade_json[i]["混合"][j]["值"]
            temp["3"]["升级来源"] = {}
            for k in upgrade_json[i]["混合"][j]["来源技能"]:
                if upgrade_json[i]["混合"][j]["来源技能"][k] == "A杖":
                    temp["3"]["升级来源"][k] = {"名称": "阿哈利姆神杖", "图片": "agha.png"}
                elif upgrade_json[i]["混合"][j]["来源技能"][k] == "本技能":
                    temp["3"]["升级来源"][k] = {"名称": i}
                    if all_json["技能"][i]["次级分类"] == "天赋技能":
                        temp["3"]["升级来源"][k]["图片"] = "talent.png"
                    else:
                        temp["3"]["升级来源"][k]["图片"] = all_json["技能"][i]["迷你图片"]
                else:
                    temp["3"]["升级来源"][k] = {"名称": upgrade_json[i]["混合"][j]["来源技能"][k]}
                    if all_json["技能"][upgrade_json[i]["混合"][j]["来源技能"][k]]["次级分类"] == "天赋技能":
                        temp["3"]["升级来源"][k]["图片"] = "talent.png"
                    else:
                        temp["3"]["升级来源"][k]["图片"] = all_json["技能"][upgrade_json[i]["混合"][j]["来源技能"][k]]["迷你图片"]
    for i in all_json["技能"]:
        for j in all_json["技能"][i]["效果"]:
            for k in ["2", "3"]:
                if k in all_json["技能"][i]["效果"][j]:
                    l = 0
                    while True:
                        l += 1
                        if str(l) in all_json["技能"][i]["效果"][j][k] and all_json["技能"][i]["效果"][j][k][str(l)] == '删除':
                            m = l
                            while True:
                                m = m + 1
                                if str(m) in all_json["技能"][i]["效果"][j][k]:
                                    all_json["技能"][i]["效果"][j][k][str(m - 1)] = copy.deepcopy(all_json["技能"][i]["效果"][j][k][str(m)])
                                else:
                                    all_json["技能"][i]["效果"][j][k].pop(str(m - 1))
                                    l -= 1
                                    break
                        else:
                            break
                    m = 0
                    l -= 1
                    while True:
                        m += 1
                        l += 1
                        if "+" + str(m) in all_json["技能"][i]["效果"][j][k]:
                            all_json["技能"][i]["效果"][j][k][str(l)] = copy.deepcopy(all_json["技能"][i]["效果"][j][k]["+" + str(m)])
                            all_json["技能"][i]["效果"][j][k].pop("+" + str(m))
                        else:
                            break


def complete_upgrade(all_json, base_txt):
    for i in all_json:
        for j in all_json[i]["属性"]:
            fulfil(all_json[i]["属性"][j]["1"]["代码"], all_json[i])
            one_upgrade(all_json[i]["属性"][j], base_txt)
        for j in all_json[i]["冷却时间"]:
            if all_json[i]["冷却时间"][j]["1"]["代码"]["1"] != '不存在':
                fulfil(all_json[i]["冷却时间"][j]["1"]["代码"], all_json[i])
                one_upgrade(all_json[i]["冷却时间"][j], base_txt)
        for j in all_json[i]["魔法消耗"]:
            for k in all_json[i]["魔法消耗"][j]:
                if k != '名称':
                    if all_json[i]["魔法消耗"][j][k]["1"]["代码"]["1"] != '不存在':
                        fulfil(all_json[i]["魔法消耗"][j][k]["1"]["代码"], all_json[i])
                        one_upgrade(all_json[i]["魔法消耗"][j][k], base_txt)
        if all_json[i]["施法前摇"]["1"]["代码"]["1"] != '不存在':
            fulfil(all_json[i]["施法前摇"]["1"]["代码"], all_json[i])
            one_upgrade(all_json[i]["施法前摇"], base_txt)
        if all_json[i]["施法后摇"]["1"]["代码"]["1"] != '不存在':
            fulfil(all_json[i]["施法后摇"]["1"]["代码"], all_json[i])
            one_upgrade(all_json[i]["施法后摇"], base_txt)


def fulfil(arr, json):
    if "1" in arr and arr["1"] == "":
        arr["1"] = "技能"
    if "2" in arr and arr["2"] == "":
        arr["2"] = json["代码"]


def one_upgrade(json, base_txt):
    inbool = ["2" in json, "3" in json]
    inbool.append(inbool[0] and inbool[1])
    getvalue = [[], [], [], []]
    calvalue = [[], [], [], []]
    caloprate = [[], [], []]
    if "0" in json["1"]["代码"]:
        if json["1"]["代码"]["0"] == "手填":
            k = 0
            while True:
                k += 1
                if str(k) in json["1"]["代码"]:
                    getvalue[0].append(json["1"]["代码"][str(k)])
                else:
                    break
        elif json["1"]["代码"]["0"] == "不存在":
            return
    else:
        for k in base_txt[json["1"]["代码"]["1"]][json["1"]["代码"]["2"]][json["1"]["代码"]["3"]]:
            getvalue[0].append(base_txt[json["1"]["代码"]["1"]][json["1"]["代码"]["2"]][json["1"]["代码"]["3"]][k])
    if json["1"]["修正"]["1"] == "":
        inbool.append(False)
    else:
        inbool.append(True)
        caloprate[0].append(json["1"]["修正"]["1"])
        k = 1
        while True:
            k += 1
            if str(k) in json["1"]["修正"]:
                getvalue[1].append(json["1"]["修正"][str(k)])
            else:
                break
    if inbool[0]:
        if "0" in json["2"]["代码"] and json["2"]["代码"]["0"] == "手填":
            k = 0
            while True:
                k += 1
                if str(k) in json["2"]["代码"]:
                    getvalue[2].append(json["2"]["代码"][str(k)])
                else:
                    break
        else:
            for k in base_txt[json["2"]["代码"]["1"]][json["2"]["代码"]["2"]][json["2"]["代码"]["3"]]:
                getvalue[2].append(base_txt[json["2"]["代码"]["1"]][json["2"]["代码"]["2"]][json["2"]["代码"]["3"]][k])
        caloprate[1].append(json["2"]["修正"]["1"])
    if inbool[1]:
        if "0" in json["3"]["代码"] and json["3"]["代码"]["0"] == "手填":
            k = 0
            while True:
                k += 1
                if str(k) in json["3"]["代码"]:
                    getvalue[3].append(json["3"]["代码"][str(k)])
                else:
                    break
        else:
            for k in base_txt[json["3"]["代码"]["1"]][json["3"]["代码"]["2"]][json["3"]["代码"]["3"]]:
                getvalue[3].append(base_txt[json["3"]["代码"]["1"]][json["3"]["代码"]["2"]][json["3"]["代码"]["3"]][k])
        caloprate[2].append(json["3"]["修正"]["1"])
    calvalue[0] = copy.deepcopy(getvalue[0])
    calvalue[1] = copy.deepcopy(getvalue[0])
    calvalue[2] = copy.deepcopy(getvalue[0])
    calvalue[3] = copy.deepcopy(getvalue[0])
    if inbool[1]:
        array_cal(calvalue[2], getvalue[3], caloprate[2], -1)
        array_cal(calvalue[3], getvalue[3], caloprate[2], -1)
    if inbool[0]:
        array_cal(calvalue[1], getvalue[2], caloprate[1], 0)
        array_cal(calvalue[3], getvalue[2], caloprate[1], 0)
    if inbool[1]:
        array_cal(calvalue[2], getvalue[3], caloprate[2], 0)
        array_cal(calvalue[3], getvalue[3], caloprate[2], 0)
    if inbool[3]:
        array_cal(calvalue[0], getvalue[1], caloprate[0], 0)
        array_cal(calvalue[1], getvalue[1], caloprate[0], 0)
        array_cal(calvalue[2], getvalue[1], caloprate[0], 0)
        array_cal(calvalue[3], getvalue[1], caloprate[0], 0)
    if inbool[1]:
        array_cal(calvalue[2], getvalue[3], caloprate[2], 1)
        array_cal(calvalue[3], getvalue[3], caloprate[2], 1)
    for k in range(len(calvalue[0])):
        json["1"][str(k + 1)] = calvalue[0][k]
    if inbool[0]:
        for k in range(len(calvalue[1])):
            json["2"][str(k + 1)] = calvalue[1][k]
    if inbool[1]:
        for k in range(len(calvalue[2])):
            json["3"][str(k + 1)] = calvalue[2][k]
    if inbool[2]:
        json["4"] = {}
        for k in range(len(calvalue[3])):
            json["4"][str(k + 1)] = calvalue[3][k]
        json["4"]["升级来源"] = copy.deepcopy(json["3"]["升级来源"])


def array_cal(arr1, arr2, op, num):
    for i in range(len(arr1)):
        if i < len(arr2):
            temp = arr2[i]
        else:
            temp = arr2[0]
        if num == 0:
            opp = '1' + op[0] + '1'
        elif num == -1:
            opp = op[0] + '1'
        elif num == 1:
            opp = '1' + op[0]
        if opp == '1=1':
            arr1[i] = temp
        elif opp == '1+1':
            arr1[i] = arr1[i] + temp
        elif opp == '1\\-1':
            arr1[i] = temp - arr1[i]
        elif opp == '1*1':
            arr1[i] = arr1[i] * temp
        elif opp == '1/1':
            arr1[i] = arr1[i] / temp
        elif opp == '1\\1':
            arr1[i] = temp / arr1[i]
        elif opp == '1%-1':
            arr1[i] = arr1[i] * (100 - temp) / 100
        elif opp == '1%+1':
            arr1[i] = arr1[i] * (100 + temp) / 100
        elif opp == '1-%1':
            arr1[i] = arr1[i] * (1 - temp)


def complete_mech(all_json,mech_json):
    for i in all_json:
        for j in all_json[i]["施法目标"]:
            mech_target(all_json[i]["施法目标"][j], mech_json["目标"])
        for j in all_json[i]["效果"]:
            for k in all_json[i]["效果"][j]:
                if "生效目标" in all_json[i]["效果"][j][k]:
                    mech_target(all_json[i]["效果"][j][k]["生效目标"], mech_json["目标"])
        mech_mech(all_json[i], mech_json["机制"])
        mech_junior(all_json[i], mech_json["次级"])
        mech_sign(all_json[i]["效果"], mech_json["标记"])
        mech_repeat(all_json[i]["效果"], mech_json["叠加"])
        mech_others(all_json[i], mech_json)


def mech_target(json, mech):
    for i in ["不分类", "英雄", "非英雄"]:
        if i in json:
            for j in json[i]:
                json[i][j]["值"] = mech["势力"][str(json[i][j]["代码"])]["名称"]
                json[i][j]["颜色"] = mech["势力"][str(json[i][j]["代码"])]["颜色"]
                k = 0
                while True:
                    k = k + 1
                    if str(k) in json[i][j]:
                        json[i][j][str(k)]["值"] = mech["分类"][str(json[i][j][str(k)]["代码"])]["名称"]
                        l = 0
                        while True:
                            l += 1
                            if str(l) in json[i][j][str(k)]:
                                json[i][j][str(k)][str(l)]["值"] = mech["分类"][str(json[i][j][str(k)]["代码"])][str(json[i][j][str(k)][str(l)]["代码"])]
                            else:
                                break
                    else:
                        break


def mech_mech(json, mech):
    for i in mech:
        if i == "施法类型":
            for j in json["施法类型"]:
                k = 0
                while True:
                    k += 1
                    if str(k) in json["施法类型"][j]:
                        json["施法类型"][j][str(k)]["值"] = mech["施法类型"][str(json["施法类型"][j][str(k)]["代码"])]
                    else:
                        break
        elif i == "效果":
            for j in json[i]:
                for k in json[i][j]:
                    if "代码" in json[i][j][k]:
                        json[i][j][k]["值"] = mech[i][str(json[i][j][k]["代码"])]["名称"]
                        json[i][j][k]["图片"] = mech[i][str(json[i][j][k]["代码"])]["图片"]
        else:
            for j in json[i]:
                if str(json[i][j]["代码"]) in mech[i]:
                    json[i][j]["值"] = mech[i][str(json[i][j]["代码"])]["名称"]
                    json[i][j]["图片"] = mech[i][str(json[i][j]["代码"])]["图片"]
                    if json[i][j]["简述"] == "":
                        json[i][j]["简述"] = mech[i][str(json[i][j]["代码"])]["简述"]


def mech_junior(json, mech):
    for i in mech:
        if i in ["即时攻击", "技能窃取"]:
            for j in json[i]:
                k = 0
                while True:
                    k += 1
                    if str(k) in json[i][j]:
                        if str(json[i][j][str(k)]["代码"]) in mech[i]:
                            json[i][j][str(k)]["值"] = mech[i][str(json[i][j][str(k)]["代码"])]["名称"]
                            if "简述" not in json[i][j][str(k)] or json[i][j][str(k)]["简述"] == "":
                                json[i][j][str(k)]["简述"] = mech[i][str(json[i][j][str(k)]["代码"])]["简述"]
                    else:
                        break
        else:
            for j in json["效果"]:
                for k in json["效果"][j]:
                    if i in json["效果"][j][k]:
                        if str(json["效果"][j][k][i]["代码"]) in mech[i]:
                            json["效果"][j][k][i]["值"] = mech[i][str(json["效果"][j][k][i]["代码"])]["名称"]
                            if "图片" in mech[i][str(json["效果"][j][k][i]["代码"])]:
                                json["效果"][j][k][i]["图片"] = mech[i][str(json["效果"][j][k][i]["代码"])]["图片"]
                            if "简述" not in json["效果"][j][k][i] or json["效果"][j][k][i]["简述"] == "":
                                json["效果"][j][k][i]["简述"] = mech[i][str(json["效果"][j][k][i]["代码"])]["简述"]


def mech_sign(json, mech):
    for i in json:
        for j in json[i]:
            if "标记" in json[i][j]:
                for k in json[i][j]["标记"]:
                    if json[i][j]["标记"][k]["类型"] in mech and str(json[i][j]["标记"][k]["代码"]) in mech[json[i][j]["标记"][k]["类型"]]:
                        json[i][j]["标记"][k]["值"] = mech[json[i][j]["标记"][k]["类型"]][str(json[i][j]["标记"][k]["代码"])]


def mech_repeat(json, mech):
    for i in json:
        for j in json[i]:
            if "叠加" in json[i][j]:
                for k in json[i][j]["叠加"]:
                    if str(json[i][j]["叠加"][k]["代码1"]) in mech["来源"] and str(json[i][j]["叠加"][k]["代码2"]) in mech["方式"]:
                        json[i][j]["叠加"][k]["来源"] = mech["来源"][str(json[i][j]["叠加"][k]["代码1"])]
                        json[i][j]["叠加"][k]["方式"] = mech["方式"][str(json[i][j]["叠加"][k]["代码2"])]


def mech_others(json, mech):
    for i in json["魔法消耗"]:
        for j in json["魔法消耗"][i]:
            if j != '名称':
                for k in json["魔法消耗"][i][j]:
                    if "类型" in json["魔法消耗"][i][j][k]:
                        json["魔法消耗"][i][j][k]["类型"]["值"] = mech["魔法消耗"][str(json["魔法消耗"][i][j][k]["类型"]["代码"])]['名称']
                        json["魔法消耗"][i][j][k]["类型"]["后缀"] = mech["魔法消耗"][str(json["魔法消耗"][i][j][k]["类型"]["代码"])]['后缀']
    for i in json["冷却时间"]:
        for j in json["冷却时间"][i]:
            if "类型" in json["冷却时间"][i][j]:
                json["冷却时间"][i][j]["类型"]["值"] = mech["冷却时间"][str(json["冷却时间"][i][j]["类型"]["代码"])]["名称"]
                json["冷却时间"][i][j]["类型"]["图片"] = mech["冷却时间"][str(json["冷却时间"][i][j]["类型"]["代码"])]["图片"]
    for i in json["施法前摇"]:
        if str(json["施法前摇"][i]["即时生效"]["代码"]) in mech["即时生效"]:
            json["施法前摇"][i]["即时生效"]["图片"] = mech["即时生效"][str(json["施法前摇"][i]["即时生效"]["代码"])]


def loop_check(json, data, all_json, name):
    for i in json:
        if isinstance(json[i], dict):
            if "混合文字" in json[i]:
                change_combine_txt(json, i, data, all_json, name)
            else:
                loop_check(json[i], data, all_json, name)


def change_combine_txt(json, ii, data, all_json, name):
    returntxt = ""
    i = 0
    while True:
        i += 1
        if str(i) in json[ii]["混合文字"]:
            if isinstance(json[ii]["混合文字"][str(i)], dict):
                j = 0
                while True:
                    j += 1
                    if str(j) in json[ii]["混合文字"][str(i)]:
                        if json[ii]["混合文字"][str(i)][str(j)]["0"] == "升级属性":
                            if json[ii]["混合文字"][str(i)][str(j)]["1"] == "":
                                json[ii]["混合文字"][str(i)][str(j)]["1"] = "技能"
                            if json[ii]["混合文字"][str(i)][str(j)]["2"] == "":
                                json[ii]["混合文字"][str(i)][str(j)]["2"] = name
                        elif json[ii]["混合文字"][str(i)][str(j)]["0"] == "数据库":
                            if json[ii]["混合文字"][str(i)][str(j)]["1"] == "":
                                json[ii]["混合文字"][str(i)][str(j)]["1"] = "技能"
                            if json[ii]["混合文字"][str(i)][str(j)]["2"] == "":
                                json[ii]["混合文字"][str(i)][str(j)]["2"] = all_json["技能"][name]["代码"]
                    else:
                        break
                temp = combine_txt_numbers(json[ii]["混合文字"][str(i)], [1], all_json, data)
                if "等级" in json[ii]["混合文字"][str(i)] and int(json[ii]["混合文字"][str(i)]["等级"]) > 0:
                    level = int(json[ii]["混合文字"][str(i)]["等级"])
                else:
                    level = 0
                if "后缀" in json[ii]["混合文字"][str(i)]:
                    post = json[ii]["混合文字"][str(i)]["后缀"]
                else:
                    post = ""
                for j in range(4):
                    bool = True
                    for k in range(len(temp[j + 1])):
                        bool = bool and temp[j + 1][0] == temp[j + 1][k]
                    if bool:
                        temp[j + 1] = [temp[j + 1][0]]
                returntxt += combine_numbers_post_level(temp[1], post, level)
                if temp[0][0] or temp[0][1]:
                    returntxt += "("
                    if temp[0][0]:
                        returntxt += "[[file:agha.png|x18px|link=阿哈利姆神杖]]"
                        returntxt += combine_numbers_post_level(temp[2], post, level)
                    if temp[0][1]:
                        for j in temp[0][3]:
                            returntxt += "[[file:" + temp[0][3][j]["图片"] + "|x18px|link=" + temp[0][3][j]["名称"] + "]]"
                        returntxt += combine_numbers_post_level(temp[3], post, level)
                    if temp[0][2]:
                        returntxt += "[[file:agha.png|x18px|link=阿哈利姆神杖]]"
                        for j in temp[0][3]:
                            returntxt += "[[file:" + temp[0][3][j]["图片"] + "|x18px|link=" + temp[0][3][j]["名称"] + "]]"
                        returntxt += combine_numbers_post_level(temp[4], post, level)
                    returntxt += ")"
            else:
                returntxt += json[ii]["混合文字"][str(i)]
        else:
            break
    json[ii] = returntxt


def combine_txt_numbers(json, index, all_json, base_txt):
    i = index[0]
    if json[str(i)]["1"] == "(" or json[str(i)]["1"] == "（":
        index[0] += 1
        re = combine_txt_numbers(json, index, all_json, base_txt)
        i = index[0]
    re = one_combine_txt_numbers(json[str(i)], all_json, base_txt)
    while True:
        i += 1
        if str(i) in json:
            if json[str(i)]["1"] == "(" or json[str(i)]["1"] == "（":
                index[0] += 1
                temp = combine_txt_numbers(json, index, all_json, base_txt)
                i = index[0]
            elif json[str(i)]["符号"] == ")" or json[str(i)]["符号"] == "）":
                return re
            else:
                temp = one_combine_txt_numbers(json[str(i)], all_json, base_txt)
            calculate_combine_txt_numbers(re, temp, json[str(i)]["符号"])
        else:
            return re


def one_combine_txt_numbers(json, all_json, base_txt):
    re = [[False, False, False, {}], [], [], [], []]
    if json["0"] == "属性":
        temp = all_json[json["1"]][json["2"]][json["3"]]
        i = 3
        while True:
            i += 1
            if str(i) in json:
                temp = temp[str(i)]
            else:
                break
        j = 0
        while True:
            j += 1
            if str(j) in temp:
                re[1].append(temp[str(j)])
            else:
                break
    elif json["0"] == "数据库":
        temp = base_txt[json["1"]][json["2"]][json["3"]]
        i = 3
        while True:
            i += 1
            if str(i) in json:
                temp = temp[str(i)]
            else:
                break
        j = 0
        while True:
            j += 1
            if str(j) in temp:
                re[1].append(temp[str(j)])
            else:
                break
    elif json["0"] == "手填":
        j = 0
        while True:
            j += 1
            if str(j) in json:
                re[1].append(json[str(j)])
            else:
                break
    else:
        temp = all_json[json["1"]][json["2"]][json["3"]]
        i = 3
        while True:
            i += 1
            if str(i) in json:
                temp = temp[str(json[str(i)])]
            else:
                break
        for i in range(4):
            if str(i + 1) in temp:
                if i > 0:
                    re[0][i - 1] = True
                    if i == 2:
                        re[0][3] = copy.deepcopy(temp["3"]["升级来源"])
                j = 0
                while True:
                    j += 1
                    if str(j) in temp[str(i + 1)]:
                        re[i + 1].append(temp[str(i + 1)][str(j)])
                    else:
                        break
    if not re[0][0]:
        re[2] = copy.deepcopy(re[1])
    if not re[0][1]:
        re[3] = copy.deepcopy(re[1])
    if not re[0][2]:
        if re[0][0]:
            re[4] = copy.deepcopy(re[2])
        else:
            re[4] = copy.deepcopy(re[3])
    return re


def calculate_combine_txt_numbers(re, temp, op):
    re[0][0] = re[0][0] or temp[0][0]
    re[0][1] = re[0][1] or temp[0][1]
    re[0][2] = re[0][2] or temp[0][2]
    if re[0][3] == {} and temp[0][3] != {}:
        re[0][3] = copy.deepcopy(temp[0][3])
    for i in range(4):
        for j in range(max(len(re[i + 1]), len(temp[i + 1]))):
            if j >= len(re[i + 1]):
                re[i + 1].append(re[i + 1][0])
            if j >= len(temp[i + 1]):
                temp[i + 1].append(temp[i + 1][0])
            if op == '+':
                re[i + 1][j] += temp[i + 1][j]
            elif op == '-':
                re[i + 1][j] -= temp[i + 1][j]
            elif op == '*':
                re[i + 1][j] *= temp[i + 1][j]
            elif op == '/':
                re[i + 1][j] /= temp[i + 1][j]
            elif op == '\\':
                re[i + 1][j] = temp[i + 1][j] / re[i + 1][j]
            elif op == '^' or op == 'pow':
                re[i + 1][j] = pow(re[i + 1][j], temp[i + 1][j])
            elif op == '%-':
                re[i + 1][j] = re[i + 1][j] * (100 - temp[i + 1][j]) / 100
            elif op == '-%':
                re[i + 1][j] = re[i + 1][j] * (1 - temp[i + 1][j])
            elif op == '%+':
                re[i + 1][j] = re[i + 1][j] * (100 + temp[i + 1][j]) / 100
            elif op == '+%':
                re[i + 1][j] = re[i + 1][j] * (1 + temp[i + 1][j])
            elif op == 'min' or op == "↓":
                re[i + 1][j] = min(re[i + 1][j], temp[i + 1][j])
            elif op == 'max' or op == "↑":
                re[i + 1][j] = max(re[i + 1][j], temp[i + 1][j])
            elif op == 'round':
                re[i + 1][j] = round(re[i + 1][j], temp[i + 1][j])
            elif op == 'ceil':
                re[i + 1][j] = math.ceil(re[i + 1][j] * pow(10, temp[i + 1][j])) / pow(10, temp[i + 1][j])
            elif op == 'floor':
                re[i + 1][j] = math.floor(re[i + 1][j] * pow(10, temp[i + 1][j])) / pow(10, temp[i + 1][j])


def combine_numbers_post_level(arr, post, level):
    re = ""
    if level > 0:
        if level < len(arr):
            re += str(arr[level])
        else:
            re += str(arr[0])
        re += post
    else:
        for i in range(len(arr)):
            if i > 0:
                re += "/"
            re += str(arr[i])
            re += post
    return re


def create_file(all_json):
    for i in all_json:
        file = open("E:/json/pythonupload/" + i + '.json', mode="w")
        file.write(json.dumps(all_json[i]))
        file.close()


abilitypro_num = [["a_cast_range", "AbilityCastRange"]
    , ["a_cast_range_buff", "AbilityCastRangeBuffer"]
    , ["a_cast", "AbilityCastPoint"]
    , ["a_channel", "AbilityChannelTime"]
    , ["a_cool", "AbilityCooldown"]
    , ["a_duration", "AbilityDuration"]
    , ["a_damage", "AbilityDamage"]
    , ["a_mana", "AbilityManaCost"]]
abilitypro_bool = [["immediate", "DOTA_ABILITY_BEHAVIOR_IMMEDIATE"]
    , ["ignore_channel", "DOTA_ABILITY_BEHAVIOR_IGNORE_CHANNEL"]]
ability_trait_level = [["中文名", "英文名", "代码", "传说", "描述", "天赋代码", "A杖信息", "注释"], ["效果", "属性", "冷却时间"], ["魔法消耗"]]