import os
import re
import shutil


class VoMp4:
    def __init__(self, name_full, name_video, ts, tm, file_size, path):
        self.name_full = name_full
        self.name_video = name_video
        self.ts = ts
        self.tm = tm
        self.file_size = file_size
        self.path = path


class VoM3u8:
    def __init__(self, name_full, name_video, ts):
        self.name_full = name_full
        self.name_video = name_video
        self.ts = ts


class VoM3u8MatchMp4:
    def __init__(self, m3u8: VoM3u8, mp4_all_matched: VoMp4, list_mp4_matched_name_video: [],
                 is_mp4_all_matched_last, is_mp4_all_matched_max):
        self.m3u8 = m3u8
        self.mp4_all_matched = mp4_all_matched
        self.list_mp4_matched_name_video = list_mp4_matched_name_video
        self.is_mp4_all_matched_last = is_mp4_all_matched_last
        self.is_mp4_all_matched_max = is_mp4_all_matched_max

    def __str__(self):
        return f'is_mp4_all_matched_last: {self.is_mp4_all_matched_last}, is_mp4_all_matched_max: {self.is_mp4_all_matched_max}, m3u8_full_name: {self.m3u8.name_full}'


dir_m3u8 = input(f'请输入m3u8文件所在目录:')

list_vo_m3u8 = []

for item in os.listdir(dir_m3u8):
    if os.path.isfile(os.path.join(dir_m3u8, item)) and item.endswith(f'.m3u8'):
        match = re.match(r'(.+)_(\d+)\.m3u8', item)
        if match:
            name_video = match.group(1)
            ts = int(match.group(2))
            list_vo_m3u8.append(VoM3u8(item, name_video, ts))

print(f'扫描到 {len(list_vo_m3u8)} 个m3u8文件: {list_vo_m3u8}')

dir_mp4 = input(f'请输入mp4所在目录:')

list_vo_mp4 = []

for item in os.listdir(dir_mp4):
    file_path = os.path.join(dir_mp4, item)
    if os.path.isfile(file_path) and item.endswith(f'.mp4'):
        match = re.match(r'(.+)_(\d+)\.mp4', item)
        if match:
            name_video = match.group(1)
            ts = int(match.group(2))
            # 获取文件大小（以字节为单位）
            file_size = os.path.getsize(file_path)
            # 获取文件的最后修改时间
            file_time = os.path.getmtime(file_path)
            vo_mp4 = VoMp4(name_full=item, name_video=name_video, ts=ts, tm=file_time, file_size=file_size,
                           path=file_path)
            list_vo_mp4.append(vo_mp4)

print(f'扫描到 {len(list_vo_mp4)} 个mp4文件: {list_vo_mp4}')

list_vo_m3u8_match_mp4 = []

for vo_m3u8 in list_vo_m3u8:
    list_mp4_matched_name_video = []
    mp4_all_matched = None
    for vo_mp4 in list_vo_mp4:
        if vo_m3u8.name_video == vo_mp4.name_video:
            list_mp4_matched_name_video.append(vo_mp4)
        if vo_mp4.name_full.removesuffix('.mp4') == vo_m3u8.name_full.removesuffix('.m3u8'):
            mp4_all_matched = vo_mp4
    last_mp4_ts = max([int(vo_mp4.ts) for vo_mp4 in list_mp4_matched_name_video])
    max_mp4_size = max([vo_mp4.file_size for vo_mp4 in list_mp4_matched_name_video])
    vo_m3u8_match_mp4 = VoM3u8MatchMp4(vo_m3u8, mp4_all_matched=mp4_all_matched,
                                       list_mp4_matched_name_video=list_mp4_matched_name_video,
                                       is_mp4_all_matched_max=mp4_all_matched.file_size == max_mp4_size,
                                       is_mp4_all_matched_last=int(mp4_all_matched.ts) == last_mp4_ts)
    print(vo_m3u8_match_mp4)
    list_vo_m3u8_match_mp4.append(vo_m3u8_match_mp4)

if len(list_vo_m3u8_match_mp4) > 0:
    dir_target = input(f'输入要剪切的目标目录:')
    if not os.path.isdir(dir_target):
        os.makedirs(dir_target)
    for vo_m3u8_match_mp4 in list_vo_m3u8_match_mp4:
        shutil.move(vo_m3u8_match_mp4.mp4_all_matched.path, dir_target)
