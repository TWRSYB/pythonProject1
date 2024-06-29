import concurrent
import json
import os
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import pandas
import requests
from lxml import etree

from A_08_m3u8.M3u8ToMp4 import M3u8ToMp4
from PC_00_Common.LogUtil.LogUtil import async_log
from PC_05_91GCYY.Config import URL_HOST, FILE_JSON_CURRENT, FILE_JSON_ALL, FILE_EXCEL_CURRENT, \
    FILE_EXCEL_ALL, DIR_OUTPUT, HEADERS, FILE_JSON_ALL_CATEGORY, DIR_CATEGORY, FILE_JSON_CURRENT_CATEGORY, \
    FILE_EXCEL_CURRENT_CATEGORY, FILE_EXCEL_ALL_CATEGORY
from A_07_Utils.ExcelUtils import format_excel_text
from PC_00_Common.LogUtil import LogUtil
from PC_00_Common.ReqUtil import SavePicUtil
from PC_00_Common.XpathUtil.XpathUtil import xpath_util

# 创建session对象
from PC_00_Common.ReqUtil import ReqUtil
from PC_05_91GCYY.Vo.Category import Category
from PC_05_91GCYY.Vo.CheckResult import CheckResult
from PC_05_91GCYY.Vo.VoVideoInfo import VoVideoInfo

session = requests.Session()
session.headers = HEADERS
session.cookies.set('existmag', 'all')
session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=50))

save_pic_util = SavePicUtil.SavePicUtil(session=session)
req_util = ReqUtil.ReqUtil(session=session)


def get_task_img(task: VoVideoInfo, dir_img):
    """
    获取影片图片并保存
    :param task: 影片任务
    :param dir_img: 图像保存目录
    :return: None
    """
    save_pic_util.save_pic(task.img_src, dir_img, task.get_name())


def get_task_m3u8(task: VoVideoInfo, dir_m3u8):
    """
    获取影片M3U8并保存
    :param task: 影片任务
    :param dir_m3u8: m3u8保存目录
    :return: None
    """
    res_get_m3u8 = req_util.try_get_req_times(f'{URL_HOST}{task.m3u8_url}', msg=f'获取.m3u8文件')
    if not res_get_m3u8:
        return
    with open(os.path.join(dir_m3u8, f'{task.get_name()}.m3u8'), 'w', encoding='utf-8') as m3u8_file:
        m3u8_file.write(add_key_uri_for_m3u8_content(res_get_m3u8.text))
    # 如果有完整.m3u8, 则获取
    if task.m3u8_url.endswith('ca4be0'):
        dir_m3u8_ca49e0 = f'{dir_m3u8}_ca49e0'
        os.makedirs(dir_m3u8_ca49e0, exist_ok=True)
        res_get_m3u8_ca49e0 = req_util.try_get_req_times(f'{URL_HOST}{task.m3u8_url.replace("ca4be0", "ca49e0")}',
                                                         msg=f'获取完整.m3u8文件')
        if not res_get_m3u8_ca49e0:
            return
        with open(os.path.join(dir_m3u8_ca49e0, f'{task.get_name().replace("ca4be0", "ca49e0")}.m3u8'),
                  'w', encoding='utf-8') as m3u8_file:
            m3u8_file.write(add_key_uri_for_m3u8_content(res_get_m3u8_ca49e0.text))


