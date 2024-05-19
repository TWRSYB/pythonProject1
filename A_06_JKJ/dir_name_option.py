import os
import re

from jkj_rename.rename import rename_file
from my_util import input_util


def dir_rename(dir_path):
    # 选择操作指令
    command_dict = {"1": "只保留《》中间的部分"}
    op_type = input_util.command_input(command_dict)

    no_prompt_and_do = False  # 不再提示

    # 获取目录下所有文件
    file_list = os.listdir(dir_path)

    # 文件夹批量操作_只保留《》中间的部分
    if op_type == "1":
        # 定义正则表达式规则，只匹配《》之间的内容
        pattern = re.compile(r'《(.+?)》')
        for file_name in file_list:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isdir(file_path):
                match = pattern.search(file_name)
                if match:
                    new_file_name = match.group(1)
                    no_more_prompt, stop = rename_file(dir_path=dir_path, file_name=file_name, new_file_name=new_file_name, no_prompt_and_do=no_prompt_and_do, option_millis=None)
                    if stop:
                        break
