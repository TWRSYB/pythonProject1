import json


def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

json1 = r'D:\15.Development Projects\06.pachon\pythonProject1\PC_05_91GCYY\OutputData03\JSON_ALL.json'
json2 = r'D:\15.Development Projects\06.pachon\pythonProject1\PC_05_91GCYY\OutputData01\JSON_ALL.json'
json3 = r'D:\15.Development Projects\06.pachon\pythonProject1\PC_05_91GCYY\OutputData02\JSON_ALL.json'

with open(json1, 'r', encoding='utf-8') as json_file:
    json_list_1 = json.load(json_file)
list_serno_1 = [item.get('serno') for item in json_list_1]
duplicates_1 = find_duplicates(list_serno_1)
list_lost_1 = []
for i in range(3038, 5407):
    if f'{i}' not in list_serno_1:
        list_lost_1.append(i)

with open(json2, 'r', encoding='utf-8') as json_file:
    json_list_2 = json.load(json_file)
list_serno_2 = [item.get('serno') for item in json_list_2]
duplicates_2 = find_duplicates(list_serno_2)
list_lost_2 = []
for i in range(3038, 5407):
    if f'{i}' not in list_serno_2:
        list_lost_2.append(i)


with open(json3, 'r', encoding='utf-8') as json_file:
    json_list_3 = json.load(json_file)
list_serno_3 = [item.get('serno') for item in json_list_3]
duplicates_3 = find_duplicates(list_serno_3)
list_lost_3 = []
for i in range(3038, 5407):
    if f'{i}' not in list_serno_3:
        list_lost_3.append(i)

# 计算交集
intersection_duplicates = set(duplicates_1).intersection(set(duplicates_2)).intersection(set(duplicates_3))
intersection_lost = set(list_lost_1).intersection(set(list_lost_2)).intersection(set(list_lost_3))


# 计算并集
union = set(list_serno_1).union(set(list_serno_2)).union(set(list_serno_3))

print(f'json1读取数量{len(json_list_1)}')
print(f'json2读取数量{len(json_list_2)}')
print(f'json3读取数量{len(json_list_3)}')
print(f'3者并集数量: {len(union)}')

print(f'json1重复的有: {duplicates_1}')
print(f'json2重复的有: {duplicates_2}')
print(f'json3重复的有: {duplicates_3}')
print(f'重复的交集有: {intersection_duplicates}')

print(f'json1 缺失的有: {list_lost_1}')
print(f'json2 缺失的有: {list_lost_2}')
print(f'json3 缺失的有: {list_lost_3}')
print(f'缺失的交集有: {intersection_lost}')


