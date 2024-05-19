import os


def do_rename_and_record(dir_path, option_millis, file_name, new_file_name):
    file_path = os.path.join(dir_path, file_name)
    new_file_path = os.path.join(dir_path, new_file_name)
    os.rename(file_path, new_file_path)
    log_str = f"文件重命名成功: |||\t{file_name}\t>>>\t{os.path.basename(new_file_path)}\t|||"
    print(log_str)
    if option_millis:
        option_millis_record_file = os.path.join(dir_path, f"file_name_option_{option_millis}.txt")
        # 以毫秒值为文件名创建文本文件
        with open(option_millis_record_file, "a") as option_log:
            option_log.write(f"{log_str}\n")


# 定义一个函数来重命名文件
def rename_file(dir_path, file_name, new_file_name, no_prompt_and_do, option_millis):
    # 如果用户选择不再提示，直接重命名文件
    if no_prompt_and_do:
        do_rename_and_record(dir_path, option_millis, file_name, new_file_name)
    else:
        # 否则，询问用户是否确认重命名
        confirm = input(
            f"操作确认 >>> 文件重命名:  |||  {file_name}  --> {new_file_name}   |||"
            f"\n\ty-确认"
            f"\n\tY-确认且不再提示"
            f"\n\tn-取消"
            f"\n\tN-取消且不再提示"
            f"\n请输入指令:")
        while confirm not in ["Y", "y", "N", "n"]:
            confirm = input(f"指令无效, 请重新输入: ")
        if confirm == "Y":
            no_prompt_and_do = True
            do_rename_and_record(dir_path, option_millis, file_name, new_file_name)
        elif confirm == "y":
            do_rename_and_record(dir_path, option_millis, file_name, new_file_name)
        elif confirm == "N":
            print("已取消批量重命名！")
            return False, True  # 返回一个标志，表示用户选择取消批量重命名
        else:
            print("已取消重命名！")
    return no_prompt_and_do, False
