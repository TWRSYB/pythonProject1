# 输入要操作的目录
import os

import dir_option
from my_util import input_util
import file_option, file_name_option, dir_name_option

dir_path = input("请输入要操作的目录: ")
# 判断目录是否存在
if not os.path.exists(dir_path):
    print(f"目录 {dir_path} 不存在，程序退出")
    exit()

# 客户选择操作类型 0-退出, 1-替换字符串, 2-添加前缀
while True:
    # 选择操作指令
    command_dict = {"0": "退出", "1": "文件名批量操作", "2": "目录名批量操作", "3": "文件批量操作", "4": "文件夹批量操作"}
    op_type = input_util.command_input(command_dict)

    # 退出逻辑
    if op_type == "0":
        break
    # 文件名批量操作
    elif op_type == "1":
        file_name_option.file_rename(dir_path)
    elif op_type == "2":
        dir_name_option.dir_rename(dir_path)
    elif op_type == "3":
        file_option.file_option(dir_path)
    elif op_type == "4":
        dir_option.dir_option(dir_path)
