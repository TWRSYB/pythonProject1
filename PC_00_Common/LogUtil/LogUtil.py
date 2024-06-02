import logging
from enum import Enum

from PC_00_Common.LogUtil import LogUtil
from PC_00_Common.Config.Config import DIR_LOG
from PC_00_Common.Config import StartPoint

LOG_PATH_GLOBAL = f'{DIR_LOG}/Global_log.log'

LOG_PATH_PROCESS = f'{DIR_LOG}/Process_log.log'

LOG_PATH_COM_DEBUG = f'{DIR_LOG}/Com_debug.log'
LOG_PATH_COM_INFO = f'{DIR_LOG}/Com_info.log'
LOG_PATH_COM_WARNING = f'{DIR_LOG}/Com_warning.log'
LOG_PATH_COM_ERROR = f'{DIR_LOG}/Com_error.log'

LOG_PATH_PIC_DEBUG = f'{DIR_LOG}/Pic_debug.log'
LOG_PATH_PIC_INFO = f'{DIR_LOG}/Pic_info.log'
LOG_PATH_PIC_WARNING = f'{DIR_LOG}/Pic_warning.log'
LOG_PATH_PIC_ERROR = f'{DIR_LOG}/Pic_error.log'

LOG_PATH_ASYNC_DEBUG = f'{DIR_LOG}/Async_debug.log'
LOG_PATH_ASYNC_INFO = f'{DIR_LOG}/Async_info.log'
LOG_PATH_ASYNC_WARNING = f'{DIR_LOG}/Async_warning.log'
LOG_PATH_ASYNC_ERROR = f'{DIR_LOG}/Async_error.log'

LOG_PROCESS_1 = 0
LOG_PROCESS_2 = 0
LOG_PROCESS_3 = 0
LOG_PROCESS_4 = 0


class Level:
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'


def set_process(level: int, order: int):
    if level == 1:
        LogUtil.LOG_PROCESS_1 = order
        LogUtil.LOG_PROCESS_2 = 0
        LogUtil.LOG_PROCESS_3 = 0
        LogUtil.LOG_PROCESS_4 = 0
        if order < StartPoint.START_POINT_1:
            return True
        StartPoint.START_POINT_1 = 0
    elif level == 2:
        LogUtil.LOG_PROCESS_2 = order
        LogUtil.LOG_PROCESS_3 = 0
        LogUtil.LOG_PROCESS_4 = 0
        if order < StartPoint.START_POINT_2:
            return True
        StartPoint.START_POINT_2 = 0
    elif level == 3:
        LogUtil.LOG_PROCESS_3 = order
        LogUtil.LOG_PROCESS_4 = 0
        if order < StartPoint.START_POINT_3:
            return True
        StartPoint.START_POINT_3 = 0
    elif level == 4:
        LogUtil.LOG_PROCESS_4 = order
        if order < StartPoint.START_POINT_4:
            return True
        StartPoint.START_POINT_4 = 0


# 自定义日志参数赋值
class _FormatterWithSelfAttr(logging.Formatter):
    def format(self, record):
        record.process = f"{LOG_PROCESS_1}-{LOG_PROCESS_2}-{LOG_PROCESS_3}-{LOG_PROCESS_4}"
        return super(_FormatterWithSelfAttr, self).format(record)


formatter_with_process = _FormatterWithSelfAttr(fmt="%(asctime)s - %(process)s - %(levelname)s - %(message)s")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 全局日志配置
logging.basicConfig(format="%(asctime)s - %(process)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logging.Formatter = _FormatterWithSelfAttr

# 全局日志对象设置
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=LOG_PATH_GLOBAL, encoding='utf-8')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter_with_process)
logger.addHandler(handler)


# def msg_add_process(msg):
#     return f"{LOG_PROCESS_ACTRESSES_PAGE}-{LOG_PROCESS_ACTRESS_ORDER}-{LOG_PROCESS_MOVIE_PAGE}-{LOG_PROCESS_MOVIE_ORDER} - {msg}"


