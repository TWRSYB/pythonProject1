import os
import re

import requests
from lxml import etree

from PC_00_Common.ReqUtil import SavePicUtil, ReqUtil

session = requests.session()
session.headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '_ga=GA1.1.1908687187.1720705458; _ga_WF05TQ75CR=GS1.1.1726146019.3.1.1726146617.21.0.0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

host = 'https://cosblay.com'

main_url = host + '/140437.html'

save_pic_util = SavePicUtil.SavePicUtil(session=session)
req_util = ReqUtil.ReqUtil(session=session)

res_main = req_util.try_get_req_times(url=main_url)
etree_html = etree.HTML(res_main.text)
title = etree_html.xpath('//header[contains(@class,"entry-header")]/h1[contains(@class,"entry-title")]/text()')[0]
max_page = 200
page_bar_list = etree_html.xpath('//div[contains(@class,"entry-content")]//div[contains(@class,"pgntn-page-pagination-block")]/a/text()')
if len(page_bar_list) == 0:
    max_page = 1
else:
    try:
        max_page=int(page_bar_list[-1])
    except ValueError:
        max_page = int(page_bar_list[-2])
chars_cant_in_filename = r'[\\/:"*?<>|]+'
title = re.sub(chars_cant_in_filename, '_', title)
path_output = f'./OutputData/{title}'
print(f'保存目录{path_output}')
print(f'最大页数{max_page}')
os.makedirs(path_output, exist_ok=True)

idx = 1
for page in range(1, max_page+1):
    res_get_page = req_util.try_get_req_times(url=f'{main_url}/{page}')
    if res_get_page:
        etree_html = etree.HTML(res_get_page.text)

        list_pic_url = etree_html.xpath('//div[contains(@class,"entry-content")]/p/a/img/@src')
        for url in list_pic_url:
            url_pic = url.replace('i0.wp.com/', '')
            name_pic = url_pic.split('/')[-1].split('.')[0]
            save_pic_util.save_pic(url=f'{url_pic}', save_dir=path_output, save_name=f'{str(idx).zfill(3)}_{name_pic}', is_async=True)
            idx+=1

