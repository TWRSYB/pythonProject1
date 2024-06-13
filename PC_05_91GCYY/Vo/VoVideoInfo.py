from A_04_FileDeal.FileNameValidate import correct_name
from PC_05_91GCYY.Config import URL_HOST
from PC_05_91GCYY.Vo.ComVo import ComVo


class VoVideoInfo(ComVo):

    def __init__(self, video_id: str, href, title, category, data_ratio, img_src, vip_type, play_times, m3u8_url: str,
                 page_order: str):
        self.video_id = video_id
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
        return correct_name(f'{self.video_id}_-_{self.title}_-_{self.vip_type}_-_{self.m3u8_url.split(".m3u8?val=")[1]}',
                            can_restored=True)

    def in_dict_list(self, list_vo_dict):
        if self.video_id not in [vo_dict.get('video_id') for vo_dict in list_vo_dict]:
            return False
        if self.title not in [vo_dict.get('title') for vo_dict in list_vo_dict]:
            return False
        if self.category not in [vo_dict.get('category') for vo_dict in list_vo_dict]:
            return False
        if self.img_src not in [vo_dict.get('img_src') for vo_dict in list_vo_dict]:
            return False
        if self.vip_type not in [vo_dict.get('vip_type') for vo_dict in list_vo_dict]:
            return False
        return True
