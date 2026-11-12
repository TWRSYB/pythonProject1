import os
import shutil

from A_03_Common.InputCheck import input_check


def delete_empty_folder(_root_path):
    list_empty_folder = []
    for sub_item in os.listdir(_root_path):
        sub_item_path = os.path.join(_root_path, sub_item)
        if os.path.isdir(sub_item_path):
            with os.scandir(sub_item_path) as it:
                if next(it, None) is None:
                    list_empty_folder.append(sub_item_path)
    print(f'扫描到{len(list_empty_folder)}个空文件夹: {list_empty_folder}')

    delete_flag = ''
    for dir_matched in list_empty_folder:
        print(f'满足条件的文件夹: {dir_matched}')
        if not delete_flag:
            delete_flag = input(f'''要不要删除呢? 
            n=不删除
            N=不删除不再提示
            y=删除
            Y=删除不再提示
            请输入:''')
        if delete_flag in ['N', 'n']:
            if delete_flag == 'n':
                delete_flag = ''
            continue
        elif delete_flag in ['Y', 'y']:
            if delete_flag == 'y':
                delete_flag = ''
            empty_folder = os.path.join(_root_path, '00.EmptyFolders')
            if not os.path.isdir(empty_folder):
                os.makedirs(empty_folder)
            path_dir_matched = os.path.join(_root_path, dir_matched)
            shutil.move(path_dir_matched, empty_folder)
            print(f'删除完成: {dir_matched}')
        else:
            if delete_flag == 'n':
                delete_flag = ''


if __name__=='__main__':
    root_path = input_check(msg='请输入要执行的目录, 如果是当前目录请输入d:', not_null=True)
    delete_empty_folder(root_path)
