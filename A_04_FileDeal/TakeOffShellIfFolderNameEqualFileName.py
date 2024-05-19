import os
import shutil

from A_03_Common.InputCheck import input_check


def take_off_shell_if_folder_name_equal_file_name(_root_path):
    list_folder_name_equal_file_name = []
    for sub_item in os.listdir(_root_path):
        sub_item_path = os.path.join(_root_path, sub_item)
        if os.path.isdir(sub_item_path) and '.' in sub_item:
            if len(os.listdir(sub_item_path)) == 1 and os.listdir(sub_item_path)[0] == sub_item:
                if os.path.isfile(os.path.join(sub_item_path, sub_item)):
                    list_folder_name_equal_file_name.append(sub_item)
    print(f'扫描到{len(list_folder_name_equal_file_name)}个文件夹名与内部文件名相同的文件夹{list_folder_name_equal_file_name}')

    move_them = ''
    for dir_matched in list_folder_name_equal_file_name:
        print(f'满足条件的文件夹: {dir_matched}')
        if not move_them:
            move_them = input(f'''要不要剪切呢? 
            n=不剪切
            N=不剪切不再提示
            y=剪切
            Y=剪切不再提示
            请输入:''')
        if move_them in ['N', 'n']:
            if move_them == 'n':
                move_them = ''
            continue
        elif move_them in ['Y', 'y']:
            if move_them == 'y':
                move_them = ''
            token_off_shell_files_folder = os.path.join(_root_path, '00.TokenOffShellFiles')
            if not os.path.isdir(token_off_shell_files_folder):
                os.makedirs(token_off_shell_files_folder)
            empty_shells_folder = os.path.join(_root_path, '00.EmptyShells')
            if not os.path.isdir(empty_shells_folder):
                os.makedirs(empty_shells_folder)
            path_dir_matched = os.path.join(_root_path, dir_matched)
            path_file_matched = os.path.join(path_dir_matched, dir_matched)
            shutil.move(path_file_matched, token_off_shell_files_folder)
            shutil.move(path_dir_matched, empty_shells_folder)
            print(f'脱壳完成: {dir_matched}')
        else:
            if move_them == 'n':
                move_them = ''


if __name__ == '__main__':
    root_path = input_check(msg='请输入要执行的目录, 如果是当前目录请输入d:', not_null=True)
    take_off_shell_if_folder_name_equal_file_name(root_path)
