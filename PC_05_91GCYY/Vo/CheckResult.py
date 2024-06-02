from PC_05_91GCYY.Vo.Category import Category
from PC_05_91GCYY.Vo.ComVo import ComVo


class CheckResult(ComVo):
    def __init__(self, category: Category, is_check: bool, count_video: int = 0, count_serno: int = 0,
                 count_m3u8: int = 0, count_img: int = 0):
        self.category = category
        self.is_check = is_check
        self.count_video = count_video
        self.count_serno = count_serno
        self.count_img = count_img
        self.count_m3u8 = count_m3u8
        self.count_diff = count_video - count_serno
        self.is_no_duplicate = count_video == count_serno
        self.is_file_complete = count_serno == count_img == count_m3u8


