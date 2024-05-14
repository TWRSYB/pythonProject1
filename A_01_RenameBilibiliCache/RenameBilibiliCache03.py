import logging

from cm import RenameWorker
from A_03_Common.InputCheck import input_check

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='log.md')


# 设置自定义的ColoredFormatter
class ColoredFormatter(logging.Formatter):
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
handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))

# 将handler添加到logger
logger.addHandler(handler)


if __name__ == '__main__':
    cache_path = input_check(msg='请输入缓存目录: ', not_null=True, path_type='dir')
    worker = RenameWorker(cache_path, logger)
    worker.read_cache_path()
