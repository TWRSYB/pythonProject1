import os
import time
from collections import defaultdict

from jkj_duplicate.duplicate import de_duplicate_one_by_one, de_duplicate_default
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


def file_option(dir_path):
    """
    对文件进行批量操作
    :param dir_path: 文件所在目录
    :return: None
    """
    # 选择操作指令
    command_dict = {"1": "去重",
                    "2": "删除指定后缀名的文件"}
    op_type = input_util.command_input(command_dict)

    # 获取目录下所有文件
    scan_dir_iterator = os.scandir(dir_path)

    # 去重
    if op_type == "1":
        # 用于收集不同大小下的文件列表集合
        size_files_map = defaultdict(list)
        # 用于收集重复文件
        duplicates = {}

        # 遍历指定目录下的所有文件和子目录
        for entry in scan_dir_iterator:
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
    elif op_type == "2":
        delete_suffix = no_empty_input("请输入要删除的后缀: ")
        # 遍历目录下的所有文件
        for entry in scan_dir_iterator:
            if is_option_file(entry):

                file_name = entry.name

                name, ext = os.path.splitext(os.path.join(dir_path, file_name))

                if ext:
                    if ext[1:].lower() == delete_suffix.lower():
                        print(f"即将删除文件{file_name}")
                        os.remove(os.path.join(dir_path, file_name))
