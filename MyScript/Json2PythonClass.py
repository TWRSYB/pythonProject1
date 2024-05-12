import json


class Json2PythonClass:
    def __init__(self, task: []):
        if isinstance(task[1], str):
            task[1] = json.loads(task[1])
        self.task_list_list: [[[]]] = [[task]]
        print(task)

    def start(self):
        for i in range(5):
            if len(self.task_list_list) > i:
                for task in self.task_list_list[i]:
                    self.deal_one(task, i)

    def deal_one(self, json_obj: [], level: int):
        print(f'class {to_pascal_case(json_obj[0])}:\n\tdef __init__(self', end='')
        for key, value in json_obj[1].items():
            print(f', {key}', end='')
        print('):')
        for key, value in json_obj[1].items():
            print(f'\t\tself.{key}: {type(value).__name__} = {key}\t\t\t#\t{value}')
            if isinstance(value, dict):
                if len(self.task_list_list) <= level + 1:
                    self.task_list_list.append([])
                self.task_list_list[level + 1].append([key, value])
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                self.task_list_list[level + 1].append([key, value[0]])

def to_pascal_case(snake_str):
    # 将字符串拆分为单词列表
    words = snake_str.split('_')
    # 将每个单词的首字母转换为大写，并连接成一个字符串
    pascal_str = ''.join(word.capitalize() for word in words)
    return pascal_str


if __name__ == '__main__':
    json_text = '{"media_type":2,"has_dash_audio":true,"is_completed":true,"total_bytes":3989296,"downloaded_bytes":3989296,"title":"【创2024主题曲Summer Dream翻跳】说好了，我先过盛夏！","type_tag":"80","cover":"http:\/\/i2.hdslb.com\/bfs\/archive\/e15e9362af0b3e9f6c897ccbc5020b1762bdc482.jpg","video_quality":80,"prefered_video_quality":80,"guessed_total_bytes":0,"total_time_milli":51547,"danmaku_count":0,"time_update_stamp":1704469732310,"time_create_stamp":1704469722838,"can_play_in_advance":true,"interrupt_transform_temp_file":false,"quality_pithy_description":"1080P","quality_superscript":"","cache_version_code":7490200,"preferred_audio_quality":0,"audio_quality":0,"avid":283328518,"spid":0,"seasion_id":0,"bvid":"BV1Ec41187j8","owner_id":284194350,"owner_name":"Huhu安","owner_avatar":"https:\/\/i0.hdslb.com\/bfs\/face\/858ef89ae710dfdcbbef99296c2565a49c0c7da1.jpg","page_data":{"cid":1395425474,"page":2,"from":"vupload","part":"裸眼3D","link":"","vid":"","has_alias":false,"tid":199,"width":3840,"height":2160,"rotate":0,"download_title":"视频已缓存完成","download_subtitle":"【创2024主题曲Summer Dream翻跳】说好了，我先过盛夏！ 裸眼3D"}}'
    j = Json2PythonClass(['VideoVo', json_text])
    j.start()
