import os

directory = r'D:\15.Development Projects\06.pachon\pythonProject1\PC_05_91GCYY\OutputData01\IMG'  # 替换为你的目录路径
list_serno = [file.split("_")[0] for file in os.listdir(directory)]
list_lost = []
for i in range(3038, 5407):
    if f'{i}' not in list_serno:
        list_lost.append(i)
print(list_lost)
