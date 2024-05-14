import json
import logging
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='log.md')


# 设置自定义的ColoredFormatter
class ColoredFormatter(logging.Formatter):
    """自定义Formatter，添加颜色支持"""

    def format(self, record):
        levelname = record.levelname
        if levelname == 'ERROR':
            # 对于error级别，添加红色ANSI转义码
            levelname_color = f'\033[31m{levelname}\033[0m'
        else:
            levelname_color = levelname

        # 替换原levelname为带颜色的levelname
        record.levelname = levelname_color
        return super().format(record)

# 创建logger对象
logger = logging.getLogger(__name__)

# 创建handler并设置自定义格式
handler = logging.StreamHandler()
formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)

# 将handler添加到logger
logger.addHandler(handler)



class Target(object):

    def __init__(self, name, path, root) -> None:
        super().__init__()
        self.name = name
        self.path = path
        self.root = root

    def __str__(self) -> str:
        return "name:{}, path:{}, root:{}".format(self.name, self.path, self.root)


class RenameWorker:

    def __init__(self, cache_path):
        super().__init__()
        self.cache_path = cache_path
        self.directory = None
        self.target_video_name = "video.m4s"
        self.target_audio_name = "audio.m4s"
        self.target_file_info = "entry.json"

        self.task_list = list()
        self.run_path = os.path.abspath(os.path.join(os.path.abspath(__file__), ".."))

    def read_cache_path(self):
        self.search_path(self.cache_path)
        logger.info("识别到: {}个可合并视频。".format(len(self.task_list)))

    def search_path(self, root_path):
        for l in os.listdir(root_path):
            path = os.path.join(root_path, l)
            if os.path.isdir(path):
                self.search_path(path)
            else:
                if path.__contains__(self.target_video_name):
                    self.add_to_task_list(path)

    def add_to_task_list(self, path):
        parent_path = os.path.abspath(os.path.join(path, ".."))
        file_info_path = "{}/../{}".format(parent_path, self.target_file_info)
        with open(file_info_path, "r", encoding="utf-8") as f:
            file_info = json.load(f)
            t = Target(f'{file_info["title"]}_cid_{file_info["page_data"]["cid"]}', parent_path, "{}/../".format(parent_path))
            print(t)
            self.task_list.append(t)


def input_check(msg, not_null, path_type):
    the_input = input(msg)
    while True:
        if not_null and not the_input:
            the_input = input(f'输入不可为空, {msg}')
        elif path_type == 'file' and not os.path.isdir(the_input):
            the_input = input(f'输入不是文件, {msg}')
        elif path_type == 'dir' and not os.path.isdir(the_input):
            the_input = input(f'输入不是文件夹, {msg}')
        else:
            return the_input


if __name__ == '__main__':
    cache_path = input_check(msg='请输入缓存目录: ', not_null=True, path_type='dir')
    worker = RenameWorker(cache_path)
    worker.read_cache_path()