def save_data(list_vo, list_json_all: list,
              dir_output, path_file_json_current, path_file_json_all, path_file_excel_current, path_file_excel_all,
              process_level=4):
    """
    保存数据
    :param list_vo: 本次新加入的数据
    :param list_json_all: 所有数据
    :param dir_output: 保存目录
    :param path_file_json_current: 本次 json 输出文件
    :param path_file_json_all: 所有 json 输出文件
    :param path_file_excel_current: 本次 EXCEL 输出文件
    :param path_file_excel_all: 所有 EXCEL 输出文件
    :param process_level: 过程等级
    :return: None
    """
    # 保存 Json 文件 ↓↓↓
    # 输出本次 Json 文件 ↓↓↓
    with open(path_file_json_current, 'w', encoding='utf-8') as f:
        json.dump([task.__dict__ for task in list_vo], f, ensure_ascii=False, indent=4)
    LogUtil.process_log.process(process_level, f'输出本次Json成功', obj=path_file_json_current)
    # 输出本次 Json 文件 ↑↑↑
    # 将本次数据合并到现有 Json 中 ↓↓↓
    for vo in list_vo:
        if not vo.in_dict_list(list_json_all):
            list_json_all.append(vo.__dict__)
    with open(path_file_json_all, "w", encoding='utf-8') as f:  # 将合并后的数据写回JSON文件
        json.dump(list_json_all, f, ensure_ascii=False, indent=4)  # indent 参数可选，用于美化输出（增加缩进）
    LogUtil.process_log.process(process_level, f'输出所有Json成功', obj=path_file_json_all)
    # 将本次数据合并到现有 Json 中 ↑↑↑
    # 保存 Json 文件 ↑↑↑

    # 保存 Excel 文件 ↓↓↓
    # 输出本次 Excel 文件 ↓↓↓
    df = pandas.DataFrame(([task.__dict__ for task in list_vo])).astype(
        str)  # 将列表转换为 DataFrame , 格式为 str , 避免 Excel 以数字和科学计数法显示
    df.to_excel(path_file_excel_current, index=False)  # 将DataFrame保存到Excel文件, index=False表示不保存行索引到Excel文件
    format_excel_text(path_file_excel_current)
    LogUtil.process_log.process(process_level, f'输出本次Excel成功', obj=path_file_excel_current)
    # 输出本次 Excel 文件 ↑↑↑
    # 输出所有 Excel 文件 ↓↓↓
    df = pandas.DataFrame(list_json_all).astype(str)
    df.to_excel(path_file_excel_all, index=False)  # 将DataFrame保存到Excel文件, index=False表示不保存行索引到Excel文件
    format_excel_text(path_file_excel_all)
    LogUtil.process_log.process(process_level, f'输出所有Excel成功', obj=path_file_excel_all)
    # 输出所有 Excel 文件 ↑↑↑
    # 保存 Excel 文件 ↑↑↑

    # 备份数据 ↓↓↓
    backup_folder_name = os.path.join(dir_output, f'Backup_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}')
    os.makedirs(backup_folder_name)
    shutil.copy2(path_file_json_current, backup_folder_name)
    shutil.copy2(path_file_json_all, backup_folder_name)
    shutil.copy2(path_file_excel_current, backup_folder_name)
    shutil.copy2(path_file_excel_all, backup_folder_name)
    LogUtil.process_log.process(process_level, f'备份数据成功', obj=backup_folder_name)
    # 备份数据 ↑↑↑


def get_save_path_by_category_code(category_code):
    """
    获取分类的输出目录
    :param category_code: 分类代码
    :return: 分类保存目录, m3u8保存目录, 图片保存目录
    """
    dir_save = os.path.join(DIR_OUTPUT, category_code)
    dir_m3u8 = os.path.join(dir_save, 'M3U8')
    dir_img = os.path.join(dir_save, 'IMG')
    os.makedirs(dir_save, exist_ok=True)
    os.makedirs(dir_m3u8, exist_ok=True)
    os.makedirs(dir_img, exist_ok=True)
    return dir_save, dir_m3u8, dir_img


def get_task_resource(vo_video_info: VoVideoInfo, dir_m3u8, dir_img):
    """
    获取影片资源
    :param vo_video_info: 影片信息
    :param dir_m3u8: m3u8保存目录
    :param dir_img: 图片保存目录
    :return:
    """
    get_task_m3u8(vo_video_info, dir_m3u8)
    get_task_img(vo_video_info, dir_img)


