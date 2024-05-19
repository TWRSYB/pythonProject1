import os
import re


# 去重_逐个确认
def de_duplicate_one_by_one(dir_path, duplicates):
    for size, files in duplicates.items():
        print(f"重复文件 {size}byte， 文件列表： {files}")
        command = input("请选择要保留第几个(0 - 跳过)： ")
        while True:
            try:
                command = int(command)
                if command > len(files):
                    command = input("输入值超出文件数量, 请重新输入： ")
                else:
                    break
            except ValueError:
                command = input("输入有误, 请重新输入： ")

        if command == 0:
            continue

        for file_name in files:
            if file_name != files[command - 1]:
                print(f"即将删除文件{file_name}")
                os.remove(os.path.join(dir_path, file_name))
    print("去重操作已经全部完成")


# 按照默认规则去重之后再逐个去重
def de_duplicate_default(dir_path, duplicates):
    duplicates_canliu = {}
    for size, files in duplicates.items():
        match_default = False
        default_file_name = ""
        for file_name in files:
            if not re.search(r'\(\d+\)| - 副本', file_name):
                default_file_name = file_name
                match_default = True
                for another_file_name in files:
                    rule_name = re.sub(r'\(\d+\)| - 副本', '', another_file_name)
                    print(f"rule_name = {rule_name}")
                    if rule_name != file_name:
                        match_default = False
                        break
                if not match_default:
                    break
        if match_default:
            for file_name in files:
                if file_name != default_file_name:
                    print(f"即将删除文件{file_name}")
                    os.remove(os.path.join(dir_path, file_name))
            print(f"重复文件 {files} 中， 保留了文件： {default_file_name}")
        else:
            print(f"重复文件 {files} 没有满足默认规则, 待逐一确认")
            duplicates_canliu[size] = files
    if duplicates_canliu:
        print("已经完成默认去重, 尚有重复文件, 请逐一确认")
        de_duplicate_one_by_one(dir_path, duplicates_canliu)
    else:
        print("已经完成默认去重, 去重操作已经全部完成")

