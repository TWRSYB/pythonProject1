import inspect

import requests
import certifi

from PC_05_91GCYY.Config import HEADERS
from PC_05_91GCYY.Executor import VoVideoInfo

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

certifi.where()
print(certifi.where())

# r = requests.get('https://lp3-cdn-tos.bytecdntd.com/awimg/uuv/4707.jpg')
# # r = requests.get('https://img-blog.csdnimg.cn/293fdf861e804a4c97fe830181e6f334.png#pic_center', verify=certifi.where())
# print(r)
# print(r.content)
# print(r.text)

cls = VoVideoInfo

init_attribute_list = [key for key, value in inspect.signature(cls).parameters.items() if key != 'self']
# out_attribute_list = [attr for attr in dir(cls) if
#                       not callable(getattr(cls, attr)) and not attr.startswith('__')] + [
#                          key for key, value in vars(cls)['__annotations__'].items()]

# for attr in dir(cls):
#     print(attr)
#
for key, value in vars(cls)['__annotations__'].items():
    print(key)
# print(init_attribute_list)