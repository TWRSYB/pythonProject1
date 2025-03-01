import os
import re
import time

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
host = 'https://www.hitxhot.org'

save_pic_util = SavePicUtil.SavePicUtil(session=session)
req_util = ReqUtil.ReqUtil(session=session)


def download_gallery(gallery: dict):
    main_url = host + f'/gallerys/{gallery.get('key')}.html'
    res_get_first_page = req_util.try_get_req_times(url=f'{main_url}', params={'page': 1})

    etree_html = etree.HTML(res_get_first_page.text)
    title = etree_html.xpath('//title/text()')[0]

    max_page = int(title.rsplit('/', 1)[-1])
    print(f'max_page: {max_page}')
    gallery_name = title.rsplit('|', 1)[0].strip()
    chars_cant_in_filename = r'[\\/:"*?<>|]+'
    gallery_name = re.sub(chars_cant_in_filename, '_', gallery_name)
    path_output = f'./OutputData/{gallery_name}'
    os.makedirs(path_output, exist_ok=True)

    gallery['page'] = max_page
    gallery['gallery_name'] = gallery_name

    idx = 0
    for page in range(1, max_page + 1):

        print(f'Page: {page}')
        res_get_page = req_util.try_get_req_times(url=f'{main_url}', params={'page': page})
        if res_get_page:
            etree_html = etree.HTML(res_get_page.text)
            list_pic_url = etree_html.xpath('//div[contains(@class,"entry-content")]//a/img/@src')
            for url in list_pic_url:
                idx += 1
                url_pic = url.replace('i0.wp.com/', '').replace('i1.wp.com/', '').replace('i2.wp.com/', '')
                name_pic = url_pic.split('/')[-1].split('.')[0]
                save_pic_util.save_pic(url=f'{url_pic}', save_dir=path_output,
                                       save_name=f'{str(idx).zfill(3)}_{name_pic}',
                                       is_async=True, msg=f'图片序号{idx}')
    gallery['count'] = idx
    time.sleep(30)
    if len(os.listdir(path_output)) == idx:
        gallery['status'] = 1
    else:
        gallery['status'] = 2
    print(gallery)
    return gallery
