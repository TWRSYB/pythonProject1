# 迅雷安装路径
import os
import subprocess

from A_03_Common.InputCheck import input_check

THUNDER_PATH= r'C:\Program Files (x86)\Thunder Network\Thunder\Program\Thunder.exe'



# 使用迅雷打开
def open_with_thunder(torrent_file):
    subprocess.run([THUNDER_PATH, torrent_file])

if __name__ == '__main__':
    scan_task_dir =  input_check("请输入扫描文件夹:", True, 'dir')

    scan_task_sub_file_list  = os.listdir(scan_task_dir)
    scan_package_task_dict = {}
    for index, sub_file in enumerate(scan_task_sub_file_list):
        if index >= 50:
            break
        sub_file_path = os.path.join(scan_task_dir, sub_file)
        if os.path.isfile(sub_file_path) and sub_file.endswith('.torrent'):
            print(f'找到一个单个种子文件{(sub_file,sub_file_path)}')
            open_with_thunder(sub_file_path)
        elif os.path.isdir(sub_file_path) and sub_file != '00.扫描后备份':
            print(f'找到一个包任务{(sub_file, sub_file_path)}')
            sub_sub_file_list = os.listdir(sub_file_path)
            for sub_sub_file in sub_sub_file_list:
                sub_sub_file_path = os.path.join(sub_file_path, sub_sub_file)
                if os.path.isfile(sub_sub_file_path) and sub_sub_file.endswith('.torrent'):
                    print(f'找到一个包内种子文件{(sub_sub_file, sub_sub_file_path)}')
                    open_with_thunder(sub_sub_file_path)
