import os
import time

from my_util import input_util


def is_option_dir(entry):
    """
    是否是需要操作的文件, 文件夹或操作记录文件将返回False
    :param entry:
    :return:
    """
    # 文件夹不操作
    if entry.is_file():
        return False
    # 文件名重命名记录文件不操作
    if entry.name.startswith("shell_back_"):
        return False
    return True


def dir_option(dir_path):
    """
    对文件进行批量操作
    :param dir_path: 文件所在目录
    :return: None
    """
    # 选择操作指令
    command_dict = {"1": "脱壳_将子文件夹下的文件移动到当前目录并将子文件夹移动到新壳中"}
    op_type = input_util.command_input(command_dict)

    no_prompt_and_do = False  # 不再提示

    # 获取当前时间的毫秒值
    option_millis = int(round(time.time() * 1000))

    # 脱壳_将子文件夹下的文件移动到当前目录并将子文件夹移动到新壳中
    if op_type == "1":
        shell_back_dir = f"{dir_path}\\shell_back_{option_millis}"
        os.mkdir(shell_back_dir)
        for entry in os.scandir(dir_path):
            if is_option_dir(entry):
                sub_dir_name = entry.name
                sub_dir_path = entry.path
                for sub_sub in os.scandir(sub_dir_path):
                    sub_sub_name = sub_sub.name
                    sub_sub_path = sub_sub.path
                    new_sub_sub_path = os.path.join(dir_path, sub_sub_name)
                    no_prompt_and_do, no_prompt_not_do = move_file(dir_path, sub_sub_path, new_sub_sub_path,
                                                                   no_prompt_and_do, option_millis)
                    if no_prompt_not_do:
                        break
                if len(os.listdir(sub_dir_path)) == 0:
                    os.rename(sub_dir_path, f"{shell_back_dir}\\{sub_dir_name}")


# 定义一个函数来重命名文件
def move_file(dir_path, file_path, new_file_path, no_prompt_and_do, option_millis):
    # 如果用户选择不再提示，直接重命名文件
    if no_prompt_and_do:
        do_move_and_record(dir_path, file_path, new_file_path, option_millis)
    else:
        # 否则，询问用户是否确认重命名
        confirm = input(
            f"操作确认 >>> 移动文件:  |||  {file_path}  --> {new_file_path}   |||"
            f"\n\ty-确认"
            f"\n\tY-确认且不再提示"
            f"\n\tn-取消"
            f"\n\tN-取消且不再提示"
            f"\n请输入指令:")
        while confirm not in ["Y", "y", "N", "n"]:
            confirm = input(f"指令无效, 请重新输入: ")
        if confirm == "Y":
            no_prompt_and_do = True
            do_move_and_record(dir_path, file_path, new_file_path, option_millis)
        elif confirm == "y":
            do_move_and_record(dir_path, file_path, new_file_path, option_millis)
        elif confirm == "N":
            print("已取消批量移动！")
            return False, True  # 返回一个标志，表示用户选择取消批量重命名
        else:
            print("已取消移动！")
    return no_prompt_and_do, False


def do_move_and_record(dir_path, file_path, new_file_path, option_millis):
    os.rename(file_path, new_file_path)
    log_str = f"移动文件成功: |||\t{file_path}\t>>>\t{new_file_path}\t|||"
    print(log_str)
    if option_millis:
        option_millis_record_file = os.path.join(dir_path, f"file_option_{option_millis}.txt")
        # 以毫秒值为文件名创建文本文件
        with open(option_millis_record_file, "a") as option_log:
            option_log.write(f"{log_str}\n")
