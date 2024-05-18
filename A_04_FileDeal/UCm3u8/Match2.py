import os
import re
import shutil
from collections import defaultdict
from pathlib import Path


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
        return (f'is_mp4_all_matched_last: {self.is_mp4_all_matched_last}, '
                f'is_mp4_all_matched_max: {self.is_mp4_all_matched_max}, '
                f'm3u8_full_name: {self.m3u8.name_full}')


def scan_files(directory, extension, parser_func):
    """Scans a directory for files with a given extension and applies parsing function."""
    path = Path(directory)
    return [parser_func(file.stem, file) for file in path.glob(f'*.{extension}')]


def parse_file_name(full_name, file_path=None):
    """Parses the file name to extract relevant information."""
    match = re.match(r'(.+)_(\d+)\.(mp4|m3u8)', full_name)
    if match:
        name_video, ts = match.groups()
        if file_path:
            file_size = os.path.getsize(file_path)
            file_time = os.path.getmtime(file_path)
            return name_video, int(ts), file_size, file_time
        else:
            return name_video, int(ts)
    raise ValueError(f"Invalid file name format: {full_name}")


def main():
    try:
        dir_m3u8 = input('请输入m3u8文件所在目录:')
        list_vo_m3u8 = scan_files(dir_m3u8, 'm3u8', lambda n, p: VoM3u8(p.name, *parse_file_name(n)))

        dir_mp4 = input('请输入mp4所在目录:')
        list_vo_mp4 = scan_files(dir_mp4, 'mp4', lambda n, p: VoMp4(p.name, *parse_file_name(n, p)))

        print(f'扫描到 {len(list_vo_m3u8)} 个m3u8文件')
        print(f'扫描到 {len(list_vo_mp4)} 个mp4文件')

        # 使用字典分组以提高匹配效率
        mp4_by_video = defaultdict(list)
        for mp4 in list_vo_mp4:
            mp4_by_video[mp4.name_video].append(mp4)

        list_vo_m3u8_match_mp4 = []
        for m3u8 in list_vo_m3u8:
            matched_mp4s = mp4_by_video[m3u8.name_video]
            last_mp4_ts = max(m.ts for m in matched_mp4s)
            max_mp4_size = max(m.file_size for m in matched_mp4s)
            all_matched_mp4 = next(
                (mp4 for mp4 in matched_mp4s if mp4.ts == last_mp4_ts and mp4.file_size == max_mp4_size), None)
            if all_matched_mp4:
                match_info = VoM3u8MatchMp4(m3u8, all_matched_mp4, matched_mp4s,
                                            all_matched_mp4.ts == last_mp4_ts,
                                            all_matched_mp4.file_size == max_mp4_size)
                list_vo_m3u8_match_mp4.append(match_info)
                print(match_info)

        if list_vo_m3u8_match_mp4:
            dir_target = input('输入要剪切的目标目录:')
            os.makedirs(dir_target, exist_ok=True)
            for match in list_vo_m3u8_match_mp4:
                shutil.move(match.mp4_all_matched.path, dir_target)
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main()
