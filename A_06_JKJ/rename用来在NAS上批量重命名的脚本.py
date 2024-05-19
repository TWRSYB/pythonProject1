import time
# 引入操作系统模块
import os
# 引入正则表达式模块
import re
# collections 模块中的 defaultdict 类提供了一种方便的方式来创建默认值为特定类型的字典
from collections import defaultdict
# 引入自定义重命名方法
from jkj_rename.rename import rename_file
# 引入自定义input方法
from my_util.input_util import no_empty_input
# 引入自定义文件去重方法
from jkj_duplicate.duplicate import de_duplicate_default, de_duplicate_one_by_one

# 输入要操作的目录
dir_path = input("请输入要操作的目录: ")
# 判断目录是否存在
if not os.path.exists(dir_path):
    print(f"目录 {dir_path} 不存在，程序退出")
    exit()

# 客户选择操作类型 0-退出, 1-替换字符串, 2-添加前缀
while True:
    # 获取目录下所有文件
    file_list = os.listdir(dir_path)
    op_type = input("请选择操作类型:"
                    "\n\t0 - 退出"
                    "\n\t1 - 文件名批量操作_替换字符串"
                    "\n\t2 - 文件名批量操作_添加前缀"
                    "\n\t5 - 文件名批量操作_数字位数补齐"
                    "\n\t6 - 文件名批量操作_添加后缀"
                    "\n\t7 - 文件名批量操作_在指定位置加指定字符串"
                    "\n\t8 - 文件名批量操作_替换指定位置的指定字符串"
                    "\n\t9 - 文件名批量操作_替换后缀名"
                    "\n\t11 - 文件夹名批量操作_只保留《》中间的部分"
                    "\n\t21 - 文件批量操作_去重"
                    "\r\n请输入: ")
    no_more_prompt = False  # 不再提示
    stop = False  # 退出循环



    # 退出逻辑
    if op_type == "0":
        break
    # 替换文件名中的指定字符串逻辑
    elif op_type == "1":
        old_str = no_empty_input("请输入要替换的字符串: ")
        new_str = input("请输入新的字符串: ")
        for file_name in file_list:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                if old_str in file_name:
                    new_file_name = file_name.replace(old_str, new_str)
                    new_file_path = os.path.join(dir_path, new_file_name)
                    no_more_prompt, stop = rename_file(file_path, new_file_path, no_more_prompt)
                    if stop:
                        break
    # 添加前缀逻辑
    elif op_type == "2":
        pre_fix_str = no_empty_input("请输入要添加的前缀: ")
        for file_name in file_list:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                new_file_name = pre_fix_str + file_name
                new_file_path = os.path.join(dir_path, new_file_name)
                no_more_prompt, stop = rename_file(file_path, new_file_path, no_more_prompt)
                if stop:
                    break

    # 文件名批量操作_数字位数补齐
    elif op_type == "5":
        num_count = input("请输入数字位数:")

        while True:
            try:
                num_count = int(num_count)
                if num_count < 2:
                    num_count = input("数字位数必须大于1, 请重新输入:")
                else:
                    break
            except ValueError:
                num_count = input("输入无效, 请重新输入:")

        # 手动输入一个字符串
        pattern = input("请输入正则表达式, 共三部分组成, 数字在第二部分, 默认为: (\\D*)(\\d+)(\\D*): ")

        while True:
            if not pattern:
                pattern = r'(\D*)(\d+)(\D*)'
                break
            # 尝试编译正则表达式
            elif re.match(r'\(.*\)\(\\d\+\)\(.*\)', pattern):
                break
            else:
                pattern = input("输入无效, 请重新输入: ")

        # 遍历目录下的所有文件
        for entry in os.scandir(dir_path):
            if entry.is_file():

                file_name = entry.name
                file_path = entry.path

                # 使用正则表达式匹配数字部分
                match = re.search(pattern, file_name)

                # 如果匹配成功，则提取数字前、数字和数字后三个部分
                if match:
                    num_before = match.group(1)
                    num_part = match.group(2)
                    if len(num_part) == 3:
                        print(f'{file_name} 不需要操作')
                        continue
                    num_after = match.group(3)
                    print(f"数字前: {num_before}, 数字部分: {num_part}, 数字后: {num_after}")
                    # 将数字部分补齐3位
                    new_num_part = num_part.zfill(num_count)
                    # 构造新的文件名
                    new_file_name = num_before + new_num_part + num_after
                    new_file_path = os.path.join(dir_path, new_file_name)
                    print(f'新的文件名: {new_file_name}')
                    # 重命名文件
                    no_more_prompt, stop = rename_file(file_path, new_file_path, no_more_prompt)
                    if stop:
                        break
                else:
                    print(f'{file_name} No match found')

    # 文件名批量操作_添加后缀
    elif op_type == "6":
        suffix = no_empty_input("请输入要添加的后缀: ")

        # 遍历目录下的所有文件
        for entry in os.scandir(dir_path):
            if entry.is_file():

                file_name = entry.name
                file_path = entry.path

                name, ext = os.path.splitext(os.path.join(dir_path, file_name))
                print(f"文件名: {name} , 后缀: {ext}")
                new_file_name = ""
                if ext:
                    if re.match(r'^[a-zA-Z0-9]+$', ext[1:]):
                        print(f"文件 {file_name} 的后缀是合法后缀")
                    else:
                        new_file_name = file_name + "." + suffix
                else:
                    new_file_name = file_name + "." + suffix
                if new_file_name:
                    new_file_path = os.path.join(dir_path, new_file_name)
                    # 重命名文件
                    no_more_prompt, stop = rename_file(file_path, new_file_path, no_more_prompt)
                    if stop:
                        break

    # 文件名批量操作_在指定位置加指定字符串
    elif op_type == "7":

        # 手动输入一个字符串
        pattern = input("请输入正则表达式, 共2部分组成, 将在中间插入指定字符串: ")

        while True:
            if re.match(r'\(.*\)\(.*\)', pattern):
                break
            else:
                pattern = input("输入无效, 请重新输入: ")

        add_str = no_empty_input("请输入要添加的字符串: ")

        # 遍历目录下的所有文件
        for entry in os.scandir(dir_path):
            if entry.is_file():

                file_name = entry.name
                file_path = entry.path

                # 使用正则表达式匹配数字部分
                match = re.search(pattern, file_name)

                # 如果匹配成功，则提取数字前、数字和数字后三个部分
                if match:
                    str_before = match.group(1)
                    str_after = match.group(2)
                    # 构造新的文件名
                    new_file_name = str_before + add_str + str_after
                    new_file_path = os.path.join(dir_path, new_file_name)
                    print(f'新的文件名: {new_file_name}')
                    # 重命名文件
                    no_more_prompt, stop = rename_file(file_path, new_file_path, no_more_prompt)
                    if stop:
                        break
                else:
                    print(f'{file_name} No match found')

    # 文件名批量操作_替换指定位置的指定字符串
    elif op_type == "8":

        # 手动输入一个字符串
        pattern = input("请输入正则表达式, 共3部分组成, 将替换中间的字符串: ")

        while True:
            if re.match(r'\(.*\)\(.*\)\(.*\)', pattern):
                break
            else:
                pattern = input("输入无效, 请重新输入: ")

        add_str = no_empty_input("请输入要新添加的字符串: ")

        # 遍历目录下的所有文件
        for entry in os.scandir(dir_path):
            if entry.is_file():

                file_name = entry.name
                file_path = entry.path

                # 使用正则表达式匹配数字部分
                match = re.search(pattern, file_name)

                # 如果匹配成功，则提取数字前、数字和数字后三个部分
                if match:
                    str_before = match.group(1)
                    str_middle = match.group(2)
                    str_after = match.group(3)
                    # 构造新的文件名
                    new_file_name = str_before + add_str + str_after
                    new_file_path = os.path.join(dir_path, new_file_name)
                    print(f'新的文件名: {new_file_name}')
                    # 重命名文件
                    no_more_prompt, stop = rename_file(file_path, new_file_path, no_more_prompt)
                    if stop:
                        break
                else:
                    print(f'{file_name} No match found')

    # 文件名批量操作_替换后缀名
    elif op_type == "9":

        before_suffix = no_empty_input("请输入被替换的后缀: ")
        after_suffix = no_empty_input("请输入新的后缀: ")

        # 遍历目录下的所有文件
        for entry in os.scandir(dir_path):
            if entry.is_file():

                file_name = entry.name
                file_path = entry.path

                name, ext = os.path.splitext(os.path.join(dir_path, file_name))
                print(f"文件名: {name} , 后缀: {ext}")

                if ext:
                    if ext[1:] == before_suffix:
                        new_file_name = name + "." + after_suffix
                        new_file_path = os.path.join(dir_path, new_file_name)
                        # 重命名文件
                        no_more_prompt, stop = rename_file(file_path, new_file_path, no_more_prompt)
                        if stop:
                            break

    # 文件夹批量操作_只保留《》中间的部分
    elif op_type == "11":
        # 定义正则表达式规则，只匹配《》之间的内容
        pattern = re.compile(r'《(.+?)》')
        for file_name in file_list:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isdir(file_path):
                match = pattern.search(file_name)
                if match:
                    new_file_name = match.group(1)
                    new_file_path = os.path.join(dir_path, new_file_name)
                    no_more_prompt, stop = rename_file(file_path, new_file_path, no_more_prompt)
                    if stop:
                        break

    # 文件批量操作_去重
    elif op_type == "21":
        # 用于收集不同大小下的文件列表集合
        size_files_map = defaultdict(list)
        # 用于收集重复文件
        duplicates = {}

        # 遍历指定目录下的所有文件和子目录
        for entry in os.scandir(dir_path):
            if entry.is_file():
                # 获取文件的大小
                file_size = entry.stat().st_size
                # 将文件存入到集合中
                size_files_map[file_size].append(entry.name)

        # 将有相同大小的文件提取出来
        for size, files in size_files_map.items():
            if len(files) > 1:
                duplicates[size] = files

        # 输出重复文件列表
        print(duplicates)

        if duplicates:
            print("发现以下相同大小的文件：")
            for size, files in duplicates.items():
                print(f"大小 {size}byte， 文件列表： {files}")
            command = input("是否执行去重操作？"
                            "\n\ty - 逐个确认去重"
                            "\n\tY - 按照默认规则去重后逐个确认去重"
                            "\n\tn - 退出"
                            "\n请输入：")

            while True:
                if command in ['y', 'Y', 'n']:
                    break
                else:
                    command = input("输入无效, 请重新输入: ")

            if command == 'y':
                de_duplicate_one_by_one(dir_path, duplicates)
            elif command == 'Y':
                de_duplicate_default(dir_path, duplicates)

        else:
            print("当前目录下未发现相同大小的文件")
