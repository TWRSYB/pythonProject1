import os
import re

import requests
from lxml import etree

from PC_00_Common.ReqUtil import SavePicUtil, ReqUtil

session = requests.session()
session.headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '_ga=GA1.2.508997473.1728023357; _gid=GA1.2.1032131527.1728023357; _ga_BK7GVCDZKD=GS1.2.1728084964.2.1.1728085041.0.0.0',
    'referer': 'https://japanesebeauties.one/model/amateur-ayano/1/',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
host = 'https://japanesebeauties.one'

main_url = host + '/javhd/amateur-ayano'

save_pic_util = SavePicUtil.SavePicUtil(session=session)
req_util = ReqUtil.ReqUtil(session=session)

res_get_first_page = req_util.try_get_req_times(url=f'{main_url}/1')
res_get_first_page.encoding = 'utf-8'

etree_html = etree.HTML(res_get_first_page.text)
title = etree_html.xpath('//title/text()')[0]

gallery_name = title.strip()
chars_cant_in_filename = r'[\\/:"*?<>|]+'
gallery_name = re.sub(chars_cant_in_filename, '_', gallery_name)
path_output = f'./OutputData/{gallery_name}'
os.makedirs(path_output, exist_ok=True)


def reach_last_page(etree_html):
    container_middle = etree_html.xpath('//div[contains(@class,"container")]/div[contains(@class,"middle")]')[0]
    page_bar_list = container_middle.xpath('./div[contains(@class,"details")]/h2/a/text()')
    return 'Go!' in page_bar_list


page = 1
idx = 1
is_last_page = reach_last_page(etree_html)
while page == 1 or not is_last_page:
    res_get_page = req_util.try_get_req_times(url=f'{main_url}/{page}')
    if res_get_page:
        etree_html = etree.HTML(res_get_page.text)
        container_middle = etree_html.xpath('//div[contains(@class,"container")]/div[contains(@class,"middle")]')[0]
        list_pic_url = container_middle.xpath('./div[contains(@class,"full")]/a/img/@src')

        for url in list_pic_url:
            url_pic = url
            name_pic = url_pic.split('/')[-1].split('.')[0]
            save_pic_util.save_pic(url=f'{host}{url_pic}', save_dir=path_output,
                                   save_name=f'{str(idx).zfill(3)}_{name_pic}',
                                   is_async=True)
            idx += 1
        is_last_page = reach_last_page(etree_html)
    page += 1
