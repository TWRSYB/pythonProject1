import os
import shutil

from A03Common.InputCheck import input_check


def take_off_shell_if_folder_name_equal_file_name(_root_path):
    for sub_item in os.listdir(_root_path):
        sub_item_path = os.path.join(_root_path, sub_item)
        if os.path.isdir(sub_item_path):
            sub_item_content_list = os.listdir(sub_item_path)
            if len(sub_item_content_list) == 1 and sub_item_content_list[0] == sub_item:
                old_sub_item_content_path = os.path.join(sub_item_path, sub_item_content_list[0])
                if os.path.isfile(old_sub_item_content_path):
                    token_off_shell_files_folder = os.path.join(_root_path, 'TokenOffShellFiles')
                    if not os.path.isdir(token_off_shell_files_folder):
                        os.makedirs(token_off_shell_files_folder)
                    empty_shells_folder = os.path.join(_root_path, 'EmptyShells')
                    if not os.path.isdir(empty_shells_folder):
                        os.makedirs(empty_shells_folder)
                    shutil.move(old_sub_item_content_path, token_off_shell_files_folder)
                    shutil.move(sub_item_path, empty_shells_folder)
                    print(old_sub_item_content_path)


if __name__ == '__main__':
    root_path = input_check(msg='请输入要执行的目录, 如果是当前目录请输入d:', not_null=True)
    take_off_shell_if_folder_name_equal_file_name(root_path)
