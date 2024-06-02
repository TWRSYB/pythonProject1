from A_04_FileDeal.FileNameValidate import correct_name
from PC_05_91GCYY.Config import URL_HOST
from PC_05_91GCYY.Vo.ComVo import ComVo


class Task(ComVo):

    def __init__(self, serno: str, href, title, category, data_ratio, img_src, vip_type, play_times, m3u8_url: str,
                 page_order: str):
        self.serno = serno
        self.href = href
        self.title = title
        self.category = category
        self.data_ratio = data_ratio
        self.img_src = img_src
        self.vip_type = vip_type
        self.play_times = play_times
        self.m3u8_url = m3u8_url
        self.host = URL_HOST
        self.page_order = page_order

    def get_name(self):
        return correct_name(f'{self.serno}_-_{self.title}_-_{self.vip_type}_-_{self.m3u8_url.split(".m3u8?val=")[1]}',
                            can_restored=True)




class ActressVo(ComVo):

    def __init__(self, id_in_javbus, url_avatar, nm_cn, nm_jp='', nm_en="", nm_kr='', movie_num=''):
        self.id_in_javbus = id_in_javbus
        self.url_avatar = url_avatar
        self.nm_cn = nm_cn
        self.nm_jp: str = nm_jp
        self.nm_en: str = nm_en
        self.nm_kr: str = nm_kr
        self.movie_num = movie_num
