from PC_05_91GCYY.Vo.ComVo import ComVo


class Category(ComVo):

    def __init__(self, category_code: str, category_name: str, href: str, super_category_code: str = '',
                 page_count: int = 0, vip_type: str = '', count_video: int = 0, list_sub_category_code: list = None):
        self.category_code = category_code
        self.category_name = category_name
        self.href = href
        self.super_category_code = super_category_code
        self.page_count = page_count
        self.vip_type = vip_type
        self.count_video = count_video
        self.list_sub_category_code = list_sub_category_code

    def get_name(self):
        return f'{self.category_code}_-_{self.category_name}_-_{self.super_category_code}'

    def in_dict_list(self, list_category_dict):
        if not self.category_code in [category_dict.get('category_code') for category_dict in list_category_dict]:
            return False
        return True
