import os

s = "hello,world,this,is,a,test"
result = s.split(",")  
print(result)  # 输出: ['hello', 'world', 'this', 'is', 'a', 'test']


def check_category(self, category, list_task_category, process_level):
    if category.page_count:
        dir_m3u8 = os.path.join(category.category_code, 'M3U8')
        dir_img = os.path.join(category.category_code, 'IMG')
        list_video_id = [vo_video_info.video_id for vo_video_info in list_task_category]
        set_video_id = set(list_video_id)  # video_id集合
        list_m3u8_id = [file_name.split('_', 1)[0] for file_name in os.listdir(dir_m3u8)]
        list_img_id = [file_name.split('_', 1)[0] for file_name in os.listdir(dir_img)]
