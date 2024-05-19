# import os
# import time
#
# from my_util.input_util import no_empty_input
#
# option_dir_path = no_empty_input("请输入要操作的目录: ")
#
# # 获取当前时间的毫秒值
# option_millis = int(round(time.time() * 1000))
# directory_tree_txt = os.path.join(option_dir_path, f"directory_tree_{option_millis}_子文件.txt")
#
# with open(directory_tree_txt, "a") as record:
#     for dir_path, dir_names, filenames in os.walk(option_dir_path):
#         record.write(f"Directory: {dir_path}\n")
#         for dirname in dir_names:
#             record.write(f"\tSubdirectory: {dirname}\n")
#         for filename in filenames:
#             if filename.startswith("directory_tree_"):
#                 continue
#             record.write(f"\tFile: {filename}\n")

import urllib.request
import urllib.parse
url = 'https://www.so.com/s?ie=utf-8&q=IP'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'QiHooGUID=0084B5FA74E6738495CF4111CF7E108D.1684676924211; ISSW=1; __guid=15484592.2882677085174585300.1687914529400.2983; so-like-red=2; dpr=1; webp=1; so_huid=11lw8OJKSKehgCWZd5jgq2lAML2Agp78m99ogMPIc0Dfk%3D; __huid=11lw8OJKSKehgCWZd5jgq2lAML2Agp78m99ogMPIc0Dfk%3D; __DC_gid=6491553.870056633.1688120534012.1688120534012.1; _S=ijdvo1c6cmrbehqb0j14885j62; count=1; gtHuid=1; _uc_silent=1; erules=p1-9%7Cp4-2%7Cp3-5%7Cp2-3%7Cecr-1; WZWS4=f5e47d172b791ec1808c3137bcb6fffe',
    'Host': 'www.so.com',
    'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&ch=&tn=maxco7_dg&bar=&wd=IP&oq=IP&rsv_pq=f7ee744e000245e9&rsv_t=84c2ukWw2YO8yyRovbugOoMyXdtqH2nquXeQub2CQc7ZfL53JsrwxaHAq8P6rPtf&rqlang=cn&rsv_enter=0&rsv_btype=t&rsv_dl=tb',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
req = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(req)
context = response.read().decode('utf-8')
print(context)
with open("ipchaxun.html", "w", encoding="UTF-8") as file:
    file.write(context)


import lxml