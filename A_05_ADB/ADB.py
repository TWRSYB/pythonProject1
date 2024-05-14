import os
import subprocess

adb_path = os.path.join(os.path.abspath(__file__), "../platform-tools/adb.exe")


def get_item_list_from_android_dir(directory, judge: bool = True):
    # 构造ADB shell命令
    cmd = [adb_path, 'shell', 'ls', f'{"-p" if judge else ""}', directory]

    # 运行ADB命令并捕获输出
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', text=True)

    # 检查是否有错误输出
    if result.stderr:
        print(f"Error: {result.stderr}")
        return []

    # 解析输出
    item_and_is_dir_list = []

    for item in result.stdout.split('\n'):
        item = item.strip()
        # 跳过空行和目录列表的开头部分（通常是文件夹本身）
        if not item or item.endswith(':'):
            continue
        if item.endswith('/'):
            item_and_is_dir_list.append((item[:-1], True))
        else:
            item_and_is_dir_list.append((item, False))
    return item_and_is_dir_list


# 检查目标目录是否存在，如果不存在则创建它
def create_directory_on_device(dir_path):
    # 尝试列出目录以检查它是否存在
    try:
        cmd = [adb_path, 'shell', f'ls {dir_path}']
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return 1, f'目录已存在: {dir_path}'
    except subprocess.CalledProcessError:
        # 如果列出目录失败（即目录不存在），则创建它
        cmd = [adb_path, 'shell', f'mkdir -p {dir_path}']
        subprocess.run(cmd, check=True)
        print(f"Directory {dir_path} created on the device.")
        return 2, f'目录创建成功： {dir_path}'


# 在安卓设备上复制文件
def copy_file_on_device(src_file, dest_dir, copy_dir=False):
    # 使用cp命令在设备内部复制文件
    cmd = [adb_path, 'shell', f'cp{" -r" if copy_dir else ""} "{src_file}" "{dest_dir}"']
    subprocess.run(cmd, check=True)
    print(f"ADB文件复制成功: {src_file} >>> {dest_dir}")


# 将文件移动到目标目录
def move_file_on_device(src_file, dest_dir):
    # 使用mv命令移动文件
    cmd = [adb_path, 'shell', f'mv "{src_file}" "{dest_dir}"']
    subprocess.run(cmd, check=True)
    print(f"ADB移动文件成功: {src_file} >>> {dest_dir}")


def pull_file_to_local(device_item, local_dir, delete_source: bool = False):
    cmd = [adb_path, 'pull ', f'"{device_item}" "{local_dir}"']
    subprocess.run(cmd, check=True)
    if delete_source:
        cmd = [adb_path, 'shell', f'rm "{device_item}"']
        subprocess.run(cmd, check=True)
    print(f"ADB pull文件 成功: {device_item} >>> {local_dir}")


def pull_dir_to_local(device_item, local_dir, delete_source: bool = False):
    android_dir_sub_list = get_item_list_from_android_dir(device_item)
    if not android_dir_sub_list:
        print(f"ADB 读取文件夹 失败: {device_item}")
    new_local_dir = os.path.join(local_dir, os.path.basename(device_item))
    os.makedirs(new_local_dir)
    cmd = [adb_path, 'pull ', f'"{device_item}/*" "{new_local_dir}"']
    subprocess.run(cmd, check=True)
    if delete_source:
        cmd = [adb_path, 'shell', f'rm -r "{device_item}"']
        subprocess.run(cmd, check=True)
    print(f"ADB pull文件夹 成功: {device_item} >>> {local_dir}")

if __name__ == '__main__':
    # directory = '/sdcard/Download/UCDownloads/VideoData'  # 替换为你想要读取的目录
    directory = '/sdcard/UCDownloads/VideoData'  # 替换为你想要读取的目录
    files = get_item_list_from_android_dir(directory)
    print(files)

    # directory = '/sdcard/UCDownloads/13月'
    # create_directory_on_device(directory)

    # 执行函数
    # copy_file_on_device('/sdcard/UCDownloads/12月', '/sdcard/UCDownloads/11月', True)
    # move_file_on_device('/sdcard/UCDownloads/12月', '/sdcard/UCDownloads/11月')
