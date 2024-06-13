from PC_05_91GCYY.Vo.Category import Category
from PC_05_91GCYY.Vo.ComVo import ComVo


class CheckResult(ComVo):
    def __init__(self, category: Category, list_video_id, set_video_id,
                 list_m3u8_id, list_img_id):
        self.category = category
        self.list_video_id = list_video_id
        self.set_video_id = set_video_id
        self.list_m3u8_id = list_m3u8_id
        self.list_img_id = list_img_id
        self.is_no_duplicate = len(list_video_id) == len(set_video_id)
        self.is_file_complete = len(list_video_id) == len(list_m3u8_id) == len(list_m3u8_id)