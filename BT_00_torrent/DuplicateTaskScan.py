import sys
from pathlib import Path

from A_03_Common.InputCheck import input_check
from BT_00_torrent.ScanTorrentAndOpen import find_torrent_files

if __name__ == '__main__':
    main_task_dir = input_check("请输入当前任务文件夹:", True, 'dir')
    main_task_torrent = find_torrent_files(main_task_dir)
    print(f'当前任务文件夹扫描到{len(main_task_torrent)}个torrent文件')
    main_task_torrent = [Path(torrent).name for torrent in main_task_torrent]
    for torrent in main_task_torrent:
        print(torrent)



    # scan_task_dir =  input_check("请输入扫描文件夹:", True, 'dir')
    # if scan_task_dir in main_task_dir:
    #     print('当前任务文件夹包含扫描文件夹或一致, 任务退出')
    #     sys.exit()
    # scan_task_torrent = find_torrent_files(scan_task_dir)
    # print(f'扫描文件夹扫描到{len(main_task_torrent)}个torrent文件')

    # for torrent in scan_task_torrent:
    #     # info_hash = get_torrent_info_hash(torrent)
    #     # print(f"Torrent 文件的 info_hash 是: {info_hash}", torrent)
    #     print(type(torrent), torrent)