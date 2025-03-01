import os
import shutil
import sys

from A_03_Common.InputCheck import input_check

if __name__ == '__main__':
    main_task_dir = input_check("请输入当前任务文件夹:", True, 'dir')
    main_task_sub_file_list  = os.listdir(main_task_dir)
    main_single_task_list = []
    main_package_task_dict = {}
    for sub_file in main_task_sub_file_list:
        sub_file_path = os.path.join(main_task_dir, sub_file)
        if os.path.isfile(sub_file_path) and sub_file.endswith('.torrent'):
            print(f'找到一个单个种子文件{(sub_file,sub_file_path)}')
            main_single_task_list.append(sub_file)
        elif os.path.isdir(sub_file_path):
            print(f'找到一个包任务{(sub_file, sub_file_path)}')
            sub_sub_file_list = os.listdir(sub_file_path)
            for sub_sub_file in sub_sub_file_list:
                sub_sub_file_path = os.path.join(sub_file_path, sub_sub_file)
                if os.path.isfile(sub_sub_file_path) and sub_sub_file.endswith('.torrent'):
                    print(f'找到一个包内种子文件{(sub_sub_file, sub_sub_file_path)}')
                    main_package_task_dict.setdefault(sub_file, []).append(sub_sub_file)
    print(main_single_task_list)
    print(main_package_task_dict)




    scan_task_dir =  input_check("请输入扫描文件夹:", True, 'dir')
    if scan_task_dir in main_task_dir:
        print('当前任务文件夹包含扫描文件夹或一致, 任务退出')
        sys.exit()
    back_dir = os.path.join(scan_task_dir, '00.扫描后备份')
    os.makedirs(back_dir, exist_ok=True)
    scan_task_sub_file_list  = os.listdir(scan_task_dir)
    scan_package_task_dict = {}
    for sub_file in scan_task_sub_file_list:
        sub_file_path = os.path.join(scan_task_dir, sub_file)
        if os.path.isfile(sub_file_path) and sub_file.endswith('.torrent'):
            print(f'找到一个单个种子文件{(sub_file,sub_file_path)}')
            if sub_file in main_single_task_list:
                print(f'种子文件已经在当前任务文件夹中, 即将移动到备份目录')
                shutil.move(sub_file_path, back_dir)
        elif os.path.isdir(sub_file_path) and sub_file in main_package_task_dict and sub_file != '00.扫描后备份':
            print(f'找到一个包任务{(sub_file, sub_file_path)}并且当前任务文件夹中有同名包任务')
            sub_sub_file_list = os.listdir(sub_file_path)
            torrent_list = []
            for sub_sub_file in sub_sub_file_list:
                sub_sub_file_path = os.path.join(sub_file_path, sub_sub_file)
                if os.path.isfile(sub_sub_file_path) and sub_sub_file.endswith('.torrent'):
                    print(f'找到一个包内种子文件{(sub_sub_file, sub_sub_file_path)}')
                    torrent_list.append(sub_sub_file)
            if torrent_list:
                if all(item in main_package_task_dict[sub_file] for item in torrent_list):
                    print(f'包任务中所有的种子文件已经存在于当前任务文件夹中{sub_file_path}, 即将移动到备份目录')
                    shutil.move(sub_file_path, back_dir)
                else:
                    print(f'警告: 当前任务包种子与当前任务文件夹中的任务包的种子不一样{sub_file}')
            else:
                print(f'警告: 当前任务包中没有种子{sub_file}')