class ComLog:
    # 获取日志对象
    logger_com = logging.getLogger('logger_com')
    logger_com.setLevel(logging.DEBUG)

    # 创建日志文件处理器
    handler_debug = logging.FileHandler(filename=LOG_PATH_COM_DEBUG, encoding='utf-8')
    handler_info = logging.FileHandler(filename=LOG_PATH_COM_INFO, encoding='utf-8')
    handler_warning = logging.FileHandler(filename=LOG_PATH_COM_WARNING, encoding='utf-8')
    handler_error = logging.FileHandler(filename=LOG_PATH_COM_ERROR, encoding='utf-8')
    # 为处理器设置级别
    handler_debug.setLevel(logging.DEBUG)
    handler_info.setLevel(logging.INFO)
    handler_warning.setLevel(logging.WARNING)
    handler_error.setLevel(logging.ERROR)
    # 为处理器设置格式
    handler_debug.setFormatter(formatter_with_process)
    handler_info.setFormatter(formatter_with_process)
    handler_warning.setFormatter(formatter_with_process)
    handler_error.setFormatter(formatter_with_process)
    # 将处理器添加到日志对象中
    logger_com.addHandler(handler_debug)
    logger_com.addHandler(handler_info)
    logger_com.addHandler(handler_warning)
    logger_com.addHandler(handler_error)

    def debug(self, msg):
        self.logger_com.debug(msg)

    def info(self, msg):
        self.logger_com.info(msg)

    def warning(self, msg):
        self.logger_com.warning(msg)

    def error(self, msg):
        self.logger_com.error(msg)


class SavePicLog:
    # 获取日志对象
    logger_pic = logging.getLogger('logger_pic')
    logger_pic.setLevel(logging.DEBUG)

    # 创建日志文件处理器
    handler_debug = logging.FileHandler(filename=LOG_PATH_PIC_DEBUG, encoding='utf-8')
    handler_info = logging.FileHandler(filename=LOG_PATH_PIC_INFO, encoding='utf-8')
    handler_warning = logging.FileHandler(filename=LOG_PATH_PIC_WARNING, encoding='utf-8')
    handler_error = logging.FileHandler(filename=LOG_PATH_PIC_ERROR, encoding='utf-8')
    # 为处理器设置级别
    handler_debug.setLevel(logging.DEBUG)
    handler_info.setLevel(logging.INFO)
    handler_warning.setLevel(logging.WARNING)
    handler_error.setLevel(logging.ERROR)
    # 为处理器设置格式
    handler_debug.setFormatter(formatter)
    handler_info.setFormatter(formatter)
    handler_warning.setFormatter(formatter)
    handler_error.setFormatter(formatter)
    # 将处理器添加到日志对象中
    logger_pic.addHandler(handler_debug)
    logger_pic.addHandler(handler_info)
    logger_pic.addHandler(handler_warning)
    logger_pic.addHandler(handler_error)

    def debug(self, msg):
        self.logger_pic.debug(msg)

    def info(self, msg):
        self.logger_pic.info(msg)

    def warning(self, msg):
        self.logger_pic.warning(msg)

    def error(self, msg):
        self.logger_pic.error(msg)


