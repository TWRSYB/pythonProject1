from PC_05_91GCYY import executor

if __name__ == '__main__':
    executor.start()

# 全局流程
# 1. 获取分类
#   1. 获取分类
#       1. 获取子分类
#   2. 保存分类数据
# 2. 获取影片
#   1. 按分类获取影片
#       1. 按页获取
#           1. 获取影片信息
#           2. 保存影片数据
#           3. 保存影片资源
#               1. 影片图片
#               2. m3u8
#               3. 完整版m3u8
#       2. 为m3u8添加秘钥
#       3. 为完整版m3u8添加秘钥
# 3. 检查完整性
#   1. 读取分类数据
#   2. 读取影片数据
#   3. 检查完整性
#       1. 按分类检查完整性
#           1. 检查重复
#           2. 检查资源完整性
#       2. 保存检查结果列表
#   4. 补全数据
#       1. 遍历检查结果列表
#           1. 检查结果
#               1. 找出可能缺失的video_id列表
#               2. 根据video_id列表获取影片信息
#                   1. 获取影片信息
#                   2. 保存影片数据
#                   3. 保存影片资源
#                       1. 影片图片
#                       2. m3u8
#                       3. 完整版m3u8


# 全局流程
# 1. 获取分类
#   1. 获取分类
#       1. 获取子分类
#   2. 保存分类数据
# 2. 获取影片
#   1. 按分类获取影片
#       1. 按页获取
#           1. 获取影片信息
#               1. 影片图片
#               2. m3u8
#                   1. 获取并保存预览版m3u8并添加完整KEY_URI
#                   2. 获取并保存完整m3u8并添加完整KEY_URI
#           2. 保存影片数据
#       2. 检查完整性
#           1. 读取影片数据
#           2. 检查完整性
#               1. 检查重复
#               2. 检查资源完整性
#           3. 补全数据
#               1. 找出可能缺失的video_id列表
#               2. 根据video_id列表获取影片信息
#                   1. 获取影片信息
#                       1. 影片图片
#                       2. m3u8
#                           1. 获取并保存预览版m3u8并添加完整KEY_URI
#                           2. 获取并保存完整m3u8并添加完整KEY_URI
#                   2. 保存影片数据
# 3. 下载并合并影片

# 有反爬机制, 需要header
# 为避免304, 要删除header中的if-modified-since属性

# 未登录与登录情况下m3u8url地址是一样的, 下载的文件内容不一样, 未登录时只截取了正常文件的前2个ts
# 识别登录与未登录时headers有点不一样, 但不知道是否有影响, cookies是一样的, 猜测后端应该是在session中存储了登录状态
# m3u8无法使用potplayer打开, 应该需要session
# m3u8中有加密秘钥需要通过URL获取


# 4158
# 	20240506
# 		未登录:
#           headers:
#                 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#                 'accept-language': 'zh-CN,zh;q=0.9',
#                 'cache-control': 'max-age=0',
#                 'cookie': '_zhchat_chat_entIds=%5B%5D; _zhchat_chat_channelIds=%5B%7B%22customerId%22%3A%22661fcaeee3a0f40ae5581599%22%2C%22channelId%22%3A%22E6Z9dw%22%7D%5D; PHPSESSID=0cee5fd378d4ec39be25b9156f44dc98; isWelcomeTipsNoShow=1',
#                 'sec-fetch-dest': 'document',
#                 'sec-fetch-mode': 'navigate',
#                 'sec-fetch-site': 'none',
#                 'sec-fetch-user': '?1',
#                 'upgrade-insecure-requests': '1',
#                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
# 			m3u8url: https://g1hs.nestokra.com/vdata/get/play.m3u8?val=46df68048a67b9fa7cdaaa472eca9ecc523f2d4eca4be0
# 			m3u8内容:
# 				#EXTM3U
# 				#EXT-X-VERSION:3
# 				#EXT-X-KEY:METHOD=AES-128,URI="/sec"
# 				#EXT-X-PLAYLIST-TYPE:VOD
# 				#EXT-X-MEDIA-SEQUENCE:0
# 				#EXT-X-TARGETDURATION:3
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/ZSdiLDPd.ts
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/ZPp956oC.ts
# 				#EXT-X-ENDLIST
# 		已登录:
#           headers:
#                 'accept': '*/*',
#                 'accept-language': 'zh-CN,zh;q=0.9',
#                 'cookie': '_zhchat_chat_entIds=%5B%5D; _zhchat_chat_channelIds=%5B%7B%22customerId%22%3A%22661fcaeee3a0f40ae5581599%22%2C%22channelId%22%3A%22E6Z9dw%22%7D%5D; PHPSESSID=0cee5fd378d4ec39be25b9156f44dc98; isWelcomeTipsNoShow=1',
#                 'referer': 'https://g1hs.nestokra.com/vid/4158.html',
#                 'sec-ch-ua': '"Chromium";v="109", "Not_A Brand";v="99"',
#                 'sec-ch-ua-mobile': '?0',
#                 'sec-ch-ua-platform': '"Windows"',
#                 'sec-fetch-dest': 'empty',
#                 'sec-fetch-mode': 'cors',
#                 'sec-fetch-site': 'same-origin',
#                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
# 			m3u8url: https://g1hs.nestokra.com/vdata/get/play.m3u8?val=46df68048a67b9fa7cdaaa472eca9ecc523f2d4eca49e0
# 			m3u8内容:
# 				#EXTM3U
# 				#EXT-X-VERSION:3
# 				#EXT-X-KEY:METHOD=AES-128,URI="/sec"
# 				#EXT-X-PLAYLIST-TYPE:VOD
# 				#EXT-X-MEDIA-SEQUENCE:0
# 				#EXT-X-TARGETDURATION:3
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/ZSdiLDPd.ts
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/ZPp956oC.ts
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/Rvjomcua.ts
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/PjUzTND1.ts
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/iwgpDRLh.ts
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/XaWBoVPR.ts
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/AY0hqJJs.ts
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/t7TMK5oD.ts
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/MRSQOkKj.ts
# 				#EXTINF:3,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/bUCXMXQe.ts
# 				#EXTINF:1.16,
# 				https://eo.com.yangxingyue1.cn/uuv/4158/wNydrmHw.ts
# 				#EXT-X-ENDLIST

#   20240507
#       未登录
#           headers:
#                 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#                 'accept-language': 'zh-CN,zh;q=0.9',
#                 'cache-control': 'max-age=0',
#                 'cookie': '_zhchat_chat_entIds=%5B%5D; _zhchat_chat_channelIds=%5B%7B%22customerId%22%3A%22661fcaeee3a0f40ae5581599%22%2C%22channelId%22%3A%22E6Z9dw%22%7D%5D; isWelcomeTipsNoShow=1; PHPSESSID=2ed5d416031097d9e089e767f587ee3d',
#                 'referer': 'https://g1hs.nestokra.com/',
#                 'sec-fetch-dest': 'document',
#                 'sec-fetch-mode': 'navigate',
#                 'sec-fetch-site': 'same-origin',
#                 'sec-fetch-user': '?1',
#                 'upgrade-insecure-requests': '1',
#                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
#           m3u8url: https://g1hs.nestokra.com/vdata/get/play.m3u8?val=46df68048a67b9fa7cdaaa472eca9ecc523f2d4eca4be0