def add_key_uri_for_m3u8(dir_m3u8, process_level: int):
    """
    为目录下的.m3u8文件添加KEY_URI
    :param dir_m3u8: m3u8目录
    :param process_level: 进程等级
    :return: None
    """
    for index, file_m3u8 in enumerate(Path(dir_m3u8).glob('*.m3u8')):
        LogUtil.set_process(process_level, index + 1)
        LogUtil.process_log.process_start(process_level, msg='为.m3u8添加key_uri', order=index + 1)
        with file_m3u8.open('r') as file:
            content = file.read()
        # 使用正则表达式替换文本
        replaced_content = re.sub(r'URI=".+/sec"', f'URI="{URL_HOST}/sec"', content)
        # 另存为新文件
        dir_m3u8_add_key_uri = f'{dir_m3u8}_ADD_KEY_URI'
        os.makedirs(dir_m3u8_add_key_uri, exist_ok=True)
        with open(os.path.join(dir_m3u8_add_key_uri, file_m3u8.name), 'w', encoding='utf-8') as new_file:
            new_file.write(replaced_content)
        LogUtil.process_log.process_end(process_level, msg='为.m3u8添加key_uri', order=index + 1)


def add_key_uri_for_m3u8_content(m3u8_content):
    """
    为 m3u8内容添加KEY_URI
    :param m3u8_content: m3u8内容
    :return: 添加完整KEY_URI之后的内容
    """
    return re.sub(r'URI=".+/sec"', f'URI="{URL_HOST}/sec"', m3u8_content)


def check_category(category, list_task_category: [VoVideoInfo], process_level) -> CheckResult:
    """
    检查分类
    :param category: 分类对象
    :param list_task_category: 分类获取的影片列表
    :param process_level: 进程等级
    :return: 检查结果
    """
    if category.page_count:
        dir_m3u8 = os.path.join(DIR_OUTPUT, category.category_code, 'M3U8')
        dir_img = os.path.join(DIR_OUTPUT, category.category_code, 'IMG')
        list_video_id = [vo_video_info.video_id for vo_video_info in list_task_category]
        set_video_id = set(list_video_id)  # video_id集合
        list_m3u8_id = [file_name.split('_', 1)[0] for file_name in os.listdir(dir_m3u8)]
        list_img_id = [file_name.split('_', 1)[0] for file_name in os.listdir(dir_img)]
        check_result = CheckResult(category=category, list_video_id=list_video_id, set_video_id=set_video_id,
                                   list_m3u8_id=list_m3u8_id, list_img_id=list_img_id)
        return check_result


def get_video_info(video_id, category_code, data_ratio='', vip_type='', play_times='', page_order='',
                   process_level: int = 4):
    href = f"/vid/{video_id}.html"
    res_video_page = req_util.try_get_req_times(f'{URL_HOST}{href}')
    if not res_video_page:
        LogUtil.process_log.process(process_level, msg='打开影片页面失败', obj=video_id, level=LogUtil.Level.ERROR)
        return
    res_video_page_etree = etree.HTML(res_video_page.text)
    title = xpath_util.get_unique(res_video_page_etree, xpath='//div/h1[contains(@class, "mb10")]/text()',
                                  msg='获取 title')
    script = xpath_util.get_unique(res_video_page_etree, xpath='//body/script/text()', msg='获取 script')
    m3u8_url = re.search(r"const m3u8_url = '(.+)';", script).group(1)
    img_src = re.search(r"const pic_thumbnail = '(.+)';", script).group(1)
    vo_video_info = VoVideoInfo(video_id=f'{video_id}', href=href, title=title, category=category_code,
                                data_ratio=data_ratio,
                                img_src=img_src,
                                vip_type=vip_type, play_times=play_times, m3u8_url=m3u8_url,
                                page_order=page_order)
    return vo_video_info


