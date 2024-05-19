import nt
import os
import re
import time

from jkj_rename.rename import rename_file
from my_util import input_util
from my_util.input_util import no_empty_input


def is_option_file(entry):
    """
    是否是需要操作的文件, 文件夹或操作记录文件将返回False
    :param entry:
    :return:
    """
    # 文件夹不操作
    if entry.is_dir():
        return False
    # 文件名重命名记录文件不操作
    if entry.name.startswith("file_name_option_"):
        return False
    return True


def file_rename(dir_path):
    # 选择操作指令
    command_dict = {"1": "字符串_替换",
                    "2": "字符串_在指定位置加",
                    "3": "字符串_替换指定位置的指定字符串",
                    "4": "前缀_添加",
                    "5": "序号_数字位数补齐",
                    "6": "后缀_添加",
                    "7": "后缀_替换",
                    "8": "正则_替换符合正则的字符串",
                    "10": "撤销操作"}
    op_type = input_util.command_input(command_dict)

    no_prompt_and_do = False  # 不再提示

    # 获取当前时间的毫秒值
    option_millis = int(round(time.time() * 1000))

    # 获取目录下所有文件
    scan_dir_iterator = os.scandir(dir_path)
    print(f"entry = {scan_dir_iterator} type(entry) = {type(scan_dir_iterator)}")
    # 字符串_替换
    if op_type == "1":
        old_str = no_empty_input("请输入要替换的字符串: ")
        new_str = input("请输入新的字符串: ")
        # 遍历目录下的所有文件
        for entry in scan_dir_iterator:
            if is_option_file(entry):
                file_name = entry.name
                if old_str in file_name:
                    new_file_name = file_name.replace(old_str, new_str)
                    no_prompt_and_do, no_prompt_not_do = rename_file(dir_path, file_name, new_file_name,
                                                                     no_prompt_and_do, option_millis)
                    if no_prompt_not_do:
                        break
    # 字符串_在指定位置加
    elif op_type == "2":

        # 手动输入一个字符串
        pattern = input("请输入正则表达式, 共2部分组成, 将在中间插入指定字符串: ")

        while True:
            if re.match(r'\(.*\)\(.*\)', pattern):
                break
            else:
                pattern = input("输入无效, 请重新输入: ")

        add_str = no_empty_input("请输入要添加的字符串: ")

        # 遍历目录下的所有文件
        for entry in scan_dir_iterator:
            if is_option_file(entry):

                file_name = entry.name

                # 使用正则表达式匹配数字部分
                match = re.search(pattern, file_name)

                # 如果匹配成功，则提取数字前、数字和数字后三个部分
                if match:
                    str_before = match.group(1)
                    str_after = match.group(2)
                    # 构造新的文件名
                    new_file_name = str_before + add_str + str_after
                    # 重命名文件
                    no_prompt_and_do, no_prompt_not_do = rename_file(dir_path, file_name, new_file_name,
                                                                     no_prompt_and_do, option_millis)
                    if no_prompt_not_do:
                        break
                else:
                    print(f'{file_name} No match found')

    # 字符串_替换指定位置的指定字符串
    elif op_type == "3":

        # 手动输入一个字符串
        pattern = input("请输入正则表达式, 共3部分组成, 将替换中间的字符串: ")

        while True:
            if re.match(r'\(.*\)\(.*\)\(.*\)', pattern):
                break
            else:
                pattern = input("输入无效, 请重新输入: ")

        add_str = input("请输入要新的字符串: ")
        print(pattern)

        # 遍历目录下的所有文件
        for entry in scan_dir_iterator:
            if is_option_file(entry):

                file_name = entry.name

                # 使用正则表达式匹配数字部分
                match = re.search(pattern, file_name)

                # 如果匹配成功，则提取数字前、数字和数字后三个部分
                if match:
                    str_before = match.group(1)
                    str_after = match.group(3)
                    # 构造新的文件名
                    new_file_name = str_before + add_str + str_after
                    # 重命名文件
                    no_prompt_and_do, no_prompt_not_do = rename_file(dir_path, file_name, new_file_name,
                                                                     no_prompt_and_do, option_millis)
                    if no_prompt_not_do:
                        break

    # 前缀_添加
    elif op_type == "4":
        pre_fix_str = no_empty_input("请输入要添加的前缀: ")
        # 遍历目录下的所有文件
        for entry in scan_dir_iterator:
            if is_option_file(entry):
                file_name = entry.name
                new_file_name = pre_fix_str + file_name
                no_prompt_and_do, no_prompt_not_do = rename_file(dir_path, file_name, new_file_name, no_prompt_and_do,
                                                                 option_millis)
                if no_prompt_not_do:
                    break

    # 序号_数字位数补齐
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
        pattern = input("请输入正则表达式, 共三部分组成, 数字在第二部分, 默认为: (\\D*)(\\d+)(.*): ")

        while True:
            if not pattern:
                pattern = r'(\D*)(\d+)(.*)'
                break
            # 尝试编译正则表达式
            elif re.match(r'\(.*\)\(\\d\+\)\(.*\)', pattern):
                break
            else:
                pattern = input("输入无效, 请重新输入: ")

        # 遍历目录下的所有文件
        for entry in scan_dir_iterator:
            if is_option_file(entry):
                file_name = entry.name

                # 使用正则表达式匹配数字部分
                match = re.search(pattern, file_name)

                # 如果匹配成功，则提取数字前、数字和数字后三个部分
                if match:
                    num_before = match.group(1)
                    num_part = match.group(2)
                    if len(num_part) >= num_count:
                        print(f'{file_name} 不需要操作')
                        continue
                    num_after = match.group(3)
                    print(f"数字前: {num_before}, 数字部分: {num_part}, 数字后: {num_after}")
                    # 将数字部分补齐位数
                    new_num_part = num_part.zfill(num_count)
                    # 构造新的文件名
                    new_file_name = num_before + new_num_part + num_after
                    print(f'新的文件名: {new_file_name}')
                    # 重命名文件
                    no_prompt_and_do, no_prompt_not_do = rename_file(dir_path, file_name, new_file_name,
                                                                     no_prompt_and_do, option_millis)
                    if no_prompt_not_do:
                        break
                else:
                    print(f'{file_name} No match found')

    # 后缀_添加
    elif op_type == "6":
        suffix = no_empty_input("请输入要添加的后缀: ")

        # 遍历目录下的所有文件
        for entry in scan_dir_iterator:
            if is_option_file(entry):

                file_name = entry.name

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
                    # 重命名文件
                    no_prompt_and_do, no_prompt_not_do = rename_file(dir_path, file_name, new_file_name,
                                                                     no_prompt_and_do, option_millis)
                    if no_prompt_not_do:
                        break

    # 后缀_替换
    elif op_type == "7":

        before_suffix = no_empty_input("请输入被替换的后缀: ")
        after_suffix = no_empty_input("请输入新的后缀: ")

        # 遍历目录下的所有文件
        for entry in scan_dir_iterator:
            if is_option_file(entry):

                file_name = entry.name

                name, ext = os.path.splitext(os.path.join(dir_path, file_name))
                print(f"文件名: {name} , 后缀: {ext}")

                if ext:
                    if ext[1:] == before_suffix:
                        new_file_name = name + "." + after_suffix
                        # 重命名文件
                        no_prompt_and_do, no_prompt_not_do = rename_file(dir_path, file_name, new_file_name,
                                                                         no_prompt_and_do, option_millis)
                        if no_prompt_not_do:
                            break
    # 后缀_替换
    elif op_type == "8":

        pattern = no_empty_input("请输入正则表达式: ")
        after_str = input("请输新的字符串: ")

        # 遍历目录下的所有文件
        for entry in scan_dir_iterator:
            if is_option_file(entry):
                file_name = entry.name
                if re.search(pattern, file_name):
                    new_file_name = re.sub(pattern, after_str, file_name)
                    # 重命名文件
                    no_prompt_and_do, no_prompt_not_do = rename_file(dir_path=dir_path, file_name=file_name,
                                                                     new_file_name=new_file_name,
                                                                     no_prompt_and_do=no_prompt_and_do,
                                                                     option_millis=option_millis)
                    if no_prompt_not_do:
                        break

    # 撤销操作
    elif op_type == "10":

        option_record = no_empty_input("请输入操作记录文件名: ")
        option_record_path = os.path.join(dir_path, option_record)
        if os.path.isfile(option_record_path):
            lines = None
            record = None
            with open(option_record_path, "r") as record:
                try:
                    lines = record.readlines()
                except:
                    pass
                finally:
                    if record:
                        record.close()
            for line in lines:
                if line.startswith("文件重命名成功:"):
                    start_index = line.find('|||') + 4
                    end_index = line.find('>>>', start_index)
                    before = line[start_index:end_index].strip()

                    start_index = end_index + 3
                    end_index = line.find('|||', start_index)
                    after = line[start_index:end_index].strip()

                    print(f'Before: {before}')
                    print(f'After: {after}')
                    # 如果文件存在, 则回退文件名
                    if os.path.isfile(os.path.join(dir_path, after)):

                        # 重命名文件
                        no_prompt_and_do, no_prompt_not_do = rename_file(dir_path=dir_path, file_name=after,
                                                                         new_file_name=before,
                                                                         no_prompt_and_do=no_prompt_and_do,
                                                                         option_millis=option_millis)
                        if no_prompt_not_do:
                            break