class ProcessLog:
    # 获取进度日志对象
    logger_process_1 = logging.getLogger('logger_process_1')
    logger_process_2 = logging.getLogger('logger_process_2')
    logger_process_3 = logging.getLogger('logger_process_3')
    logger_process_4 = logging.getLogger('logger_process_4')
    logger_process_5 = logging.getLogger('logger_process_5')

    logger_process_1.setLevel(logging.DEBUG)
    logger_process_2.setLevel(logging.DEBUG)
    logger_process_3.setLevel(logging.DEBUG)
    logger_process_4.setLevel(logging.DEBUG)
    logger_process_5.setLevel(logging.DEBUG)

    # 创建日志文件处理器
    handler_1 = logging.FileHandler(filename=LOG_PATH_PROCESS, encoding='utf-8')
    handler_2 = logging.FileHandler(filename=LOG_PATH_PROCESS, encoding='utf-8')
    handler_3 = logging.FileHandler(filename=LOG_PATH_PROCESS, encoding='utf-8')
    handler_4 = logging.FileHandler(filename=LOG_PATH_PROCESS, encoding='utf-8')
    handler_5 = logging.FileHandler(filename=LOG_PATH_PROCESS, encoding='utf-8')

    # 为处理器设置级别
    handler_1.setLevel(logging.DEBUG)
    handler_2.setLevel(logging.DEBUG)
    handler_3.setLevel(logging.DEBUG)
    handler_4.setLevel(logging.DEBUG)
    handler_5.setLevel(logging.DEBUG)

    # 为处理器设置格式
    handler_1.setFormatter(
        logging.Formatter('%(asctime)s - %(process)s - %(levelname)s - %(message)s'))
    handler_2.setFormatter(
        logging.Formatter('\t%(asctime)s - %(process)s - %(levelname)s - %(message)s'))
    handler_3.setFormatter(
        logging.Formatter('\t\t%(asctime)s - %(process)s - %(levelname)s - %(message)s'))
    handler_4.setFormatter(
        logging.Formatter('\t\t\t%(asctime)s - %(process)s - %(levelname)s - %(message)s'))
    handler_5.setFormatter(
        logging.Formatter('\t\t\t\t%(asctime)s - %(process)s - %(levelname)s - %(message)s'))

    # 将处理器添加到日志对象中
    logger_process_1.addHandler(handler_1)
    logger_process_2.addHandler(handler_2)
    logger_process_3.addHandler(handler_3)
    logger_process_4.addHandler(handler_4)
    logger_process_5.addHandler(handler_5)

    list_logger = [logger_process_1, logger_process_2, logger_process_3, logger_process_4, logger_process_5]

    def process1(self, msg):
        self.logger_process_1.info(msg)

    def process2(self, msg):
        self.logger_process_2.info(msg)

    def process3(self, msg):
        self.logger_process_3.info(msg)

    def process4(self, msg):
        self.logger_process_4.info(msg)

    def process5(self, msg):
        self.logger_process_5.info(msg)

    def process_start(self, process_level: int, msg, order=None, obj=None, level: str = Level.INFO):
        msg = f'{msg} Start ↓↓↓↓↓'
        self.process(process_level, msg, order, obj, level)

    def process_end(self, process_level: int, msg, order=None, obj=None, level: str = Level.INFO):
        msg = f'{msg} End ↑↑↑↑↑'
        self.process(process_level, msg, order, obj, level)

    def process_skip(self, process_level: int, msg, order=None, obj=None, level: str = Level.INFO):
        msg = f'跳过 {msg}'
        self.process(process_level, msg, order, obj, level)

    def process(self, process_level: int, msg, order=None, obj=None, level: str = Level.INFO):
        # 确保 process_level 是一个有效的索引
        if not 0 < process_level <= len(self.list_logger):
            raise IndexError(f"Invalid process_level: {process_level}")

        msg = f'{msg} 第 {order} 个' if order else msg
        msg = f'{msg} obj: {obj}' if obj else msg

        # 使用字典映射来简化日志级别的处理
        log_methods = {Level.DEBUG: 'debug', Level.WARNING: 'warning', Level.ERROR: 'error', Level.INFO: 'info'}
        # 使用 get 方法，并指定默认值为 info 方法的名称
        method_name = log_methods.get(level, log_methods[Level.INFO])
        getattr(self.list_logger[process_level - 1], method_name)(msg)
        # getattr(com_log, method_name)(msg)

        # if level == Level.DEBUG:
        #     self.list_logger[process_level - 1].debug(msg)
        #     com_log.debug(msg)
        # elif level == Level.WARNING:
        #     self.list_logger[process_level - 1].warning(msg)
        #     com_log.warning(msg)
        # elif level == Level.ERROR:
        #     self.list_logger[process_level - 1].error(msg)
        #     com_log.error(msg)
        # else:
        #     self.list_logger[process_level - 1].info(msg)
        #     com_log.info(msg)


class AsyncLog:
    # 获取日志对象
    logger = logging.getLogger('logger_async')
    logger.setLevel(logging.DEBUG)

    # 创建不同级别日志文件对象处理器
    handler_debug = logging.FileHandler(filename=LOG_PATH_ASYNC_DEBUG, encoding='utf-8')
    handler_info = logging.FileHandler(filename=LOG_PATH_ASYNC_INFO, encoding='utf-8')
    handler_warning = logging.FileHandler(filename=LOG_PATH_ASYNC_WARNING, encoding='utf-8')
    handler_error = logging.FileHandler(filename=LOG_PATH_ASYNC_ERROR, encoding='utf-8')
    # 为处理器设置级别
    handler_debug.setLevel(logging.DEBUG)
    handler_info.setLevel(logging.INFO)
    handler_warning.setLevel(logging.WARNING)
    handler_error.setLevel(logging.ERROR)
    # 为处理器设置格式
    handler_debug.setFormatter(formatter_with_process)
    handler_info.setFormatter(formatter_with_process)
    handler_warning.setFormatter(formatter_with_process)
    handler_error.setFormatter(formatter_with_process)
    # 将处理器添加到日志对象中
    logger.addHandler(handler_debug)
    logger.addHandler(handler_info)
    logger.addHandler(handler_warning)
    logger.addHandler(handler_error)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)


com_log = ComLog()
process_log = ProcessLog()
async_log = AsyncLog()
save_pic_log = SavePicLog()