class Executor:
    def __init__(self):
        self.list_category: [Category] = []
        self.list_category_json_all = []
        self.list_task: [VoVideoInfo] = []
        self.list_json_all = []
        # 读取现有JSON文件中的数据
        if os.path.isfile(FILE_JSON_ALL):
            with open(FILE_JSON_ALL, 'r', encoding='utf-8') as json_file:
                self.list_json_all = json.load(json_file)

        # 读取现有JSON文件中的数据
        if os.path.isfile(FILE_JSON_ALL_CATEGORY):
            with open(FILE_JSON_ALL_CATEGORY, 'r', encoding='utf-8') as json_file:
                self.list_category_json_all = json.load(json_file)

    def start(self):
        process_level = 1

        # 获取分类
        if LogUtil.set_process(process_level, 1):
            LogUtil.process_log.process_skip(process_level, '获取分类')
        else:
            LogUtil.process_log.process_start(process_level, '获取分类')
            self.get_category()
            LogUtil.process_log.process_end(process_level, '获取分类')
        # 获取影片
        if LogUtil.set_process(process_level, 2):
            LogUtil.process_log.process_skip(process_level, '获取影片')
        else:
            LogUtil.process_log.process_start(process_level, '获取影片')
            self.get_task()
            LogUtil.process_log.process_end(process_level, '获取影片')
        # 下载并合并为 mp4
        if LogUtil.set_process(process_level, 3):
            LogUtil.process_log.process_skip(process_level, '下载并合并为 mp4')
        else:
            LogUtil.process_log.process_start(process_level, '下载并合并为 mp4')
            self.download_and_merge_mp4()
            LogUtil.process_log.process_end(process_level, '下载并合并为 mp4')

    def get_category(self, process_level=2):
        """
        获取分类
        :param process_level: 进程级别
        :return: None
        """
        res_home_page = req_util.try_get_req_times(url=f'{URL_HOST}')
        if not res_home_page:
            return
        etree_res_home_page = etree.HTML(res_home_page.text)  # 初始化生成一个XPath解析对象
        list_category_home = etree_res_home_page.xpath('//div/ul/li/a[contains(@href,"/category")]')
        for index, category_home in enumerate(list_category_home):
            if LogUtil.set_process(process_level, index + 1):
                LogUtil.process_log.process_skip(process_level, msg='获取首页分类', order=index + 1)
                continue
            LogUtil.process_log.process_start(process_level, msg='获取首页分类', order=index + 1)
            href = xpath_util.get_unique(category_home, './@href')
            category_code = href.replace('/category/', '')
            category_name = xpath_util.get_unique(category_home, './text()')
            category = Category(category_code, category_name, href)
            self.list_category.append(category)
            self.get_sub_category(category)
            LogUtil.process_log.process_end(process_level, msg='获取首页分类', order=index + 1, obj=category)
        save_data(list_vo=self.list_category, list_json_all=self.list_category_json_all, dir_output=DIR_CATEGORY,
                  path_file_json_current=FILE_JSON_CURRENT_CATEGORY, path_file_json_all=FILE_JSON_ALL_CATEGORY,
                  path_file_excel_current=FILE_EXCEL_CURRENT_CATEGORY, path_file_excel_all=FILE_EXCEL_ALL_CATEGORY,
                  process_level=process_level + 1)

    def get_sub_category(self, category):
        """
        完善分类或获取子分类
        :param category: 分类
        :return: None
        """
        res_category = req_util.try_get_req_times(url=f'{URL_HOST}/category/{category.category_code}')
        if not res_category:
            return
        etree_res_category = etree.HTML(res_category.text)  # 初始化生成一个XPath解析对象
        page_count = 0
        list_sub_category_item = etree_res_category.xpath(
            '//div[contains(@class,"home-tab")]/div[contains(@class,"mb15")]')
        # 有子分类获取子分类
        if len(list_sub_category_item) > 0:
            category.list_sub_category_code = []
            for index, sub_category_item in enumerate(list_sub_category_item):
                LogUtil.set_process(3, index + 1)
                LogUtil.process_log.process_start(3, f'获取子分类', order=index + 1, obj=category)
                href = xpath_util.get_unique(sub_category_item, './a/@href')
                category_code = href.replace('/category/', '')
                category_name = xpath_util.get_unique(sub_category_item, './div/text()')
                sub_category = Category(category_code, category_name, href, super_category_code=category.category_code,
                                        page_count=page_count)
                category.list_sub_category_code.append(category_code)
                self.list_category.append(sub_category)
                self.get_sub_category(sub_category)
                LogUtil.process_log.process_end(3, f'获取子分类', order=index + 1, obj=sub_category)
        # 没有子分类完善分类
        else:
            list_page_bar_item = etree_res_category.xpath('//div[contains(@class,"pagebar")]/li/*/text()')
            page_count = 1
            vip_type = xpath_util.get_unique(etree_res_category, xpath='//li[@class="mb15"]/a/*[@class="vip"]/text()',
                                             msg='获取 vip_type')
            if len(list_page_bar_item) > 0:
                page_count = max(
                    [int(page_bar_item) for page_bar_item in list_page_bar_item if re.match(r'\d+', page_bar_item)])
            category.page_count = page_count
            category.vip_type = vip_type
            category.list_sub_category_code = None

    def get_task(self, process_level=2):
        """
        获取任务
        :param process_level: 进程等级
        :return: None
        """
        if len(self.list_category) > 0:
            for index, category in enumerate(self.list_category):
                order = index + 1
                if LogUtil.set_process(process_level, order):
                    LogUtil.process_log.process_skip(process_level, f"获取本次分类数据", order=order, obj=category)
                    continue
                LogUtil.process_log.process_start(process_level, f"获取本次分类数据", order=order, obj=category)
                list_task_category = self.read_category(category)
                LogUtil.process_log.process_end(process_level, f"获取本次分类数据", order=order, obj=list_task_category)
        else:
            for index, category in enumerate(self.list_category_json_all):
                order = index + 1
                if LogUtil.set_process(process_level, order):
                    LogUtil.process_log.process_skip(process_level, f"获取所有分类数据", order=order, obj=category)
                    continue
                LogUtil.process_log.process_start(process_level, f"获取所有分类数据", order=order, obj=category)
                list_task_category = self.read_category(Category(**category))
                LogUtil.process_log.process_end(process_level, f"获取所有分类数据", order=order, obj=list_task_category)

    def read_category(self, category, process_level: int = 3):
        """
        读取分类数据
        :param category: 分类对象
        :param process_level: 进程等级
        :return: 分类影片列表
        """
        list_task_category = []
        # 分页获取 ↓↓↓
        category_code = category.category_code
        page_count = category.page_count
        for i in range(0, page_count):
            page = i + 1
            if LogUtil.set_process(process_level, page):
                LogUtil.process_log.process_skip(process_level, f"读取页", order=page)
                continue
            LogUtil.process_log.process_start(process_level, f"读取页", order=page)
            list_page_task = self.read_page(category_code, page, process_level + 1)
            list_task_category.extend(list_page_task)
            LogUtil.process_log.process_end(process_level, f"读取页", order=page, obj=list_page_task)
        # 分页获取 ↑↑↑
        # 检查缺失情况 ↓↓↓
        LogUtil.process_log.process_start(process_level, '检查缺失情况', obj=category)
        check_result = check_category(category=category, list_task_category=list_task_category,
                                      process_level=process_level + 1)

        if check_result:
            if check_result.is_no_duplicate and check_result.is_file_complete:
                LogUtil.process_log.process(process_level, msg=f'分类检查结果: 完全正常', obj=check_result)
            else:
                if not check_result.is_file_complete:
                    LogUtil.process_log.process(process_level, msg=f'分类检查结果: 资源不全', obj=check_result,
                                                level=LogUtil.Level.ERROR)
                if not check_result.is_no_duplicate:
                    LogUtil.process_log.process(process_level, msg=f'分类检查结果: 有重复不全', obj=check_result,
                                                level=LogUtil.Level.ERROR)
                    LogUtil.process_log.process_start(process_level, msg='补全数据')
                    self.complete_data(check_result, list_task=list_task_category, process_level=process_level + 1)
                    LogUtil.process_log.process_end(process_level, msg='补全数据')

        LogUtil.process_log.process_end(process_level, '检查缺失情况', obj=check_result)
        # 检查缺失情况 ↑↑↑
        return list_task_category

    def read_page(self, category_code, page, process_level: int = 4):
        dir_save, dir_m3u8, dir_img = get_save_path_by_category_code(category_code)
        list_page_task = []
        res_page = req_util.try_get_req_times(url=f'{URL_HOST}/category/{category_code}', params={'page': page})
        if not res_page:
            return
        res_page_etree = etree.HTML(res_page.text)  # 初始化生成一个XPath解析对象

        mb15_list = res_page_etree.xpath('//li[@class="mb15"]')

        if len(mb15_list) < 1:
            return
        for index, mb15 in enumerate(mb15_list):
            order = index + 1
            if LogUtil.set_process(process_level, order):
                LogUtil.process_log.process_skip(process_level, f"获取影片详情", order, obj=category_code)
                continue
            LogUtil.process_log.process_start(process_level, f"获取影片详情", order, obj=category_code)
            href = xpath_util.get_unique(mb15, xpath='./a/@href', msg='获取 href')
            video_id = re.search(r"/vid/(.+).html", href).group(1)
            # title = xpath_util.get_unique(mb15, xpath='./a/@title', msg='获取 title')
            # img_src = xpath_util.get_unique(mb15, xpath='./a/img/@data-src', msg='获取 img_src')
            data_ratio = xpath_util.get_unique(mb15, xpath='./a/@data-ratio', msg='获取 data_ratio')
            vip_type = xpath_util.get_unique(mb15, xpath='./a/*[@class="vip"]/text()', msg='获取 vip_type')
            play_times = xpath_util.get_unique(mb15, xpath='./a/*[@class="ico-right"]/text()', msg='获取 play_times')
            page_order = f'{page}_{order}'
            vo_video_info = get_video_info(video_id=f'{video_id}', category_code=category_code,
                                           data_ratio=data_ratio, vip_type=vip_type,
                                           play_times=play_times,
                                           page_order=page_order,
                                           process_level=process_level)
            if vo_video_info:
                get_task_resource(vo_video_info, dir_m3u8, dir_img)
                list_page_task.append(vo_video_info)
            LogUtil.process_log.process_end(process_level, f"获取影片详情", order, obj=vo_video_info)
        self.list_task += list_page_task
        self.save_task(list_page_task, dir_save)
        return list_page_task

    def save_task(self, list_task, dir_save):
        save_data(list_task, list_json_all=self.list_json_all,
                  dir_output=dir_save,
                  path_file_json_current=FILE_JSON_CURRENT, path_file_json_all=FILE_JSON_ALL,
                  path_file_excel_current=FILE_EXCEL_CURRENT, path_file_excel_all=FILE_EXCEL_ALL)

    # 通过video_id获取影片
    def get_video_by_list_video_id(self, list_video_id, category_code, list_task=None,
                                   page_order: str = '未获取: 通过video_id获取影片',
                                   process_level: int = 4):
        list_task = list_task if list_task else []
        dir_save, dir_m3u8, dir_img = get_save_path_by_category_code(category_code)
        for index, video_id in enumerate(list_video_id):
            order = index + 1
            LogUtil.process_log.process_start(process_level, f"获取影片详情", order, obj=category_code)
            data_ratio = '未获取: 通过video_id获取影片'
            vip_type = '未获取: 通过video_id获取影片'
            play_times = '未获取: 通过video_id获取影片'
            vo_video_info = get_video_info(video_id=f'{video_id}', category_code=category_code,
                                           data_ratio=data_ratio, vip_type=vip_type,
                                           play_times=play_times,
                                           page_order=page_order,
                                           process_level=process_level)
            if vo_video_info:
                get_task_resource(vo_video_info, dir_m3u8, dir_img)
                list_task.append(vo_video_info)
            LogUtil.process_log.process_end(process_level, f"获取影片详情", order, obj=vo_video_info)
        self.list_task += list_task
        self.save_task(list_task, dir_save)
        return list_task

    def complete_data(self, check_result: CheckResult, list_task=None, process_level: int = 4):
        if not check_result.is_no_duplicate:
            list_video_id_maybe_lost = []
            set_video_id = check_result.set_video_id
            set_video_id_int = [int(video_id) for video_id in set_video_id]
            max_video_id = max(set_video_id_int)
            min_video_id = min(set_video_id_int)
            count_diff = len(check_result.list_video_id) - len(check_result.set_video_id)
            for video_id in range(min_video_id - count_diff, max_video_id + 1 + count_diff):
                if video_id not in set_video_id_int:
                    list_video_id_maybe_lost.append(video_id)
            if len(list_video_id_maybe_lost) > 0:
                LogUtil.process_log.process(process_level,
                                            msg=f'分类 {check_result.category} 缺失 {count_diff} 个, 可能得缺失列表: {list_video_id_maybe_lost}')
                list_task = self.get_video_by_list_video_id(list_video_id_maybe_lost,
                                                            category_code=check_result.category.category_code,
                                                            list_task=list_task,
                                                            process_level=process_level)
                LogUtil.process_log.process(process_level,
                                            msg=f'分类 {check_result.category} 缺失 {count_diff} 个, 补全 {len(list_task)} 个, 补全列表: {list_task}')
        else:
            LogUtil.process_log.process(process_level, msg='分类没有重复, 无需补全', obj=check_result)

    def download_and_merge_mp4(self, process_level=2):
        for index, category_json in enumerate(self.list_category_json_all):
            order = index + 1
            if LogUtil.set_process(process_level, order):
                LogUtil.process_log.process_skip(process_level, f"下载并合并分类的影片", order=order, obj=category_json)
                continue
            LogUtil.process_log.process_start(process_level, f"下载并合并分类的影片", order=order, obj=category_json)
            category = Category(**category_json)
            dir_m3u8 = os.path.join(DIR_OUTPUT, category.category_code, 'M3U8_ca49e0_ADD_KEY_URI')
            if os.path.isdir(dir_m3u8):
                LogUtil.process_log.process(process_level, '分类有m3u8文件夹', obj=category.category_code)
                m3u8_files_without_mp4 = []
                m3u8_files_with_mp4 = []
                Path_m3u8 = Path(dir_m3u8)
                # 获取指定目录下所有的 .m3u8 文件
                m3u8_files = [m3u8_file for m3u8_file in Path_m3u8.glob('*.m3u8')]
                # 获取指定目录下所有的 .mp4 文件
                list_mp4_name = [mp4_file.stem for mp4_file in Path_m3u8.glob('*.mp4')]

                for m3u8_file in m3u8_files:
                    if m3u8_file.stem in list_mp4_name:
                        m3u8_files_with_mp4.append(m3u8_file)
                    else:
                        m3u8_files_without_mp4.append(m3u8_file)
                LogUtil.process_log.process(process_level,
                                            f'分类{category.category_code}扫描结果: m3u8数量={len(m3u8_files)}, mp4数量={len(list_mp4_name)}'
                                            f', 有mp4的m3u8数量={len(m3u8_files_with_mp4)}, 没有mp4的m3u8数量={len(m3u8_files_without_mp4)}')
                if len(m3u8_files_without_mp4) > 0:
                    # 使用ThreadPoolExecutor来并行处理M3u8文件
                    set_future = set()
                    with ThreadPoolExecutor(max_workers=3) as executor:  # 可根据实际情况调整max_workers的数量
                        for i, m3u8_file in enumerate(m3u8_files_without_mp4):
                            m3u8_to_mp4 = M3u8ToMp4(path_m3u8_file=m3u8_file,
                                                    dir_cache=os.path.join(os.getcwd(), 'OutputData', category.category_code),
                                                    log=async_log)
                            future = executor.submit(m3u8_to_mp4.download_and_merge_by_m3u8_file)
                            set_future.add(future)
                    # 收集所有完成的Future对象的结果（可选，根据需要处理结果或异常）
                    for future in concurrent.futures.as_completed(set_future):
                        LogUtil.process_log.process(process_level + 1, f'得到 下载并合并 结果 {future.result()}')
                        try:
                            result = future.result()
                            if result[0]:
                                LogUtil.process_log.process(process_level, f'下载并合并完成, 执行结果: {result}')
                            else:
                                LogUtil.process_log.process(process_level, f'下载并合并 失败: {future.result()}', level=LogUtil.Level.ERROR)
                        except Exception as exc:
                            LogUtil.process_log.process(process_level, f'下载并合并遇到异常, 异常: {exc}', level=LogUtil.Level.ERROR)
            else:
                LogUtil.process_log.process(process_level, f'分类{category.category_code}没有m3u8文件夹')
            LogUtil.process_log.process_end(process_level, f"下载并合并分类的影片", order=order, obj=category)
